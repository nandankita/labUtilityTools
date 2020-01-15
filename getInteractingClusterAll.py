'''
Created on May 18, 2018

@author: nanda
'''
import argparse
import textwrap
import os
import gzip
from _collections import defaultdict

#####################################################################
def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Find to which cluster this 40kb bin/line interacts most
    python ~/aTools/utilities/getInteractingClusterAll.py -i selectedOrderWithLines.txt -m afterLineAssembRearranged.matrix
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_bin-cluster_order_file' ,
                        help = "input_bin-cluster_order_file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-m" ,
                        metavar = 'Matrix file' ,
                        help = "Matrix file" ,
                        dest = "matrix",
                        required = True ,
                        type = str)
    
#     parser.add_argument("-l" ,
#                         metavar = 'line number assuming matrix has no top header' ,
#                         help = "line number assuming matrix has no top header" ,
#                         dest = "line",
#                         required = True ,
#                         type = str)

    return parser.parse_args()

#####################################################################
def magic(clustHeaders, matrixDictLine):
    mSum=0
    mKey="Can't say NA"
    for keys, values in clustHeaders.items():
        v = [ 0 if matrixDictLine[x]=="NA" else float(matrixDictLine[x]) for x in values]
        if(sum(v)>mSum):
            mSum=sum(v)
            mKey=keys
    return(mKey)

def correctCluster(input_file, matrix_file):
    clusterCount=1
    clustHeaders=defaultdict(list)
    cList=[]
    matrixDict=defaultdict(list)
    with open(input_file, "r") as clusFH, open(matrix_file, "r") as matrixFH, open("NewSelectedOrderFile", "w") as newFH:
        for c in clusFH:
            c=c.rstrip("\n")
            cList.append(c)
            sC = c.split("\t")
            cNum=sC[1]
            clustHeaders[cNum].append(clusterCount)
            clusterCount +=1
        print("Wrote cluster")
        count = 0
        for line in matrixFH:
            line=line.rstrip("\n")
            line=line.rstrip()
            interactions=line.split("\t")
            matrixDict[count]=interactions
            count+=1
        print(len(matrixDict[1]))
        print("Wrote Matrix")
        n=1
        for c in cList:
            sC = c.split("\t")
            cBin=sC[0]
            matrixDict[n][n]=0
            cNum=magic(clustHeaders, matrixDict[n])
            if(cNum=="Can't say NA"):
                cNum=sC[1]
            n+=1
            newFH.write(cBin+"\t"+str(cNum)+"\n")
        print("done")
            
#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    matrix_file = os.path.abspath(arguments.matrix)
    #line = int(arguments.line)

    correctCluster(input_file, matrix_file)


#####################################################################
if __name__ == '__main__':
    main()