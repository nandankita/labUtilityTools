'''
Created on Jun 12, 2017

@author: nanda
'''
import argparse
import textwrap
import os
import gzip
from Bio import SeqIO

#####################################################################

def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    split a fastq.gz file into multiple 
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_fastq_gz_file' ,
                        help = "Input fastq gz file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-n" ,
                        metavar = 'number_of_reads_in_one_file' ,
                        help = "number of reads in one file" ,
                        dest = "reads",
                        required = True ,
                        type = str)

    return parser.parse_args()

#####################################################################
def splitFiles(input_file, reads,input_file_name):
    record_iter = SeqIO.parse(gzip.open(input_file),"fastq")
    output_file=input_file_name.split("_")
    countWritten=0
    i=1
    entry = True
    while(entry):
        try:
            entry = record_iter.next()
        except StopIteration:
            entry = None
        if entry is None:
            # End of file
            break
        if(countWritten%reads == 0):
            filename=output_file[0]+"_"+str(i)+"_"+str("_".join(output_file[1:len(output_file)]))
            FH=gzip.open(filename, "wt") 
            i+=1
        SeqIO.write(entry,FH,"fastq")
        countWritten+=1
    
#     countWritten = 0 
#     with 
#     while(i<=)
#     
#     
#     for i, batch in enumerate(batch_iterator(record_iter, reads)):
#         #print(output_file)
#         filename=output_file[0]+"_"+str(i + 1)+"_"+str("_".join(output_file[1:len(output_file)]))
#         with gzip.open(filename, "wt") as handle:
#             count = SeqIO.write(batch, handle, "fastq")
        
        # print("Wrote %i records to %s" % (count, filename))



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
                entry = iterator.next()
            except StopIteration:
                entry = None
            if entry is None:
                # End of file
                break
            batch.append(entry)
        if batch:
            yield batch
    



#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    input_file_name=str((arguments.input))
    reads =int(arguments.reads)
    
    splitFiles(input_file, reads,input_file_name)


#####################################################################
if __name__ == '__main__':
    main()
    