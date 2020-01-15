'''
Created on Mar 28, 2018

@author: nanda
'''
import argparse
import textwrap
import os
from Bio import SeqIO
import re
import numpy as np

#####################################################################

def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    It will find the start, end, length of N's in the fasta file
    python ~/aTools/fasta_tools/NsFinderInFasta.py -i Symbiodinium_microadriaticum-1.0.fa
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_fasta_file' ,
                        help = "Input fasta file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    return parser.parse_args()


#####################################################################
def nFinder(input_file):
    output_file="NsReport.txt"
    with open(input_file) as FASTAIN, open(output_file,"w") as OUTFH:
        fastaParse = SeqIO.parse(FASTAIN,"fasta")
        for fastaSeq in fastaParse:
            s = str(fastaSeq.seq)
            idFasta = fastaSeq.id
            print("Working on "+idFasta)
            re.findall("N+",s)
            start=[m.start() for m in re.finditer('N+', s)]
            end=[m.end() for m in re.finditer('N+', s)]
            diff=np.subtract(end,start)
            for i in range(len(diff)):
                OUTFH.write(idFasta+"\t"+str(start[i]+1)+"\t"+str(end[i])+"\t"+str(diff[i])+"\n")
            


#####################################################################


def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    nFinder(input_file)
    

#####################################################################

if __name__ == '__main__':
    main()