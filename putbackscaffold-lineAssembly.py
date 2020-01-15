'''
Created on Dec 6, 2017

@author: nanda
'''
import argparse
import textwrap
import os
from _collections import defaultdict
import numpy as np


#####################################################################


def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    put back lines with adjacent scaffolds if it is available.
    python ~/aTools/utilities/putbackscaffold-lineAssembly.py -i selectedOrder65 -o selectedOrder65-new
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_order_file' ,
                        help = "Input order file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-o" ,
                        metavar = 'output_file' ,
                        help = "output file" ,
                        dest = "output",
                        required = True ,
                        type = str)
    

    
    return parser.parse_args()

#####################################################################

def putback(input_file, output_file):
    scList=[]
    lineList=[]
    lineNotAddedList=[]
    with open(input_file) as INP,  open(output_file,"w") as OUT:
        for line in INP:
            line=line.rstrip("\n")
            if(line.startswith("Smic")):
                scList.append(line)
            else:
                lineList.append(line)
        for bin in lineList:
            diffDict=defaultdict(list)
            v=bin.split("__")
            lSt=int(v[1])
            s=v[0].split(".")
            matching = [a for a in scList if "Smic."+s[2]+"__" in a]
            diffList=[]
            series=[]
            for m in matching:
                c=m.split("__")
                sEnd=int(c[2])
                diff=lSt-sEnd
                diffDict[diff]=scList.index(m)
                diffList.append(diff)
                series.append(int(c[1]))
            if(len(diffList)>0):
                desDiff=min(diffList, key=lambda x:abs(x-1))
                indx=diffDict[desDiff]
                k=diffList.index(desDiff)
                if(k!=0):
                    indx+=1
                    
#                 maxDiff=max(diffList, key=lambda x:abs(x-1))
#                 maxIndx=diffDict[maxDiff]
#                 indx+=1
#                 print(bin,indx,maxIndx)
#                 if(maxIndx<indx):
#                     indx+=1
#                 if(desDiff>1):
#                     indx+=1
#                 elif(desDiff==1):
#                     del(diffList[diffList.index(desDiff)])
#                     desDiff2=min(diffList, key=lambda x:abs(x-1))
#                     indx2=diffDict[desDiff2]
#                     print(bin,scList[indx],scList[indx2],indx,indx2)
#                     if(int(scList[indx].split("__")[1])>int(scList[indx2].split("__")[1])):
#                         indx+=1
                scList.insert(indx,bin)
            else:
                lineNotAddedList.append(bin)
        tot=scList+lineNotAddedList
        for t in tot:
            OUT.write(t+"\n")

#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    output_file = os.path.abspath(arguments.output)
    
    putback(input_file, output_file)


#####################################################################
if __name__ == '__main__':
    main()

