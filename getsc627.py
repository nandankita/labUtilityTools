'''
Created on Jan 12, 2018

@author: nanda
'''
from _collections import defaultdict
from Bio import SeqIO
input_file = "/nl/umw_job_dekker/users/an27w/dinoflagellets/genome/fasta/Symbiodinium_microadriaticum/Symbiodinium_microadriaticum.fa"

with open(input_file) as FASTAIN, open("scaffold627__280001__320000.fa", "w") as OUTFH:
    fastaParse = SeqIO.parse(FASTAIN,"fasta")
    for fastaSeq in fastaParse:
        s = str(fastaSeq.seq)
        idFasta = fastaSeq.id
        if(idFasta=="Smic.scaffold627"):
            start=280001-1
            end=320000
            OUTFH.write(">Smic.scaffold627__280001__320000\n")
            OUTFH.write(s[start:end])
    print("done")