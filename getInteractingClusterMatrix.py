'''
Created on Feb 5, 2019

@author: nanda
'''
import argparse
import textwrap
import os
from _collections import defaultdict
import numpy as np
from numpy import nan, array

#####################################################################
def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Find to which chr clusters of 95 interacts most. 
    python ~/aTools/utilities/getInteractingClusterMatrix.py -i Dplus-20kb.matrix-iced.matrix -f 20kbHeaders-iced
    ''') )

    
    parser.add_argument("-i" ,
                        metavar = 'Matrix file' ,
                        help = "Matrix file" ,
                        dest = "matrix",
                        required = True ,
                        type = str)
    
    parser.add_argument("-f" ,
                        metavar = 'Headers File' ,
                        help = "less Dplus-20kb.matrix-iced.matrix | cut -f 1 > 20kbHeaders-iced" ,
                        dest = "headers",
                        required = True ,
                        type = str)
    

    return parser.parse_args()

#####################################################################
def magic(matrix_file,headers_file):
    headersDict=defaultdict(list)
    with open(matrix_file, "r") as matrixFH, open(headers_file, "r") as headFH, open("chr-clusters95-interactionList", "w") as intFH:
        for line in headFH:
            h=line.rstrip("\n")
            hIndex = h.split("|")
            ch=hIndex[2].split(":")
            headersDict[ch[0]].append(int(hIndex[0])+1)
            
        clusterLine=[]
        c=0
        for line in matrixFH:
            line=line.rstrip("\n")
            if(c>0):
                mLine = line.split("\t")
                mH1=mLine[0].split("|")[2]
                mH=mH1.split(":")[0]
                
                if "chr" in mH:
                    continue
                else:
                    if not (len(clusterLine)+1==len(headersDict[mH])):
                        clusterLine.append(line)
                    else:
                        clusterLine.append(line)
                        clInt=[]
                        for keys in headersDict:
                            if "chr" in keys:
                                sortedIndChr=sorted(headersDict[keys])
                                sumChr=0
                                for values in clusterLine:
                                    v=values.split("\t")
                                    results = array(map(float, v[int(sortedIndChr[0]):int(sortedIndChr[-1])+1]))
                                    denom=(len(results))
                                    results[np.isnan(results)] = 0
                                    sumChr+=(sum(results)/denom)
                                clInt.append([keys,sumChr])
                        maxInt=max(clInt, key=lambda x:x[1])
                        #print("\t".join([mH, maxInt[0],str(maxInt[1])]))
                        intFH.write("\t".join([mH, maxInt[0],str(maxInt[1])]))
                        intFH.write("\n")
                        clusterLine=[]
                        
            else:
                c+=1
                
        
        
    


#####################################################################

def main():
    arguments = get_arguments()
    matrix_file = os.path.abspath(arguments.matrix)
    headers_file = os.path.abspath(arguments.headers)

    magic(matrix_file,headers_file)
    


#####################################################################
if __name__ == '__main__':
    main()