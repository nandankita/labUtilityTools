'''
Created on Sep 6, 2018

@author: nanda

python ~/aTools/utilities/appendDeleteIndex.py
'''
from _collections import defaultdict

with open("unselectedIndexLocation1kb60percent") as indx1, open("new-delete") as indx2, open("totalAppendedIndx", "w") as OUTFH:
    indx60=defaultdict(list)
    indx60Fin=defaultdict(list)
    for line in indx1:
        line=line.rstrip("\n")
        v=line.split(":")
        indx60[v[0]].append(v[1])
    
    for i in indx2:
        i=i.rstrip("\n")
        v=i.split(":")
        loc=v[1].split("-")
        for n in range(int(loc[0]),int(loc[1]),1000):
            p=str(n)+"-"+str(n+999)
            indx60[v[0]].append(p)
    
    for k,v in indx60.items():
        vals=sorted(v, key=lambda x: int(x.split("-")[0]))
        #nodup=list(set(vals, key=lambda x: int(x.split("-")[0])))
        indx60Fin[k].append(vals)
    
    for k,v in sorted(indx60Fin.items()):
        c=0
        for n in indx60Fin[k]:
            c+=1
            if(c>1):
                print("here 2")
            for b in n:
                OUTFH.write(k+":"+b+"\n")
        