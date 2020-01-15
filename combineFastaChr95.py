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

from scipy.interpolate import interp1d



#####################################################################

def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    It will add remaining scaffolds to the fasta file
    cp /nl/umw_job_dekker/users/an27w/dinoflagellets/analysis/fixesAfter60per/trial5/dino-v1.0-t5.fa .
    python ~/aTools/utilities/combineFastaChr95.py -i filteredGe9999.fa  -k dino-v1.0-t5.fa -n chr95-scaffold-clusters
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
    orderDictSc=OrderedDict()
    with open(input_file) as FASTAIN, open(append_file, "a") as APP, open(order) as ORD:
        fastaParse = SeqIO.parse(FASTAIN,"fasta")
        fastaOutDict=defaultdict(list)
        for fastaSeq in fastaParse:
            s = str(fastaSeq.seq)
            idFasta = fastaSeq.id
            fastaInDict[idFasta]=s
        
        keyMap={"Smic.scaffold9__1420062__1920061":"Smic.scaffold9__1420062__2138115",
                "Smic.scaffold236__1__500000":"Smic.scaffold236__1__795886",
                "Smic.scaffold338__1__500000":"Smic.scaffold338__1__646490",
                "Smic.scaffold458__1__500000":"Smic.scaffold458__1__544999"
                }
        
        for line in ORD:
            line=line.rstrip("\n")
            val=line.split("\t")

            k=val[0]
            if(k in keyMap):
                k=keyMap[k]
                seq= fastaInDict[k][0:500000]
            else:
                seq= fastaInDict[k]
            
            fastaOutDict[val[1]].append(seq)
            orderDictSc[val[1]]=len(seq)
        
        for keys in orderDictSc.keys():
            chrom="cluster"+keys
            print("Writing Chromosome "+str(chrom))
            APP.write(">"+chrom+"\n")
            APP.write("".join(fastaOutDict[keys]))
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
