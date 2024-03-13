class Totalizer:
    def __init__(self, lits, top):
        self.lits = lits
        self.clauses = []
        queue = []
        for x in lits:
            node = Node([x])
            queue.append(node)

        while len(queue)>1:
            left = queue.pop(0)
            right = queue.pop(0)
            lst = []
            for i in range(len(left.lits)+len(right.lits)-2):
                lst.append(top)
                top+=1
            node = Node(lst)
            node.left=left
            node.right=right
            queue.append(node)
            for a in range(len(left.lits)):
                for b in range(len(right.lits)):
                    if a!=0 and b!=0:
                        self.clauses.append([-left.lits[a],-right.lits[b],node.lits[a+b]])
                    else:
                        if a!=0:
                            self.clauses.append([-left.lits[a],node.lits[a+b]])
                        else:
                            if b!=0:
                                self.clauses.append([-right.lits[b],node.lits[a+b]])
                    if a!=len(left.lits)-1 and b != len(right.lits)-1:
                        self.clauses.append([left.lits[a+1],right.lits[b+1],-node.lits[a+b+1]])
                    else:
                        if a!=len(left.lits)-1:
                            self.clauses.append([left.lits[a+1],-node.lits[a+b+1]])
                        else:
                            if b!=len(right.lits)-1:
                            #print(f"{b} {len(right.lits)} {a} {len(left.lits)}")
                                self.clauses.append([right.lits[b+1],-node.lits[a+b+1]])
                    if left.lits==[3]:
                        print(self.clauses[-1+len(self.clauses)])
            self.root=queue[0]


class Node:
    def __init__(self, lits):
        self.lits=[]
        self.lits.append(0)
        self.left=None
        self.right=None
        for x in lits:
            self.lits.append(x)