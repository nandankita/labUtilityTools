'''
Created on Jan 22, 2019

@author: nanda
python ~/aTools/utilities/scaffoldfindheaderChr95.py
'''
from _collections import defaultdict

scfDict={}
karDict=defaultdict(list)
#with open("filteredGe9999.chrom.sizes.header", "r") as header1FH, open("cluster13.predpos.header", "r") as header2FH, open("cluster13.scaffolds.header", "w") as header3FH:
with open("filteredGe9999.chrom.sizes.header", "r") as header1FH, open("sorted.Karyotype_500000_large_clusters.scaffold-header.tab", "r") as header2FH, \
open("chr95rearrangedClusters.header", "r") as header3FH, open("chr95rearrangedClusters.scaffolds.header", "w") as header4FH:
    for line in header1FH:
        line=line.rstrip("\n")
        v=line.split("\t")
        scfDict[v[2]]=v[0]
    
#     for line in header2FH:
#         line=line.rstrip("\n")
#         v=line.split("__")
#         n=scfDict[v[0]]
#         header3FH.write("__".join([n,v[1],v[2]]))
#         header3FH.write("\n")
    
    for line in header2FH:
        line=line.rstrip("\n")
        v=line.split("\t")
        n=scfDict[v[0]]
        header3FH.write("\t".join([n,v[1],v[2],v[3]]))
        header3FH.write("\n")