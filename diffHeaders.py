'''
Created on Jun 25, 2017

@author: nanda
'''
import argparse
import textwrap
import os
import gzip
from Bio import SeqIO
from _collections import defaultdict

#####################################################################
def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Make a new scaffold list based on removed bins. 
    header1 should be dino rearranged
    python  ~/aTools/utilities/diffHeaders.py -i1 Dino-HiC-D7plus-Comb8.header -i2 rearrangedMatrix.header -o headerDiff
    python  ~/aTools/utilities/diffHeaders.py -i1 more -i2 less -o headerDiff
    ''') )

    parser.add_argument("-i1" ,
                        metavar = 'input_header1_file' ,
                        help = "input header1 file" ,
                        dest = "input1",
                        required = True ,
                        type = str)

    parser.add_argument("-i2" ,
                        metavar = 'input_header2_file' ,
                        help = "input header2 file" ,
                        dest = "input2",
                        required = True ,
                        type = str)
    
    parser.add_argument("-o" ,
                        metavar = 'output_difference_file' ,
                        help = "output difference file" ,
                        dest = "output",
                        required = True ,
                        type = str)

    return parser.parse_args()

#####################################################################
def createList(input_file1, input_file2, output_file):
    with open(input_file1) as inFH1, open(input_file2) as inFH2, open(output_file, "w") as outFH:
        header1 = []
        header2 = []
        for line in inFH1:
            line=line.rstrip("\n")
            line=line.rstrip()
            header1.append(line)
            
        for line in inFH2:
            line=line.rstrip("\n")
            line=line.rstrip()
            header2.append(line)
        
        for i in header1:
            if i not in header2:
                outFH.write(i)
                outFH.write("\n")
            
        

            
#####################################################################

def main():
    arguments = get_arguments()
    input_file1 = os.path.abspath(arguments.input1)
    input_file2 = os.path.abspath(arguments.input2)
    output_file = os.path.abspath(arguments.output)

    createList(input_file1, input_file2, output_file)


#####################################################################
if __name__ == '__main__':
    main()
