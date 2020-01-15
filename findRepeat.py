'''
Created on Apr 19, 2017

@author: nanda
'''
from Bio import SeqIO
import argparse
import textwrap
import os
import operator
import multiprocessing
from multiprocessing import Process, Queue
import math
from collections import Counter


#####################################################################

def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Given the fasta file find the most frequent repeat of given length
    python ~/aTools/utilities/findRepeat.py -i test.fa -l 4 -n 8
    bsub -q long -n 8 -W 12:00 -R "span[hosts=1]" -R "rusage[mem=1024]" python ~/aTools/utilities/findRepeat.py -i Symbiodinium_microadriaticum-1.0.fa -l 7 -n 8
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_fasta_file' ,
                        help = "Input fasta file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-l" ,
                        metavar = 'repeat_length' ,
                        help = "repeat Length" ,
                        dest = "repeatLen",
                        required = True ,
                        type = int)
    
    parser.add_argument("-n" ,
                        metavar = 'num_of_cores' ,
                        help = "num of cores" ,
                        dest = "num",
                        required = True ,
                        type = int)
    
    
    return parser.parse_args()

#####################################################################
def batch_iterator(iterator, batch_size):
    """Returns lists of length batch_size.

    This can be used on any iterator, for example to batch up
    SeqRecord objects from Bio.SeqIO.parse(...), or to batch
    Alignment objects from Bio.AlignIO.parse(...), or simply
    lines from a file handle.

    This is a generator function, and it returns lists of the
    entries from the supplied iterator.  Each list will have
    batch_size entries, although the final list may be shorter.
    """
    entry = True  # Make sure we loop once
    while entry:
        batch = []
        while len(batch) < batch_size:
            try:
                entry = next(iterator)
            except StopIteration:
                entry = None
            if entry is None:
                # End of file
                break
            batch.append(entry)
        if batch:
            yield batch

def worker(num,repeatLen,fastaChunk):
    kmer=dict()
    for fastaSeq in fastaChunk:
        print("worker "+str(num)+" working on "+str(fastaSeq.id))
        s = fastaSeq.seq
        i=0
        j=repeatLen
        while(j<=len(s)):
            k=str(s)[i:j]
            if(k not in kmer.keys()):
                kmer[k]=1
            else:
                kmer[k]+=1
            i+=1
            j=i+repeatLen
        print("worker "+str(num)+" done with "+str(fastaSeq.id))
    return(kmer)


def filterRepeat(input_file,repeatLen,numCores):
    fastaParse = SeqIO.parse(open(input_file), "fasta")
    fastaParseLen = SeqIO.parse(open(input_file), "fasta")
    num_of_records=(len(SeqIO.to_dict(fastaParseLen)))
    dall = Counter()
    print("Total number of records " + str(num_of_records))
    if(num_of_records<=numCores):
        batchLen=1
    else:
        batchLen=int(num_of_records/numCores)+1
    pool=multiprocessing.Pool(processes=numCores)
    multiple_results = [pool.apply_async(worker, (i,repeatLen,batch,)) for i, batch in enumerate(batch_iterator(fastaParse, batchLen))]
    #print([res.get(timeout=1) for res in multiple_results])
    for res in multiple_results:
        dall+=Counter(res.get())
    pool.close()
    pool.join()
    #print(dall)
    print("Most frequent repeat of length "+str(repeatLen)+" = " + str(dall.most_common(1)))
   

#####################################################################


def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    repeatLen=int(arguments.repeatLen)
    numCores=int(arguments.num)
    filterRepeat(input_file,repeatLen,numCores)
    

#####################################################################

if __name__ == '__main__':
    main()
