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
    python ~/aTools/utilities/sumMatrixWindow.py -i Dino-HiC-Dplus_chr23_1000_dino_iced.matrix.gz -n 20
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_tab_matrix_file' ,
                        help = "Input tab matrix file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    parser.add_argument("-n" ,
                        metavar = 'window_size' ,
                        help = "number of bins to be avoided around diagonal" ,
                        dest = "block",
                        required = True ,
                        type = str)

    return parser.parse_args()

#####################################################################
def sumMatrix(input_file,windowSize):
    count = 0
    lnNum=0
    n=input_file.split("/")[-1].split("_")
    c=n[1]
    with gzip.open(input_file, "r") as MATRIXFH, open("sumMatrix"+c, "w") as sumFH:
        for line in MATRIXFH:
            line=line.rstrip("\n")
            line=line.rstrip()
            if(count == 0):
                count+=1
            else:
                lnNum+=1
                interactions=line.split("\t")
                itself=interactions[lnNum]
                diagonal=lnNum
#                 for i in range(1, len(interactions)):
#                     sumLine+=float(interactions[i])
                if(itself=='nan'):
                    sumLine='nan'
                else:
                    interactions1 = map(float, interactions[1:len(interactions)])
                    interactionsN=np.nan_to_num(interactions1)
                    sumLine=0.0
                    left=(sum(interactionsN[:(diagonal-windowSize-1)]))
                    right=(sum(interactionsN[(diagonal+windowSize):]))
                    if((diagonal-windowSize)<=0):
                        left=0
                    if((diagonal+windowSize)>len(interactionsN)):
                        right=0
                    sumLine=left+right
                sumFH.write(str(interactions[0])+"\t"+str(sumLine))
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
    