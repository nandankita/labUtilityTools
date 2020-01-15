'''
Created on Mar 1, 2019

@author: nanda
python ~/aTools/utilities/scalingPlotDiagonal.py chr2-diagonal.domain1.matrix
'''

import sys
import numpy
import argparse
import textwrap
import os


#####################################################################

def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Calculate scaling data for a non diagonal domain
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_matrix_file' ,
                        help = "Input matrix file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    parser.add_argument("-r" ,
                        metavar = 'resolution' ,
                        help = "resolution of matrix file" ,
                        dest = "resolution",
                        required = True ,
                        type = str)
    

    return parser.parse_args()

#####################################################################
def calculateScalingDiagonal(input_file, resolution):

    inFile= input_file
    
    inF=inFile.split("/")
    if(len(inF)>0):
        filename=inF[-1]
    
    else:
        filename=inFile
    
    RESOLUTION=int(resolution)
    colNames=[]
    firstRow=0
    
    ln=0
    
    with open(inFile, "r") as lineFH:
        for line in lineFH:
            line=line.rstrip("\n")
            indV=line.split("\t")
            if(ln==0):
                for l in indV:
                    v=l.split('|')
                    if(len(v)>2):
                        v1=v[2].split(":")
                        v2=v1[1].split("-")
                        ##End of the bin
                        colNames.append(v2[0])
                ln+=1
            else:
                v=indV[0].split('|')
                v1=v[2].split(":")
                v2=v1[1].split("-")
                firstRow=v2[0]
                break
    
    startNumber = abs(int(colNames[0])-int(firstRow))
    
    inMatrix=numpy.loadtxt(inFile,skiprows=1,usecols=range(1,len(colNames)+1))
    diagNumber=0
    
    averageList=[]
    
    while(inMatrix.diagonal(diagNumber).size!=0):
        diagValues1=inMatrix.diagonal(diagNumber)
        diagValues=numpy.nan_to_num(diagValues1)
        avgn=sum(diagValues)/diagValues.size
        averageList.append(avgn)
        diagNumber+=1
    
    # c=0
    # #print(averageList, colNames)
    # with open("scaling_data."+inFile, "w") as sdFH:
    #     for i in averageList:
    #         #sdFH.write(str(i)+"\n")
    #         #print(colNames[c]+"\t"+str(i)+"\n")
    #         sdFH.write(colNames[c]+"\t"+str(i)+"\n")
    #         c+=1
            
    with open("scaling_data."+filename, "w") as sdFH:
        for i in averageList:
            sdFH.write(str(startNumber)+"\t"+str(i)+"\n")
    #         if(c==0):
    #             startNumber-=1
    #             c+=1
            startNumber+=RESOLUTION
    

#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    resolution = str(arguments.resolution)

    
    
    calculateScalingDiagonal(input_file, resolution)


#####################################################################
if __name__ == '__main__':
    main()
