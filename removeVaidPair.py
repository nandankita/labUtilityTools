'''
Created on Apr 10, 2017

@author: nanda
'''

import argparse
import textwrap
import os
import gzip

#####################################################################


def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Count Number of interactions in a given matrix
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_gz_validpair_file' ,
                        help = "Input gzipped tab file" ,
                        dest = "input",
                        required = True ,
                        type = str)

    return parser.parse_args()

#####################################################################
def countInteractions(input_file):
    totalInteractions = 0
    count=0
    with gzip.open(input_file, "rt") as MATRIXFH:
        for line in MATRIXFH:
            if(count>9):
                line = line.rstrip("\n")
                values=line.split("\t")
                value0 = [0 if x=="nan" else x for x in values]
                totalInteractions += sum(list(map(float, value0[1:len(value0)])))
            count+=1
    print("Total number of interactions in "+str(input_file)+" is "+str(totalInteractions))
   
#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    
    countInteractions(input_file)


#####################################################################
if __name__ == '__main__':
    main()
    