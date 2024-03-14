from Totalizer import *
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
from pysat.card import *
x=WCNF()
rc2=RC2(x)
formula=CardEnc.equals(lits=[1,2,3,4,5],bound=4,encoding=6)
print(formula.to_dimacs())
print()
f=Totalizer(lits=[-1,-2,-3,-4,-5,-6,7,-8,-9,-10,-11],top=12)
print()
print(f.clauses)
n=f.root

def dfs(n):
    if n==None:
        return
    print(n.lits[1:])
    dfs(n.left)
    dfs(n.right)
dfs(n)
for c in f.clauses:
    rc2.add_clause(c)
#rc2.add_clause([f.root.lits[7]])

rc2.add_clause([f.root.lits[11]])
m=rc2.compute()
print(m)