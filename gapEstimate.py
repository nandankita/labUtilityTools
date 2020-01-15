'''
Created on Mar 25, 2019

@author: nanda
python ~/aTools/utilities/gapEstimate.py -i scaling_data.chr5-diagonal.domain1.matrix -y 0.0037776825

'''
import sys
import numpy as np
import pandas
import argparse
import textwrap
import os
from _collections import defaultdict

#####################################################################
def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Given a y value it will interpolate the x value shift for the scaling plot
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_scaling_data_file' ,
                        help = "Input scaling_data file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-y" ,
                        metavar = 'y value to interpolate' ,
                        help = "y value to interpolate" ,
                        dest = "yValue",
                        required = True ,
                        type = str)
    
    
    return parser.parse_args()

#####################################################################


def gapEstimate(inFile1,predV):
    xbins1=[]
    yAvg1=[]
    
    scalingData=pandas.read_csv(inFile1, sep='\t',header=None)
    sortedScaling=scalingData.sort_values(by=[1])
    
    for i in sortedScaling[0]:
        yAvg1.append(float(i))
        
    for i in sortedScaling[1]:
        xbins1.append(float(i))
             
    xShift=np.interp(predV, xbins1, yAvg1)
    print(xShift)
    return(xShift)


#####################################################################


def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    yValue = float(arguments.yValue)
    gapEstimate(input_file,yValue)
    

#####################################################################

if __name__ == '__main__':
    main()