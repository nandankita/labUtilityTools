'''
Created on Mar 20, 2018

@author: nanda
'''
#with open("pacbio.pairs.map", "r") as PacFH:
with open("nanopore.pairs.map", "r") as PacFH:
    same=0
    not_same=0
    for line in PacFH:
        line=line.rstrip("\n")
        v=line.split("\t")
        if(str(v[0])==str(v[1])):
            same+=1
        else:
            not_same+=1

print("Same values="+str(same))
print("Not Same values="+str(not_same))