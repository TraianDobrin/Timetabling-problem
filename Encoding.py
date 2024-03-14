from data_parser import *
from Totalizer import *

from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
from pysat.card import *

slot = {}
for ind, t in enumerate(times):
    slot[t] = ind
no_of_times = 25
cnt = 1
id = 'Id'
encodings = WCNF()
S = {}  # start times of events
Y = {}  # true if event i takes place at time j
K = {}  # event i starts at time j and takes k time slots = K[i][j][k]
R = {}  # resource i busy at time j with event k
A = {}  # resource i busy in time group j after time k
B = {}  # resource i busy in time group j before time k
X = {}  # resource r busy at time i
D = {}  # event i happens during time group j
Idle = {}  # resource i idle in time group j at time k
costFunction = {'Linear': lambda x: x, 'Quadratic': lambda x: x ** 2, 'Step': lambda x: 1 if x != 0 else 0}
# Assign time constraint
# Split Events constraint(hardcoded)
for e_key in events:

    e = events[e_key]
    K[e_key] = []
    for t in range(no_of_times):
        K[e_key].append([])
        K[e_key][t].append(0)
        for d in range(1, 3):
            K[e_key][t].append(cnt + 1)
            cnt += 1
    formula = []
    #print(e)
    S[e[id]] = []
    Y[e[id]] = []
    for t in range(no_of_times):
        S[e[id]].append(cnt + 1)
        formula.append(S[e[id]][t])
        cnt += 1

    encodings.append(formula)

    for t in range(no_of_times):
        Y[e[id]].append(cnt + 1)
        cnt += 1

    formula = []
    for t in range(no_of_times):
        formula = [-S[e[id]][t], Y[e[id]][t]]
        if t != no_of_times - 1:
            formula.append(Y[e[id]][t + 1])
        encodings.append(formula)

top = cnt
# Distribute split events

for e_key in events:
    e = events[e_key]
    if len(e['DistributeSplitEventsConstraint']) == 0:
        continue
    constraints = []
    for c_id in e['DistributeSplitEventsConstraint']:
        c = distribute_split_events[c_id]
        d = int(c['Duration'])
        min = int(c['Minimum'])
        maximum = int(c['Maximum'])
        formula = []

        for t in range(no_of_times):
            formula.append(K[e_key][t][d])

        formulaTOT = Totalizer(lits=formula, top=cnt)
        for f in formulaTOT.clauses:
            encodings.append(f)
        cnt = max(abs(lit) for clause in formulaTOT.clauses for lit in clause)
        # rhs is in unary, so if at any point
        # rhs[i]=0 and rhs[i-1]=1 then there are exactly i-1 true variables
        # then assign a corresponding cost. This has to happen exactly one
        # so the cost function is only applied once per violation
        # could have been done differently but I hoped this would be more helpful to the solver
        # the other solution was to add clauses -rhs[i] weight*costfunction(1) for i<min and similar for max
        # however, the solution from below allows for nonlinear cost function, while the other doesn't

        if min > 0:
            encodings.append([formulaTOT.root.lits[1]], costFunction[c['CostFunction']](min) * int(c['Weight']))
        for i in range(1, min):
            # encode a ^ b as exactly_2(a,b)
            miniform = Totalizer(lits=[-formulaTOT.root.lits[i], formulaTOT.root.lits[i - 1]], top=cnt)
            encodings.append([miniform.root.lits[2]], costFunction[c['CostFunction']](min - i) * int(c['Weight']))
            cnt = max(abs(lit) for clause in miniform.clauses for lit in clause)

        for i in range(maximum + 2, len(formula) + 1):
            miniform = Totalizer(lits=[-formulaTOT.root.lits[i], formulaTOT.root.lits[i - 1]], top=cnt)
            encodings.append([miniform.root.lits[2]],
                             costFunction[c['CostFunction']](i - maximum - 1) * int(c['Weight']))
            cnt = max(abs(lit) for clause in miniform.clauses for lit in clause)

        if maximum < len(formula):
            encodings.append([formulaTOT.root.lits[len(formula)]],
                             costFunction[c['CostFunction']]((len(formula) - maximum)) * int(c['Weight']))

# Prefer times constraint
for e_key in events:
    e = events[e_key]
    for t in range(4, no_of_times, 5):
        encodings.append([-K[e_key][t][2]])
# kind of hardcoded for brazil 1

# Spread events constraint

for cc in spread_events:
    c_times = []
    lims = []
    c = spread_events[cc]
    for tg in c['Times']:
        c_times.append([])
        lims.append([tg['Minimum'], tg['Maximum']])
        for t in timeGroups[tg['TimeGroup']]:
            c_times[len(c_times) - 1].append(slot[t])
    for ev_group in c['EventGroups']:
        lst = []
        for e in eventGroups[ev_group]:
            for x in c_times:
                lst = []
                for y in x:
                    lst.append(S[e][y])
                formula = CardEnc.atmost(lits=lst, bound=1, top_id=cnt)
                cnt = 1 + max(abs(lit) for clause in formula for lit in clause)
                # a bit hardcoded until we find an efficient way to count variables for easy cardinality constraints(
                # maybe a totalizer would be nice)
                # print(lst)
                for f in formula.clauses:
                    encodings.append(f)

# Avoid clashes constraint
for r in resources:
    R[r] = []

    for t in range(no_of_times):
        dct = {}
        lst = []
        for e in events:
            dct[e] = cnt + 1
            lst.append(cnt + 1)
            cnt += 1
        formula = CardEnc.atmost(lits=lst, bound=1, top_id=cnt)
        cnt = 1 + max(abs(lit) for clause in formula for lit in clause)
        for f in formula.clauses:
            encodings.append(f)
        R[r].append(dct)

# Limit idle times constraint

for x in resources:
    R[x] = []
    for t in range(no_of_times):
        # encoding equivalence relation here
        dct = {}
        for e in events:
            dct[e] = cnt + 1
            cnt += 1
        R[x].append(dct)

for x in resources:
    tg = []
    A[x] = {}
    for tg_key in timeGroups:
        tg = timeGroups[tg_key]
        A[x][tg_key] = []
        for t in tg:
            A[x][tg_key].append(cnt + 1)
            cnt += 1

for x in resources:
    tg = []
    B[x] = {}
    for tg_key in timeGroups:
        tg = timeGroups[tg_key]
        B[x][tg_key] = []
        for t in tg:
            B[x][tg_key].append(cnt + 1)
            cnt += 1

for x in resources:
    tg = []
    Idle[x] = {}
    for tg_key in timeGroups:
        tg = timeGroups[tg_key]
        Idle[x][tg_key] = []
        for t in tg:
            Idle[x][tg_key].append(cnt + 1)
            cnt += 1

for x in resources:
    X[x] = []
    for t in range(no_of_times):
        X[x].append(cnt + 1)
        cnt += 1

for x in resources:
    for t in range(no_of_times):
        # encoding equivalence relation here
        lst = []
        for e in events:
            lst.append(R[x][t][e])
            encodings.append([-R[x][t][e], X[x][t]])
        newlst = lst
        lst.append(-X[x][t])
        encodings.append(newlst)

for x in resources:
    tg = []
    for tg_key in timeGroups:
        tg = timeGroups[tg_key]
        # print(slot[tg[len(tg) - 1]])
        encodings.append([-A[x][tg_key][slot[tg[len(tg) - 1]] % 5]])
        encodings.append([-B[x][tg_key][0]])
        for tt in tg[:len(tg) - 1]:
            t = int(slot[tt]) % 5
            # a[x][tgkey][t]<=>()
            encodings.append([-A[x][tg_key][t], A[x][tg_key][t + 1], X[x][t + 1]])
            encodings.append([A[x][tg_key][t], -A[x][tg_key][t + 1]])
            encodings.append([A[x][tg_key][t], -X[x][t + 1]])

        for tt in tg[1:]:
            t = int(slot[tt]) % 5
            encodings.append([-B[x][tg_key][t], B[x][tg_key][t - 1], X[x][t - 1]])
            encodings.append([B[x][tg_key][t], -B[x][tg_key][t - 1]])
            encodings.append([B[x][tg_key][t], -X[x][t - 1]])

        for tt in tg:
            t = int(slot[tt]) % 5
            encodings.append([Idle[x][tg_key][t], X[x][t], -A[x][tg_key][t], -B[x][tg_key][t]])
            encodings.append([-Idle[x][tg_key][t], -X[x][t]])
            encodings.append([-Idle[x][tg_key][t], A[x][tg_key][t]])
            encodings.append([-Idle[x][tg_key][t], B[x][tg_key][t]])

for tg in timeGroups:
    if tg == 'gr_TimesDurationTwo':
        continue
    for r_key in resourceGroups['gr_Teachers']:
        for t in timeGroups[tg]:
            encodings.append([-Idle[r_key][tg][slot[t] % 5]], weight=3)

for rs in resourceGroups['gr_Teachers']:
    r = resources[rs]
    D[rs] = {}
    for tg in timeGroups:
        if tg == 'gr_TimesDurationTwo':
            continue
        D[rs][tg] = cnt + 1
        cnt += 1

for rs in resourceGroups['gr_Teachers']:
    r = resources[rs]
    for tg in timeGroups:
        if tg == 'gr_TimesDurationTwo':
            continue
        lst = []
        for tt in timeGroups[tg]:
            # print(tt)
            lst.append(X[rs][slot[tt] % 5])
        newlst = lst
        newlst.append(-D[rs][tg])
        encodings.append(newlst)
        for x in lst:
            encodings.append([D[rs][tg], -x])

for rs in resources:
    r = resources[rs]
    if len(r['ClusterBusyTimes']) == 0:
        continue
    for c_key in r['ClusterBusyTimes']:
        c = cluster_busy_times[c_key]
        lst = []
        min = int(c['Minimum'])
        maximum = int(c['Maximum'])
        w = int(c['Weight'])
        cf = c['CostFunction']

        # not handling case where multiple such constraints span the same time groups, optimizations could be made
        # for such things
        for tg in c['TimeGroups']:
            lst.append(D[rs][tg])
        tot = Totalizer(lst, top=cnt)
        cnt = max(abs(lit) for clause in formulaTOT.clauses for lit in clause)
        if min > 0:
            encodings.append(tot.root.lits[1], weight=w * costFunction[cf](min))
        for i in range(1, min):
            a = tot.root.lits[i]
            b = tot.root.lits[i - 1]
            minitot = Totalizer([-a, b], top=cnt)
            encodings.append([-minitot.root.lits[2]], weight=w * costFunction[cf](min - i))
            cnt = max(abs(lit) for clause in formulaTOT.clauses for lit in clause)
        for i in range(maximum + 2, len(lst) + 1):
            a = tot.root.lits[i]
            b = tot.root.lits[i - 1]
            minitot = Totalizer([-a, b], top=cnt)
            encodings.append([-minitot.root.lits[2]], weight=w * costFunction[cf](i - maximum - 1))
            cnt = max(abs(lit) for clause in formulaTOT.clauses for lit in clause)
        if maximum < len(lst):
            encodings.append([-tot.root.lits[len(lst)]], weight=w * costFunction[cf](len(lst) - maximum))

# Avoid Unavailable Times Constraints
for r in resources:
    # AvoidUnavailableTimes
    if len(resources[r]['AvoidUnavailableTimes']) == 0:
        continue
    for c in resources[r]['AvoidUnavailableTimes']:
        print(avoid_unavailable_times[c]['Times'])
        for t in avoid_unavailable_times[c]['Times']:
            encodings.append([-X[r][slot[t]]])



