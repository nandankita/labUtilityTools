'''
Created on Jul 18, 2017

@author: nanda
'''
import argparse
import textwrap
import os
import gzip
from itertools import count
from collections import defaultdict
from functools import partial
from Bio import SeqIO
import re

#####################################################################


def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    split fasta file into given subscaffolds
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_fasta_file' ,
                        help = "Input fasta file" ,
                        dest = "input",
                        required = True ,
                        type = str)
      
    parser.add_argument("-o" ,
                        metavar = 'output_fasta_file_name' ,
                        help = "Input fasta file name" ,
                        dest = "output",
                        required = True ,
                        type = str)
    
    parser.add_argument("-s" ,
                        metavar = 'scaffoldList' ,
                        help = "scaffoldList" ,
                        dest = "scaffold",
                        required = True ,
                        type = str)
    

    return parser.parse_args()

#####################################################################

def collapseMatrix(input_file,output_file, scFile):
    scList = defaultdict(list)
    with open (input_file, "r") as inFasta, open (scFile, "r") as inScList, open(output_file, "w") as outFasta:
        for line in inScList:
            line=line.rstrip("\n")
            v = line.split("\t")
            scList[v[0]].append(v[1])
            
        fastaParse = SeqIO.parse(inFasta,"fasta")
        for fastaSeq in fastaParse:
            s = fastaSeq.seq
            idFasta = fastaSeq.id
            regex_txt=r""+idFasta+"\D"
            for key, value in scList.items():
                if re.match(regex_txt, key) is not None:
                    cord=value[0].split("-")
                    stCord=int(cord[0])-1
                    if(int(cord[0])==0):
                        stCord=int(cord[0])
                    enCord=int(cord[1])
                    subSeq=s[stCord:enCord]
                    print(key,len(subSeq))
                    outFasta.write(">"+key+"\n")
                    outFasta.write(str(subSeq)) 
                    outFasta.write("\n")   
    
#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    output_file = os.path.abspath(arguments.output)
    scaffold = arguments.scaffold
    
    collapseMatrix(input_file,output_file,scaffold)


#####################################################################
if __name__ == '__main__':
    main()

