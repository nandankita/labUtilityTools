'''
Created on Mar 30, 2019

@author: nanda
'''
import sys
import numpy as np
import pandas
import argparse
import textwrap
import os
from scalingPlotDomainsWrapper import calDominas

#####################################################################
def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Given a gap Estimate list and domains file write new scaling data per row
    python ~/aTools/utilities/createNewScalingData.py -i scalingShift.txt -d domains 
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_gap_estimate' ,
                        help = "Input gap_estimate file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-d" ,
                        metavar = 'domains list' ,
                        help = "domains_list" ,
                        dest = "domains",
                        required = True ,
                        type = str)
    
    
    return parser.parse_args()

#####################################################################
def writeNewScaling(input_file, domains_file):
    domains=calDominas(domains_file)
    gapValues=pandas.read_csv(input_file, sep='\t',header=None, skiprows=[0])
    
    for chromKey,domainValue in domains.items():
        st=len(domainValue)
        end=len(domainValue)+1
        for i in range(1,st):
            endV=i
            for j in range(2,end):
                domainFileName="scaling_data."+chromKey+"-row"+str(i)+"-domain"+str(j)+".matrix"
                print(domainFileName)
                with open(domainFileName, "r") as oldSCFH, open("new_"+domainFileName, "w") as newSCFH:
                    for line in oldSCFH:
                        line=line.rstrip("\n")
                        indV=line.split("\t")
                        startRange=(np.where(gapValues[0] == chromKey+"-row"+str(i))[0][0])
                        
                        endRange=(np.where(gapValues[0] == chromKey+"-row"+str(endV))[0][0])+1
                        
                        addValRange=int(sum(gapValues[startRange:endRange][9].values))
    
                        newLine=str(int(indV[0])+addValRange)+"\t"+indV[1]+"\n"
                        newSCFH.write(newLine)
                endV+=1
            end-=1
   
            
#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    domains_file = os.path.abspath(arguments.domains)

    writeNewScaling(input_file, domains_file)


#####################################################################
if __name__ == '__main__':
    main()