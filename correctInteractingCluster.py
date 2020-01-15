'''
Created on May 6, 2019

@author: nanda
'''
lastChr=""
lastScf=""
with open("interactionList", "r") as intList, open("interactionList-corrected", "w") as intCFH:
    for line in intList:
        line=line.rstrip("\n")
        v=line.split("\t")
        scf=v[0].split("__")[0]
        
        if(float(v[5])==0.0) and (lastScf==scf):
            intCFH.write("\t".join([v[0],v[1],v[2],lastChr,v[5]]))
            intCFH.write("\n")
        elif(float(v[5])==0.0) and (lastScf!=scf):
            intCFH.write("\t".join([v[0],v[1],v[2],"chr95",v[5]]))
            intCFH.write("\n")
        else:
            intCFH.write("\t".join([v[0],v[1],v[2],v[4],v[5]]))
            intCFH.write("\n")
        lastChr=v[4]
        lastScf=scf
        