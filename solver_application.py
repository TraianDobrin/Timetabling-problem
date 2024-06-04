from Encoding import *

rc2 = RC2(encodings)
mm=rc2.compute()

with open("assignment.txt", 'w') as file:
    # Write each element of the list to the file
    for item in mm:
        file.write("%s\n" % item)