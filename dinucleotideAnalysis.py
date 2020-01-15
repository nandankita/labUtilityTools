'''
Created on Sep 29, 2019

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
    calculate GC content within a window and step
    bsub -q short -n 1 -W 4:00 -R "span[hosts=1]" -R "rusage[mem=40000]" python /home/an27w/aTools/fasta_tools/gc_content.py -i /nl/umw_job_dekker/users/an27w/sing-distiller/chromosome-missing-scaffolds/results/coolers_library_group/arrangeScaffolds/dino-missingClusters95.fa -w 80000 -s 5000
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_fasta_file' ,
                        help = "Input fasta file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    parser.add_argument("-w" ,
                        metavar = 'Window size' ,
                        help = "Window size'" ,
                        dest = "window",
                        required = True ,
                        type = str)
    parser.add_argument("-s" ,
                        metavar = 'step size' ,
                        help = "step size" ,
                        dest = "step",
                        required = True ,
                        type = str)
    

    return parser.parse_args()

#####################################################################
def GC(seq):
    gc = sum(seq.count(x) for x in ['G', 'C', 'g', 'c']) 
    ns = sum(seq.count(x) for x in ['N', 'n']) 
    try:
        return gc * 100.0 / (len(seq)-ns)
    except ZeroDivisionError:
        return 0.0 
#####################################################################

def calculate_dinuc(input_file,window,step):
    outFile="GC_content"+str(window)+".txt"
    with open (input_file, "r") as inFasta, open(outFile, "w") as gcFile:
        gcFile.write("\t".join(["id","start","end","mid-point","GC%"]))
        gcFile.write("\n")
        fastaParse = SeqIO.parse(inFasta,"fasta")
        for fastaSeq in fastaParse:
            s = fastaSeq.seq
            idFasta = fastaSeq.id
            lenSeq=len(s)
            start=1
            end=window+1
            while(end<=lenSeq):
                #print(start,end,step)
                chunkSeq=s[start:end]
                #print(len(chunkSeq))
                mid=(start+end-1)/2
                gcSeq=GC(chunkSeq)
                gcFile.write("\t".join([idFasta,str(start),str(end-1),str(mid),str(gcSeq)]))
                gcFile.write("\n")
                start+=step
                end+=step
            
        
    
#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    window = int(arguments.window)
    step = int(arguments.step)
    
    calculate_dinuc(input_file,window,step)


#####################################################################
if __name__ == '__main__':
    main()