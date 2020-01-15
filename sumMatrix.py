'''
Created on May 12, 2017

@author: nanda
'''

import argparse
import textwrap
import os
import gzip
import numpy as np


#####################################################################



def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    sum the rows in a given matrix excluding a block
     python ~/aTools/utilities/sumMatrix.py -i Dino-HiC-Dplus_chr25_1000_dino_iced.matrix.gz -n 40
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_tab_matrix_file' ,
                        help = "Input tab matrix file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    parser.add_argument("-n" ,
                        metavar = 'block_size' ,
                        help = "block to be avoided e.g. 40 for 40kb" ,
                        dest = "block",
                        required = True ,
                        type = str)

    return parser.parse_args()

#####################################################################
def sumMatrix(input_file,blockSize):
    count = 0
    lnNum=0
    with gzip.open(input_file, "r") as MATRIXFH, open("sumMatrix", "w") as sumFH:
        for line in MATRIXFH:
            line=line.rstrip("\n")
            line=line.rstrip()
            if(count == 0):
                count+=1
            else:
                block=(lnNum/blockSize)
                block+=1
                lnNum+=1
                interactions=line.split("\t")
                itself=interactions[lnNum]
#                 for i in range(1, len(interactions)):
#                     sumLine+=float(interactions[i])
                if(itself=='nan'):
                    sumLine='nan'
                else:
                    interactions = map(float, interactions[1:len(interactions)])
                    interactionsN=np.nan_to_num(interactions)
                    sumLine=0.0
                    left=(sum(interactionsN[:(block-1)*blockSize]))
                    right=(sum(interactionsN[(block)*blockSize:]))
                    sumLine=left+right
                sumFH.write(str(sumLine))
                sumFH.write("\n")
                        
   
#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    blockSize = int(arguments.block)
    
    sumMatrix(input_file,blockSize)


#####################################################################
if __name__ == '__main__':
    main()
    