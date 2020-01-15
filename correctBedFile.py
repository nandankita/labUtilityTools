'''
Created on Nov 15, 2018

@author: nanda
'''
import sys
inFile=sys.argv[1]
with open(inFile) as INFH, open("SmicGenes_vs_dinoChrs_100_b1_with_Annotstrand_startStop.bed","w") as OUTFH:
    for line in INFH:
        line=line.rstrip("\n")
        ln=line
        v=line.split("\t")
        if(int(v[2])<int(v[1])):
            ln="\t".join([v[0],v[2],v[1],v[3],v[4],v[5],v[6],v[7],v[8]])
        else:
            ln=line
        OUTFH.write(ln+"\n")