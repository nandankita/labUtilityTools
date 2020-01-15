import argparse
import textwrap
import os
import cooler
import cooltools
import pandas as pd
import numpy as np


#####################################################################

def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Given a cooler file create a begraph file of Cis only Hi-C interactions
    #python ~/aTools/utilities/coolerHi-C-Cis-interaction2bedgraph.py -i Dino-HiC-Dplus-R1.1000.cool -o Dino-HiC-Dplus-R1.1000.cis.bedGraph
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_cooler_file' ,
                        help = "Input cooler file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-o" ,
                        metavar = 'output_begraph_file' ,
                        help = "output begraph file" ,
                        dest = "out",
                        required = True ,
                        type = str)
    
    
    return parser.parse_args()

#####################################################################
def insert(originalfile,header):
    with open(originalfile,'r') as f:
        with open('newfile.txt','w') as f2: 
            f2.write(header)
            f2.write(f.read())
    os.rename('newfile.txt',originalfile)


def createbedGraph(input_file,output_file):
    df = pd.DataFrame([])
    c = cooler.Cooler(input_file)
    chrs=c.chromnames
    for i in chrs:
        print("working on "+i)
        binV = c.bins().fetch(i).copy()
        binV["interactions"]=np.nan_to_num(np.array(c.matrix().fetch(i))).sum(axis=0)
        df=df.append(pd.DataFrame(binV))
    df.to_csv(output_file,sep='\t', index=False, header=False, columns=["chrom","start","end","interactions"])
    header="track type=bedGraph name=\"Hi-C Cis interactions\" description=\"Hi-C Cis interactions\" maxHeightPixels=128:64:1 visibility=full autoScale=off color=200,100,0 altColor=0,100,200 priority=20\n"
    insert(output_file,header)

#####################################################################


def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    output_file = os.path.abspath(arguments.out)
    createbedGraph(input_file,output_file)
    

#####################################################################

if __name__ == '__main__':
    main()
