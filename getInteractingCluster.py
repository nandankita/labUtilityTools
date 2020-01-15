'''
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
    python ~/aTools/utilities/getInteractingCluster.py -i selectedOrderWithLines.txt -m afterLineAssembRearranged.matrix -l 1
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
    
    parser.add_argument("-l" ,
                        metavar = 'line number assuming matrix has no top header' ,
                        help = "line number assuming matrix has no top header" ,
                        dest = "line",
                        required = True ,
                        type = str)

    return parser.parse_args()

#####################################################################
def magic(input_file, matrix_file, lineNo):
    clustHeaders=defaultdict(list)
    mSum=0
    mKey="Can't say NA"
    count = 0
    clusterCount=1
    with open(matrix_file, "r") as matrixFH, open(input_file, "r") as clusFH:
        for c in clusFH:
            c=c.rstrip("\n")
            sC = c.split("\t")
            cNum=sC[1]
            clustHeaders[cNum].append(clusterCount)
            clusterCount +=1
        for line in matrixFH:
            line=line.rstrip("\n")
            line=line.rstrip()
            if(count == lineNo):
                interactions=line.split("\t")
                for keys, values in clustHeaders.items():
                    v = [ 0 if interactions[x]=="NA" else float(interactions[x]) for x in values]
                    if(sum(v)>mSum):
                        mSum=sum(v)
                        mKey=keys
                print(interactions[0] + " Max interaction sum cluster is "+str(mKey)+" with interaction sum "+str(mSum))
                break
            count+=1
            
#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    matrix_file = os.path.abspath(arguments.matrix)
    line = int(arguments.line)

    magic(input_file, matrix_file, line)


#####################################################################
if __name__ == '__main__':
    main()