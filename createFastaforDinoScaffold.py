'''
Created on Dec 12, 2017

@author: nanda
'''
from Bio import SeqIO
from Bio.Seq import Seq
import argparse
import textwrap
import os
from _collections import defaultdict, OrderedDict


#####################################################################

def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Given a Fasta file and order file, it creates a new fasta file based on that order.
    python ~/aTools/fasta_tools/createFastaforDinoScaffold.py -i Symbiodinium_microadriaticum.fa -n sortedMissingScaffolds
       ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_fasta_file' ,
                        help = "Input fasta file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-n" ,
                        metavar = 'input order file' ,
                        help = "correct order file" ,
                        dest = "order",
                        required = True ,
                        type = str)
    
    
    return parser.parse_args()

#####################################################################
def createFasta(input_file,order):
    output_file="missing-Scaffolds.fa"
    fastaInDict=OrderedDict()
    fastaOutDict=defaultdict(list)
    with open(input_file) as FASTAIN, open(order) as ORD, open(output_file, "w") as OUTFH:
        fastaParse = SeqIO.parse(FASTAIN,"fasta")
        for fastaSeq in fastaParse:
            s = str(fastaSeq.seq)
            idFasta = fastaSeq.id
            fastaInDict[idFasta]=s
        for line in ORD:
            line=line.rstrip("\n")
            cl=line.split("\t")
            val=cl[0].split("__")
            start=int(val[1])-1
            end=int(val[2])
            seq= fastaInDict[val[0]][start:end]
            
            if(cl[2]=="minus"):
                s = Seq(seq)
                rc=s.reverse_complement()
                seq=str(rc)
                
            fastaOutDict[cl[0]].append(seq)
            
#         for keys in sorted(fastaOutDict.iterkeys()):
#             fastaOutDict[keys].append("NNNNNNNNNNNNNNNNNNNN")
            
        for keys,values in fastaOutDict.items():
            print("Writing Chromosome"+keys)
            chrom=keys
            seqVal=values
            #size=len(seqVal)
            OUTFH.write(">"+chrom+"\n")
            OUTFH.write(seqVal)
            OUTFH.write("\n")
                
    

#####################################################################


def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    order = os.path.abspath(arguments.order)
    createFasta(input_file,order)
    

#####################################################################

if __name__ == '__main__':
    main()
