'''
Created on Dec 12, 2017

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
    It will add remaining scaffolds to the fasta file
    python ~/aTools/utilities/pacbioReadLengForPairs.py -i filtered_subreads.fastq -p pacbio.nodups.pairs.map -o pacbio.nodups.pairs.leng
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_fastq_file' ,
                        help = "Input fastq file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-p" ,
                        metavar = 'input pairs file' ,
                        help = "input pairs file" ,
                        dest = "pairs",
                        required = True ,
                        type = str)
    
    parser.add_argument("-o" ,
                        metavar = 'output file' ,
                        help = "output file" ,
                        dest = "out",
                        required = True ,
                        type = str)
    
    
    return parser.parse_args()

#####################################################################
def calLength(input_file,output_file,pairs):
    fastqInDict=dict()
    with open(input_file) as FASTQIN, open(output_file, "w") as OUT, open(pairs) as PAR:
        fastqParse = SeqIO.parse(FASTQIN,"fastq")
        for fastqSeq in fastqParse:
            s = str(fastqSeq.seq)
            idFastq = fastqSeq.id
            fastqInDict[idFastq]=s
        for line in PAR:
            line=line.rstrip("\n")
            val=line.split("\t")
            seqLeng=len(fastqInDict[val[0]])
            OUT.write(line+"\t"+str(seqLeng))
            OUT.write("\n")

#####################################################################


def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    output_file= os.path.abspath(arguments.out)
    pairs = os.path.abspath(arguments.pairs)
    calLength(input_file,output_file,pairs)
    

#####################################################################

if __name__ == '__main__':
    main()
