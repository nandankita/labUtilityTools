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
import UserString
from UserString import MutableString

#####################################################################

def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Given a Fasta file and order file, it creates a new fasta file based on that order.
    python ~/aTools/fasta_tools/createFastaforDinoRemove1kbBins.py -i dino-2.0.fa -n unselectedIndexLocation1kb
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_fasta_file' ,
                        help = "Input fasta file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-n" ,
                        metavar = 'Bins to be removed file.' ,
                        help = "Bins to be removed file." ,
                        dest = "order",
                        required = True ,
                        type = str)
    
    
    return parser.parse_args()
#####################################################################
def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


#####################################################################
def createFasta(input_file,order):
    output_file="dino-genome-final.fa"
    fastaInDict=dict()
    fastaOutDict=defaultdict()
    removeLs = defaultdict(list)
    with open(input_file) as FASTAIN, open(order) as ORD, open(output_file, "w") as OUTFH:
        fastaParse = SeqIO.parse(FASTAIN,"fasta")
        for fastaSeq in fastaParse:
            s = str(fastaSeq.seq)
            idFasta = fastaSeq.id
            fastaInDict[idFasta]=s
        print("Read input fasta done")
        for line in ORD:
            line=line.rstrip("\n")
            val=line.split(":")
            removeLs[val[0]].append(val[1])
            
        for k,v in removeLs.items():
            seq=MutableString(fastaInDict[k])
            for i in list(reversed(v)):
                loc=i.split("-")
                start=int(loc[0])-1
                end=int(loc[1])
                del seq[start:end]
#                 print(start,end)
#             print(k,len(fastaInDict[k]),len(seq))
            fastaOutDict[k]=seq
            
        z = merge_two_dicts(fastaInDict, fastaOutDict)
        
        #for keys in sorted(fastaOutDict.iterkeys(),key= lambda x: int(x.strip('chr'))):
        for keys in sorted(z.iterkeys(),key= lambda x: int(x.strip('Smic.scaffold'))):
            print("Writing Chromosome "+keys)
            chrom=keys
            seqVal=z[keys]
            OUTFH.write(">"+chrom+"\n")
            OUTFH.write(str(seqVal))
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
