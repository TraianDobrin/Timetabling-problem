from data_parser import *

from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
from pysat.card import *

slot = {}
for ind, t in enumerate(times):
    slot[t]=ind+1
no_of_times=25
cnt=1
id='Id'
encodings = WCNF()
S = {} # start times of events
Y = {} # true if event i takes place at time j
K = {} # event i starts at time j and takes k time slots = K[i][j][k]
R = {} # resource i busy at time j with event k
A = {} # resource i busy in time group j after time k
B = {} # resource i busy in time group j before time k
costFunction={}
costFunction['Linear'] = lambda x : x
costFunction['Quadratic'] = lambda x : x**2
costFunction['Step'] = lambda x : 1 if x!=0 else 0
# Assign time constraint
# Split Events constraint(hardcoded)
for e_key in events:

    e=events[e_key]
    K[e_key]=[]
    for t in range(no_of_times):
        K[e_key].append([])
        K[e_key][t].append(0)
        for d in range(1,3):
            K[e_key][t].append(cnt+1)
            cnt += 1
    formula = []
    print(e)
    S[e[id]] = []
    Y[e[id]] = []
    S[e[id]].append(0)
    Y[e[id]].append(0)
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
        formula = []
        formula.append(-S[e[id]][t])
        formula.append(Y[e[id]][t])
        if t != no_of_times - 1:
            formula.append(Y[e[id]][t+1])
        encodings.append(formula)

top=cnt
# Distribute split events
'''
for e_key in events:
    e=events[e_key]
    if len(e['DistributeSplitEventsConstraint']) == 0:
        continue
    constraints=[]
    for c_id in e['DistributeSplitEventsConstraint']:
        c=distribute_split_events[c_id]
        d = int(c['Duration'])
        min = int(c['Minimum'])
        max = int(c['Maximum'])
        formula = []

        for t in range(no_of_times):
            formula.append(K[e_key][t][d])

        formulaTOT=ITotalizer(lits=formula,ubound=len(formula),top_id=10000)
        for f in formulaTOT.cnf.clauses:
            encodings.append(f)
        # rhs is in unary, so if at any point
        # rhs[i]=0 and rhs[i-1]=1 then there are exactly i-1 true variables
        # then assign a corresponding cost. This has to happen exactly one
        # so the cost function is only applied once per violation
        # could have been done differently but I hoped this would be more helpful to the solver
        # the other solution was to add clauses -rhs[i] weight*costfunction for i<min and similar for max
        # however, the solution from below allows for nonlinear cost function, while the other doesn't

        if min>0:
            encodings.append([formulaTOT.rhs[0]],costFunction[c['CostFunction']](min)*int(c['Weight']))
        for i in range(1,min):
            # encode a ^ b as exactly_2(a,b)
            miniform = ITotalizer(lits=[-formulaTOT.rhs[i],formulaTOT.rhs[i-1]],ubound=2,top_id=top)
            encodings.append([miniform.rhs[2]],costFunction[c['CostFunction']](min-i)*c['Weight'])
            miniform.delete()

        for i in range(max+2,len(formulaTOT.cnf.clauses)):
            miniform = ITotalizer(lits=[-formulaTOT.rhs[i],formulaTOT.rhs[i-1]],ubound=2,top_id=top)
            encodings.append([miniform.rhs[2]],costFunction[c['CostFunction']](i-max-1)*c['Weight'])
            miniform.delete()

        if max<len(formula):
            encodings.append([formulaTOT.rhs[len(formula)]],costFunction[c['CostFunction']]((len(formula)-max))*c['Weight'])
# my feather
'''
# Prefer times constraint
for e_key in events:
    e=events[e_key]
    for t in range(4,no_of_times,5):
        encodings.append([-K[e_key][t][2]])
# kind of hardcoded for brazil 1

# Spread events constraint

for cc in spread_events:
    c_times = []
    lims = []
    c=spread_events[cc]
    for tg in c['Times']:
        c_times.append([])
        lims.append([tg['Minimum'],tg['Maximum']])
        for t in timeGroups[tg['TimeGroup']]:
            c_times[len(c_times) - 1].append(slot[t])
    for ev_group in c['EventGroups']:
        lst=[]
        for e in eventGroups[ev_group]:
            for x in c_times:
                lst = []
                for y in x:
                    lst.append(S[e][y])
                formula=CardEnc.atmost(lits=lst,bound=1)
                # a bit hardcoded until we find an efficient way to count variables for easy cardinality constraints(maybe a totalizer would be nice)
                print(lst)
                for f in formula.clauses:
                    encodings.append(f)

# Avoid clashes constraint
for r in resources:
    K[r]=[]
    K[r].append(0)

    for t in range(no_of_times):
        dct = {}
        lst = []
        for e in events:
            dct[e] = cnt + 1
            lst.append(cnt + 1)
            cnt += 1
        formula=CardEnc.atmost(lits=lst,bound=1)
        for f in formula.clauses:
             encodings.append(f)
        K[r].append(dct)

# Limit idle times constraint

# for x in resources:
#     tg = []
#     for tg_key in timeGroups:
#         tg = timeGroups[tg_key]
#         encodings.append(-A[x][tg_key][tg[len(tg)-1]])
#         for t in tg:
#
#
#
#
