'''
Created on Mar 29, 2019

@author: nanda

python ~/aTools/utilities/gapEstimateWarpper.py -d domains
'''
from gapEstimate import gapEstimate
from scalingPlotDomainsWrapper import calDominas
import argparse
import textwrap
import os
import gzip
from _collections import defaultdict
import pandas
import math

#####################################################################

def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    gap Estimate wrapper given the domains list
    ''') )

    
    parser.add_argument("-d" ,
                        metavar = 'input_domain_file' ,
                        help = "Input domain, chr,st,end file" ,
                        dest = "domain",
                        required = True ,
                        type = str)
    
    return parser.parse_args()

#####################################################################

def roundup(x):
    return int(math.floor(x / 1000.0)) * 1000

def getFileName(domains):
    fileNames=[]
    for k,v in domains.items():
        row=1
        #domain=1
        for i in range(len(v)-1):
            #diagFileName="scaling_data."+k+"-diagonal.domain"+str(domain)+".matrix"
            diagFileName="scaling_data."+k+"-row"+str(row)+"-domain1-diagonal.matrix"
            domainFileName="scaling_data."+k+"-row"+str(row)+"-domain2.matrix"
            row+=1
            #domain+=1
            fileNames.append([diagFileName,domainFileName])
    return fileNames
    
#####################################################################    
def gapCalculate(domain_file):
    
    domains=calDominas(domain_file)
    fileNames=getFileName(domains)
    
    
    with open("scalingShift.txt", "w") as scFH:
        scFH.write("\t".join(["file","y1 value","x1 value","x1 predicted","x1 shift","y2 value","x2 value","x2 predicted","x2 shift","Average"+"\n"]))
        for f in fileNames:
            print(f)
            usedList=[]
            scalingDataDiagonal=pandas.read_csv(f[1], sep='\t',header=None)
            y1=scalingDataDiagonal.iloc[[2]][1].values[0]
            y2=scalingDataDiagonal.iloc[[4]][1].values[0]
            
            x1Minus=(scalingDataDiagonal.iloc[[2]][0].values[0])
            x2Minus=(scalingDataDiagonal.iloc[[4]][0].values[0])
            
            x1Pred=gapEstimate(f[0],y1)
            x2Pred=gapEstimate(f[0],y2)
            
            usedList.append(2)
            usedList.append(4)
            
            if(x1Pred-int(x1Pred)==0):
                usedList.append(1)
                y1=scalingDataDiagonal.iloc[[1]][1].values[0]
                x1Minus=(scalingDataDiagonal.iloc[[1]][0].values[0])
                x1Pred=gapEstimate(f[0],y1)
 
            if(x2Pred-int(x2Pred)==0):
                usedList.append(3)
                y2=scalingDataDiagonal.iloc[[3]][1].values[0]
                x2Minus=(scalingDataDiagonal.iloc[[3]][0].values[0])
                x2Pred=gapEstimate(f[0],y2)
            
            if(x1Pred-int(x1Pred)==0):
                print("hello")
                y1=scalingDataDiagonal.iloc[[0]][1].values[0]
                x1Minus=(scalingDataDiagonal.iloc[[0]][0].values[0])
                x1Pred=gapEstimate(f[0],y1)
            
            if(x2Pred-int(x2Pred)==0):
                if (1 not in usedList):
                    y2=scalingDataDiagonal.iloc[[1]][1].values[0]
                    x2Minus=(scalingDataDiagonal.iloc[[1]][0].values[0])
                    x2Pred=gapEstimate(f[0],y2)
            
                else:
                    y2=scalingDataDiagonal.iloc[[0]][1].values[0]
                    x2Minus=(scalingDataDiagonal.iloc[[0]][0].values[0])
                    x2Pred=gapEstimate(f[0],y2)
                

            x1=x1Pred-x1Minus
            x2=x2Pred-x2Minus
            
            v=(f[1].split(".")[1].split("-"))
            
            avg=roundup((x1+x2)/2)
            
            #scFH.write(v[0]+"-"+v[1]+"\t"+str(x1)+"\t"+str(x2)+"\t"+str(avg)+"\n")
            
            scFH.write("\t".join([v[0]+"-"+v[1],str(y1),str(x1Minus),str(x1Pred),str(x1),str(y2),str(x2Minus),str(x2Pred),str(x2),str(avg)+"\n"]))
            
                       
            

#####################################################################

def main():
    arguments = get_arguments()
    domain_file = os.path.abspath(arguments.domain)

    gapCalculate(domain_file)
    


#####################################################################
if __name__ == '__main__':
    main()
