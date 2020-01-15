'''
Created on Aug 6, 2018

@author: nanda

python ~/aTools/utilities/removedBinsList.py
'''


with open("1kbHeadersFileBeforeRemoval") as SCPLIST, open("unselectedIndex60percent") as ORD, open("1kbHeadersFileAfterRemoval", "w") as OUTFH, open("1kbHeadersRemovedIndex", "w") as OUT2:
    ls=[]
    for l in ORD:
        l=l.rstrip("\n")
        ls.append(int(l)-1)
    
    c=0
    for line in SCPLIST:
        if (c in ls):
            OUT2.write(line)
            ls.remove(c)
        else:
            OUTFH.write(line)
        c+=1