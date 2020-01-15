'''
Created on Jul 21, 2017

@author: nanda
'''
import argparse
import textwrap
import os
import gzip
from pathlib import Path

#####################################################################

def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    split a fastq.gz file into multiple 
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_folder' ,
                        help = "Input folder" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-o" ,
                        metavar = 'output_folder' ,
                        help = "output folder" ,
                        dest = "output",
                        required = True ,
                        type = str)
    
    parser.add_argument("-p" , 
                        metavar = 'output_file_prefix' ,
                        help = "output file prefix" ,
                        dest = "prefix",
                        required = True ,
                        type = str)
    
    parser.add_argument("-q" ,
                        metavar = 'input_file_prefix' ,
                        help = "input file prefix" ,
                        dest = "prefix_in",
                        required = True ,
                        type = str)

    return parser.parse_args()

#####################################################################
def combineFiles(input_fol, output_fol,out_prefix,in_prefix):
    rList=["R1","R2"]
    for r in rList:
        x = int(1)
        count = str(x).zfill(3)
        my_file_r = Path(input_fol+"/"+in_prefix+r+"_"+count+".fastq.gz")
        my_out_r = str(output_fol+"/"+out_prefix+r+"_000.fastq.gz")
        
        with gzip.open (my_out_r, "wt")as outFH:
            
            while(my_file_r.is_file()):
                print(my_file_r)
                with gzip.open(str(my_file_r), "rt") as inFH:
                    for lines in inFH:
                        outFH.write(lines)
                x+=1
                count = str(x).zfill(3)
                my_file_r = Path(input_fol+"/"+in_prefix+r+"_"+count+".fastq.gz")
                
    
    



#####################################################################

def main():
    arguments = get_arguments()
    input_fol = os.path.abspath(arguments.input)
    output_fol = os.path.abspath(arguments.output)
    out_prefix = str(arguments.prefix)
    in_prefix = str(arguments.prefix_in)
    
    combineFiles(input_fol,output_fol,out_prefix,in_prefix)


#####################################################################
if __name__ == '__main__':
    main()
    