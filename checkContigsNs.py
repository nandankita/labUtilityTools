'''
Created on Oct 24, 2019

@author: nanda
python ~/aTools/utilities/checkContigsNs.py
'''
from Bio import SeqIO
from Bio.Seq import Seq
from _collections import defaultdict, OrderedDict
from itertools import groupby
from collections import Counter
import re



counter=0
fastaInDict=dict()
nCount=[]


# genomefasta="/nl/umw_job_dekker/users/an27w/dinoflagellets/genome/smic1.0/smic1.0.fa"
# boundariesFile="/nl/umw_job_dekker/users/an27w/boundries/boundariesWithinSubscaffolds-smic1.0.bed"

# genomefasta="/nl/umw_job_dekker/users/an27w/rawPacBio/LR_Gapcloser/src/Output-94chr-smic1.0-added100NeachChunk/iteration-6/gapclosed-clusters.added100Neachchunk.fa"
# boundariesFile="/nl/umw_job_dekker/users/an27w/sing-distiller/n_eachchunk_gapclosed/results-chronly/boundaries/gapclosed.N_each_chunk_manuallycorrected.boundaries.bed"
#boundariesFile="test"
genomefasta="/nl/umw_job_dekker/users/an27w/rawPacBio/Gapcloser/LR_Gapcloser/smic1.0-gapcloserinput-added100NseachChunk.fa"
boundariesFile="/nl/umw_job_dekker/users/an27w/boundaries-final/10kbInsulation-filtered-manuallyCorrected-only"

# genomefasta="/nl/umw_job_dekker/users/an27w/rawPacBio/LR_Gapcloser/smic1.0-gapcloserinput-100NsatScjunc.fa"
# boundariesFile="/nl/umw_job_dekker/users/an27w/boundaries-final/10kbInsulation-filtered-manuallyCorrected-only"


with open(genomefasta, "r") as FASTAIN, open(boundariesFile, "r") as ORD1, open("boundariesWithinContigs.bed" , "w") as ORD2:
        fastaParse = SeqIO.parse(FASTAIN,"fasta")
        for fastaSeq in fastaParse:
            s = str(fastaSeq.seq)
            idFasta = fastaSeq.id
            fastaInDict[idFasta]=s
        for line in ORD1:
            line=line.rstrip("\n")
            v=line.split("\t")
           # val=v[3].split("__")
            #print(v)
            start=int(v[1])-1-10000
            end=int(v[2])+10000
            chrom=v[0] #abcdnnnaaa
#             senq=fastaInDict[chrom][start:end][0]
            print(start-end)
            if(start<0) or end>len(fastaInDict[chrom]):
                #print("here")
                continue
            else:
                a=fastaInDict[chrom][start:end]
#                b="N"
#               number=a.count("N")
                
#                 if(number<24):
#                     ORD2.write(line+"\n")
                the_ones = re.findall(r"N+", a)
                
                
                if the_ones:
                    max_n = len(max(the_ones, key=len))
                    
                    if(max_n<24):
                        ORD2.write(line+"\n")
                
                else:
                    ORD2.write(line+"\n")
#                   
#                 for i in fastaInDict[chrom][start:end]:
#                     if (i=="N"):
#                         counter+=1
#                         inside=True
#                     else:
#                         if(inside==True):
#                             nCount.append(counter)
#                         counter=0
#                         inside=False
#                 pwrite=True
#                 for c in nCount:
#                     if(c>=24):
#                         pwrite=False
#                         break
#                 if(pwrite==True):
#                     ORD2.write(line+"\n")
#                 nCount=[]   
             
            
            
            
            
            
            
            
            
            
            