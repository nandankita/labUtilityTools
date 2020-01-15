'''
Created on Feb 5, 2019

@author: nanda
python ~/aTools/utilities/filterBoundaryBedFile.py
'''
with open("chrD-40kb--is520000--nt0--ids320000--ss0--immean.insulation.boundaries.bed", "r") as header1FH, \
open("chrD-40kb--is520000--nt0--ids320000--ss0--immean.insulation.filter.boundaries.bed", "w") as header2FH:
    c=0
    for line in header1FH:
        line=line.rstrip("\n")
        if(c==0):
            header2FH.write(line+"\n")
            c+=1
        else:
            v=line.split("\t")
            if(float(v[4])>=0.20):
                header2FH.write(line+"\n")
