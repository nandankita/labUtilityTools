'''
Created on Aug 21, 2018

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
    python ~/aTools/utilities/sortChromosomes.py -i Symbio-final.fa -n mappingChr2sortedchromosomesizes
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_fasta_file' ,
                        help = "Input fasta file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-n" ,
                        metavar = 'input mapping file' ,
                        help = "input mapping  file" ,
                        dest = "mapping",
                        required = True ,
                        type = str)
    
    
    return parser.parse_args()

###################################################################
#####################################################################
def sortChr(input_file,mapping):
    output_file="dino-v1.0.fa"
    fastaInDict=defaultdict(list)
    with open(input_file) as FASTAIN, open(mapping) as ORD, open(output_file, "w") as OUTFH:
        fastaParse = SeqIO.parse(FASTAIN,"fasta")
        
        for fastaSeq in fastaParse:
            s = str(fastaSeq.seq)
            idFasta = fastaSeq.id
            fastaInDict[idFasta]=s
        
        print("Read sequences - mapping now")
        for line in ORD:
            line=line.rstrip("\n")
            m=line.split("\t")
            
            OUTFH.write(">"+m[2]+"\n")
            OUTFH.write(fastaInDict[m[0]])
            OUTFH.write("\n")
            
            

#####################################################################


def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    mapping = os.path.abspath(arguments.mapping)
    sortChr(input_file,mapping)
    

#####################################################################

if __name__ == '__main__':
    main()
