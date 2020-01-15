'''
Created on Jul 24, 2018

@author: nanda
'''

import argparse
import textwrap
import os
from _collections import defaultdict

#####################################################################
def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Create a bed from intermediate bed file 
    python ~/aTools/utilities/finalBedfile.py -i bed1kbremovedsingCorrectListHang4NMPos-40kb -o dinobedfile.bed
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_bed_intermediate file' ,
                        help = "input_bed_intermediate file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    
    parser.add_argument("-o" ,
                        metavar = 'output_bed file' ,
                        help = "output_bed file" ,
                        dest = "output",
                        required = True ,
                        type = str)

    return parser.parse_args()

########################################################
def createList(input_file, output_file):
    with open(input_file) as inFH, open(output_file, "w") as outFH:
        for line in inFH:
            line=line.rstrip("\n")
            v=line.split("\t")
            c=v[1].split("__")
            if(v[2]=="plus"):
                tmp="+"
            else:
                tmp="-"
            outFH.write(c[0]+"\t"+c[1]+"\t"+c[2]+"\t"+v[0]+"\t"+str(0)+"\t"+tmp+"\n")

#######################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    output_file = os.path.abspath(arguments.output)

    createList(input_file, output_file)


#####################################################################
if __name__ == '__main__':
    main()
    