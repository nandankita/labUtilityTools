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
    It will add remaining scaffolds to the fasta file
    python ~/aTools/fasta_tools/combineFastaAllforDino.py -i Symbiodinium_microadriaticum.fa  -k Symbiodinium_microadriaticum-1.0.fa -n mergedtotalMissingBinsth300lt40kb 
    python ~/aTools/fasta_tools/combineFastaAllforDino.py -i Symbiodinium_microadriaticum.fa  -k Symbiodinium_microadriaticum-1.0.fa -n removedBins300headergt80kb
    python ~/aTools/fasta_tools/combineFastaAllforDino.py -i Symbiodinium_microadriaticum.fa -k dino-v1.0-missingBins.fa -n sortedMissingScaffolds
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_fasta_file' ,
                        help = "Input fasta file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-k" ,
                        metavar = 'fasta_file_to_append' ,
                        help = "fasta file append" ,
                        dest = "append",
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
def createFasta(input_file,append_file,order):
    fastaInDict=dict()
    seq=OrderedDict()
    
    with open(input_file) as FASTAIN, open(append_file, "a") as APP, open(order) as ORD:
        fastaParse = SeqIO.parse(FASTAIN,"fasta")
        for fastaSeq in fastaParse:
            s = str(fastaSeq.seq)
            idFasta = fastaSeq.id
            fastaInDict[idFasta]=s
        for line in ORD:
            line=line.rstrip("\n")
            v=line.split("\t")
            val=v[0].split("__")
            start=int(val[1])-1
            end=int(val[2])
            k=val[0]
            chrom=v[1]
            if chrom in seq:
                seq[chrom].append(fastaInDict[k][start:end])
            else:
                seq[chrom]=[]
                seq[chrom].append(fastaInDict[k][start:end])
        for k,v in seq.items():
            print("Writing Chromosome"+str(k))
            APP.write(">"+k+"\n")
            APP.write("".join(v))
            APP.write("\n")
            

#####################################################################


def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    append_file= os.path.abspath(arguments.append)
    order = os.path.abspath(arguments.order)
    createFasta(input_file,append_file,order)
    

#####################################################################

if __name__ == '__main__':
    main()
