from Totalizer import *
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
from pysat.card import *
from Encoding import *
import xml.etree.ElementTree as ET



evt=[]
for e in events:
    dur=0
    print(e, end=' starts at: \n')
    for i in range(25):
        if m[S[e][i]]>0:
            print(i, end=' and takes: \n')
        if m[Y[e][i]]>0:
            print(f"active at {i}")
            dur+=1
            for d in range(1,6):
                if(m[K[e][i][d]]>0):
                   evt.append([e,i,d])


# Create the root element
root = ET.Element("SolutionGroups")

# Create a SolutionGroup element
solution_group = ET.SubElement(root, "SolutionGroup")
solution_group.set("Id", "ceva")
# Create a Metadata element

metadata = ET.SubElement(solution_group, "MetaData")
# Create a Solution element
solution = ET.SubElement(solution_group, "Solution")
solution.set("Reference", "BrazilInstance1_XHSTT-v2014")
con=ET.SubElement(metadata,"Contributor")
con.text="someone"
nt=ET.SubElement(metadata,"Date")
nt.text="March 2024"
des=ET.SubElement(metadata,"Description")
des.text="des"
# Create an Events element
events = ET.SubElement(solution, "Events")

dic=["Mo_1","Mo_2","Mo_3","Mo_4","Mo_5","Tu_1","Tu_2","Tu_3","Tu_4","Tu_5","We_1","We_2","We_3","We_4","We_5","Th_1","Th_2","Th_3","Th_4","Th_5","Fr_1","Fr_2","Fr_3","Fr_4","Fr_5"]


# Assuming `evt` is a list of tuples [(reference, time, duration), ...]
for x in evt:
    # Create an Event element
    event = ET.SubElement(events, "Event")
    event.set("Reference", x[0])

    # Create a Duration element
    duration = ET.SubElement(event, "Duration")
    duration.text = str(x[2])

    # Create a Time element
    time = ET.SubElement(event, "Time")
    time.set("Reference", dic[x[1]])

# Create an ElementTree object
tree = ET.ElementTree(root)

# Write the ElementTree object to a file
tree.write("Solution.xml", encoding="utf-8", xml_declaration=True)