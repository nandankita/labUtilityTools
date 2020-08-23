'''
Created on Jan 17, 2020

@author: nanda
'''
'''
Created on Apr 19, 2017

@author: nanda
'''
from Bio import SeqIO
import argparse
import textwrap
import os


#####################################################################

def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Filter the fasta file by id
    
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_fasta_file' ,
                        help = "Input fasta file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-f" ,
                        metavar = 'filter_length' ,
                        help = "Filter Length" ,
                        dest = "filterLen",
                        required = True ,
                        type = int)
    
    
    return parser.parse_args()

#####################################################################
def filterFasta(input_file,filterLen):
    output_file="filteredGe"+str(filterLen)+".fa"
    countTotalbpO=0
    countTotalbpF=0
    with open(input_file) as FASTAIN, open(output_file,"w") as OUTFH:
        fastaParse = SeqIO.parse(FASTAIN,"fasta")
        for fastaSeq in fastaParse:
            s = fastaSeq.seq
            idFasta = fastaSeq.id
            countTotalbpO += len(s)
            if(len(s)>filterLen):
                countTotalbpF += len(s)
                OUTFH.write(">"+str(idFasta)+"\n")
                OUTFH.write(str(s))
                OUTFH.write("\n")
    print("Total Number of bp in original file ", countTotalbpO)
    print("Total Number of bp in filtered file ", countTotalbpF)

#####################################################################


def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    filterLen=int(arguments.filterLen)
    filterFasta(input_file,filterLen)
    

#####################################################################

if __name__ == '__main__':
    main()
