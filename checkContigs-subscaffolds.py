'''
Created on May 2, 2020

@author: nanda
python ~/aTools/utilities/checkContigs-subscaffolds.py   boundariesWithinContigs.bed
'''
import sys
print(sys.argv[1])

file=sys.argv[1]

with open(file, "r") as FIN, open("boundariesWithinContigssubscaffolds.bed" , "w") as ORD2:
    for line in FIN:
        line=line.rstrip("\n")
        v=line.split("\t")
        
        if((int(v[1])-30000-1)>int(v[4])) and ((int(v[2])+30000+1)<int(v[5])):
            ORD2.write(line+"\n")


