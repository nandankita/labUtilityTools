'''
Created on Nov 26, 2018

@author: nanda
python ~/aTools/utilities/addPositions.py
'''
posStart=1

with open("missing-Scaffolds.chrom.sizes", 'r') as orderFH, open("scaffoldsPositionFile", 'w') as binFH: 
        for line in orderFH:
            line = line.rstrip('\n')
            v=line.split("\t")
            posEnd=posStart+int(v[1])-1
            st="chr95__"+str(posStart)+"__"+str(posEnd)
            binFH.write("\t".join([line,st]))
            binFH.write("\n")
            posStart=posEnd+1
