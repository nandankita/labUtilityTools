'''
Created on Oct 24, 2019

@author: nanda
'''
from Bio import SeqIO
from Bio.Seq import Seq
from _collections import defaultdict, OrderedDict
from itertools import groupby
from collections import Counter
counter=0
fastaInDict=dict()
nCount=[]

with open("/nl/umw_job_dekker/users/an27w/dinoflagellets/genome/fasta/Symbiodinium_microadriaticum/Symbiodinium_microadriaticum.fa", "r") as FASTAIN,open("boundariesWithinSubscaffolds.bed", "r") as ORD1, open("boundariesWithinContigs.bed" , "w") as ORD2:
        fastaParse = SeqIO.parse(FASTAIN,"fasta")
        for fastaSeq in fastaParse:
            s = str(fastaSeq.seq)
            idFasta = fastaSeq.id
            fastaInDict[idFasta]=s
        for line in ORD1:
            line=line.rstrip("\n")
            v=line.split("\t")
            val=v[3].split("__")
            start=int(val[1])-1
            end=int(val[2])
            chrom=val[0] #abcdnnnaaa
#             senq=fastaInDict[chrom][start:end][0]
            inside=False
            for i in fastaInDict[chrom][start:end]:
                if (i=="N"):
                    counter+=1
                    inside=True
                else:
                    if(inside==True):
                        nCount.append(counter)
                    counter=0
                    inside=False
            pwrite=True
            for c in nCount:
                if(c>=24):
                    pwrite=False
                    break
            if(pwrite==True):
                ORD2.write(line+"\n")
            nCount=[]   