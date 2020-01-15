'''
Created on Nov 9, 2018

@author: nanda
'''
import sys
chro=sys.argv[1]
with open("final.bed") as INFH, open(chro+".bed","w") as OUTFH:
    for line in INFH:
        line=line.rstrip("\n")
        v=line.split("\t")
        if(v[0]==chro):
            OUTFH.write(line)
            OUTFH.write("\n")