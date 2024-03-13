
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
from pysat.card import *
x=WCNF()
rc2=RC2(x)
formula=CardEnc.equals(lits=[1,2,3,4,5],bound=3,encoding=6)
print(formula.to_dimacs())
print()
#
# e=ITotalizer(lits=[-1,-2,-3,-4,-5],ubound=2)
# for x in e.cnf.clauses:
#     rc2.add_clause(x)
# print(e.rhs)
# rc2.add_clause([e.rhs[0]])
ee=ITotalizer(lits=[1,2,3],ubound=3)
for x in ee.cnf.clauses:
    print(x)
    rc2.add_clause(x)
# rc2.add_clause([1])
# rc2.add_clause([2])
# rc2.add_clause([3])
# rc2.add_clause([-e.rhs[3]])
# rc2.add_clause([-e.rhs[0]])
# e.delete()
# e=ITotalizer(lits=[-1,-2,-3,-4,-5],ubound=3)
# for x in e.cnf:
#     rc2.add_clause(x)
m=rc2.compute()
print(ee.rhs)
print(m)
# [-2, 6]
# [-1, 6]
# [-1, -2, 7]
# [-4, 8]
# [-3, 8]
# [-3, -4, 9]
# [-6, 10]
# [-7, 11]
# [-5, 10]
# [-5, -6, 11]
# [-10, 12]
# [-11, 13]
# [-8, 12]
# [-9, 13]
# [-8, -10, 13]