'''
Created on May 20, 2019

@author: nanda
python ~/aTools/utilities/95clustersPostion.py
'''
posStart=1
prCluster=""
with open("missingClusterScaffoldList", "r") as lineFH, open("missingClusterScaffoldListPostion", "w") as overFH:
    for line in lineFH:
            line = line.rstrip('\n')
            v=line.split("\t")
            print(prCluster,v[1])
            if(prCluster != v[1]):
                posStart=1
            sc=v[0].split("__")
            diff=int(sc[2])-int(sc[1])+1
            posEnd=posStart+diff-1
            overFH.write("\t".join([v[1],str(posStart),str(posEnd),v[0]]))
            overFH.write("\n")
            posStart=posEnd+1
            prCluster=v[1]
            