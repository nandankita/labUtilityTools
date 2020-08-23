'''
Created on Jan 8, 2019

@author: nanda
'''
import argparse
import textwrap
import os
import gzip
from _collections import defaultdict
import operator

#####################################################################
def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Find to how to arrange a cluster,
    Find most interacting bin in a chr
    
    python ~/aTools/utilities/arrangeCluster.py -m test.matrix 
    ''') )

    parser.add_argument("-m" ,
                        metavar = 'Matrix file' ,
                        help = "Matrix file" ,
                        dest = "matrix",
                        required = True ,
                        type = str)
 
    return parser.parse_args()

#####################################################################
def magicArrange(matrix_file):
    #count = 573
    count = 0
    headerList=[]
    rearrangedList=[]
    headerRow = []
    movedHeader=[]
    with open(matrix_file, "r") as matrixFH, open("out-header", "w") as clusFH:
        for line in matrixFH:
            line=line.rstrip("\n")
            interactions=line.split("\t")
            
            Z=[]
            
            if(count==0):
                rearrangedList=list(range(len(interactions[1:])))
                
                for rowIndx in interactions[1:]:
                    row=rowIndx.split("|")[2]
                    headerRow.append(row)
            else:
                headerColumn=interactions[0].split("|")[2]
                headerList.append(headerColumn)
                del interactions[0]
                
                if(count<=len(interactions)):
                    interactions[count-1]=0
                
                for i in rearrangedList:
                    Z.append(interactions[i])

                
                
                index, rowMost = max(enumerate([float(i) for i in Z[0:]]), key=operator.itemgetter(1))
                print(index, rowMost)
                print(rearrangedList)
                print(count)
                print(movedHeader)
                if(rowMost != 0) and (count not in movedHeader):
                    copy=rearrangedList[count-1]
                    cIndex=rearrangedList.index(copy)
                    rearrangedList.remove(copy)
                    if(cIndex>=index):                    
                        rearrangedList.insert(index,copy)
                    else:
                        rearrangedList.insert(index-1,copy)
                    
                    movedHeader.append(index)
                    print(rearrangedList)
                    
            count+=1    
        
        for i in rearrangedList:
            clusFH.write(headerRow[i]+"\n")
            

            
#####################################################################

def main():
    arguments = get_arguments()
    matrix_file = os.path.abspath(arguments.matrix)

    magicArrange(matrix_file)


#####################################################################
if __name__ == '__main__':
    main()