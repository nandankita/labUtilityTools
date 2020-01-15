'''
Created on Aug 20, 2018

@author: nanda
'''
from Bio import SeqIO
from Bio.Seq import Seq
import argparse
import textwrap
import os
from _collections import defaultdict


#####################################################################

def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Find out the missing scaffold slices
    python ~/aTools/utilities/missingScaffolds.py -i fastaScaffold/Symbiodinium_microadriaticum.fa -n merged-cutSc-newScaffoldList1kb60percent
    python ~/aTools/utilities/missingScaffolds.py -i fasta/Symbiodinium_microadriaticum.fa -n merged-listScfAfterFixSplitChromosome 
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_fasta_file' ,
                        help = "Input fasta file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-n" ,
                        metavar = 'input scaffold file' ,
                        help = "input scaffold  file" ,
                        dest = "scaffold",
                        required = True ,
                        type = str)
    
    
    return parser.parse_args()

###################################################################
def getRange(inputSlices,start,end):
    for i in inputSlices:
        n=i.split("__")
        if(int(n[0])<=start) and (int(n[1])>=end):
            return i
        
    return None
        
####################################################################

def getSlice(inputSlices,start,end, line):
    nSt = start-1
    nEd = end+1
    a = getRange(inputSlices,start,end)
    b = a.split("__")
    
    indx=inputSlices.index(a)
    if(nSt>0) and (int(b[0])<nSt):
        tmp1=b[0]+"__"+str(nSt)
        inputSlices[indx]=tmp1
        
        if(int(b[1])>nEd):
            tmp2=str(nEd)+"__"+b[1]
            inputSlices.insert(indx+1,tmp2)
    
    elif(int(b[1])>nEd):
        tmp2=str(nEd)+"__"+b[1]
        inputSlices[indx]=tmp2
        
    else:
        print(inputSlices,start,end, line)
        del inputSlices[indx]
    
    
    

#####################################################################
def findMissing(input_file,scaffold):
    output_file="MissingScaffolds"
    fastaInDict=defaultdict(list)
    with open(input_file) as FASTAIN, open(scaffold) as ORD, open(output_file, "w") as OUTFH:
        fastaParse = SeqIO.parse(FASTAIN,"fasta")
        
        for fastaSeq in fastaParse:
            s = str(fastaSeq.seq)
            idFasta = fastaSeq.id
            fastaInDict[idFasta]=[str(1)+"__"+str(len(s))]
            
        for line in ORD:
            line=line.rstrip("\n")
            cl=line.split("\t")
            val=cl[0].split("__")
            start=int(val[1])
            end=int(val[2])
            getSlice(fastaInDict[val[0]],start,end, line)
            
        for k,v in  fastaInDict.items():
            for i in v:
                OUTFH.write(k+"__"+i+"\n")
            
            



#####################################################################


def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    scaffold = os.path.abspath(arguments.scaffold)
    findMissing(input_file,scaffold)
    

#####################################################################

if __name__ == '__main__':
    main()
