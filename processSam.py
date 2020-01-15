'''
Created on Feb 21, 2017

@author: nanda
'''

import argparse
import textwrap
import os
import pysam
import re
from _collections import defaultdict

#####################################################################


def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Read Sam file and give logistic info
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_sam_file' ,
                        help = "Input sam file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-o" ,
                        metavar = 'output_report_file' ,
                        help = "Output report file" ,
                        dest = "output",
                        required = False,
                        default = "samReport.txt",
                        type = str)
    
    parser.add_argument("-t" ,
                        metavar = 'total_reads_fastq' ,
                        help = "Total Number of reads from your fastq file" ,
                        dest = "fastqReads",
                        required = False,
                        default = 0,
                        type = str)
    

    return parser.parse_args()

#####################################################################

def processSam(input_file, output_file, fastq_reads):
    samInFH = pysam.AlignmentFile(input_file)
    samOutFH = open(output_file, 'w')
    countMapped = 0
    countUnmapped = 0
    listMapped = []
    coverageCount = {}
    samEntry = defaultdict(list)
    readRefDict = defaultdict(list)
    for r in samInFH.fetch(until_eof=True):
        if r.is_unmapped:
            countUnmapped +=1
        else:
            print(r)
            listMapped.append(r.query_name)
            position = r.get_reference_positions()
            print(position)
            if (r.reference_name not in readRefDict[r.query_name] and r.mapping_quality>30):
            	readRefDict[r.query_name].append(r.reference_name)
            	writeList = [r.query_name, r.reference_name, str(position[0]), str(position[-1]), str(r.mapping_quality)]
            	w = ",".join(writeList)
            	samEntry[r.query_name].append(w)
            	if (r.reference_name) in coverageCount:
                	coverageCount[r.reference_name] +=1
            	else:
                	coverageCount[r.reference_name] = 1
            	countMapped +=1
    
    
    
    listMultiMapped,listUniqueMapped = countMulti(listMapped)
    
    samInFH.close()
    
    samOutFH.write("Total reads in pacbio fastq\t"+ str(fastq_reads) +"\n")
    samOutFH.write("Count Mapped\t"+ str(countMapped) +"\n")
    samOutFH.write("Count Unmapped\t" + str(countUnmapped) +"\n")
    samOutFH.write("Uniquely Mapped\t" + str(len(listUniqueMapped)) + "\n")
    samOutFH.write("Multi Mapped\t" + str(len(listMultiMapped)) +"\n")
    #samOutFH.write("Coverage to each contig\n"+ str(coverageCount) + "\n")
    
    samOutFH.write("Read Name,Contig Name,Pos start,Pos End\n")
    print("Number of reads mapped to multiple contigs and mapq>30: ",len(samEntry))  
    for key, value in samEntry.items():
        if (len(value)>1):
            for v in value:
                samOutFH.write(str(v)+"\n")
    
    print("Done")
    samOutFH.close()

#####################################################################
def countMulti(L):
    seen = set()
    seen2 = set()
    seen_add = seen.add
    seen2_add = seen2.add
    for item in L:
        if item in seen:
            seen2_add(item)
        else:
            seen_add(item)
    unique = seen - seen2
    return list(seen2),list(unique)



#####################################################################


def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    output_file = os.path.abspath(arguments.output)
    fastq_reads = int(arguments.fastqReads)
    processSam(input_file,output_file, fastq_reads)


#####################################################################
if __name__ == '__main__':
    main()

