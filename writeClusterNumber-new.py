'''
Created on Dec 12, 2018

@author: nanda
'''
from _collections import defaultdict

with open("filteredGe9999.chrom.sizes.header") as pos, open("header500Rearranged") as sc, open("Karyotype_500000_large_clusters.tab") as kar, open("chr95-scaffold-clusters", "w") as outFile:
    scaffoldNumberMap=defaultdict()
    scaffoldKaryotypeCluster=defaultdict()
    
    for line in pos:
        line=line.rstrip("\n")
        v=line.split("\t")
        if(int(v[1])<=500000):
            k="__".join([v[2],str(1),v[1]])
            scaffoldNumberMap[k]=v[0]
        else:
            s=v[0].split("__")
            
            k1="__".join([v[2],str(1),str(500000)])
            v1="__".join([s[0],s[1],str(int(s[1])+500000-1)])
            scaffoldNumberMap[k1]=v1
            
            
            k2="__".join([v[2],str(500001),v[1]])
            v2="__".join([s[0],str(int(s[1])+500000),s[2]])
            scaffoldNumberMap[k2]=v2
            
            
    
    for line in kar:
        line=line.rstrip("\n")
        v=line.split("\t")
        scf="__".join([v[0],v[1],v[2]])
        scaffoldKaryotypeCluster[scf]=v[3]
    
    
    for line in sc:
        line=line.rstrip("\n")
        clusterNumber=scaffoldKaryotypeCluster[line]
        actScaffold=scaffoldNumberMap[line]
        outFile.write("\t".join([actScaffold,clusterNumber]))
        outFile.write("\n")