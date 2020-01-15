'''
Created on Mar 18, 2019

@author: nanda
python ~/aTools/utilities/sortchr95clusters.py 

'''
from _collections import defaultdict

with open("chr-clusters95-interactionList-sorted", "r") as lineFH, open("chr95-scaffold-clusters-rearranged", "r") as scFH, \
open("sortedByInteractionClusterList","w") as OUT:
    clusterSortList=[]
    scList=defaultdict(list)
    for line in lineFH:
        line=line.rstrip("\n")
        indV=line.split("\t")
        clusterSortList.append(indV[0])
    
    
    for line in scFH:
        line=line.rstrip("\n")
        indV=line.split("\t")
        scList["cluster"+indV[1]].append(indV[0])
    
    
    for i in clusterSortList:
        for values in scList[i]:
            OUT.write(values+"\t"+i+"\n")
        
        
    
    
    
    