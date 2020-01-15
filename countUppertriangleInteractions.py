'''
Created on May 16, 2017

@author: nanda
'''
import argparse
import textwrap
import os


#####################################################################



def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    sum the upper triangle matrix and give mean
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_tab_matrix_file' ,
                        help = "Input tab matrix file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    

    return parser.parse_args()

#####################################################################
def countInteractions(input_file):
    count = 0
    with open(input_file, "r") as MATRIXFH:
        i=1
        sumLine=0.0
        pix=0
        for line in MATRIXFH:
            line=line.rstrip("\n")
            line=line.rstrip()
            if(count == 0):
                count+=1
            else:
                interactions=line.split("\t")
                for j in range(1, len(interactions)):
                    if(j>=i):
                        sumLine+=float(interactions[j])
                        pix+=1
                    j+=1
                i+=1
        print("Total upper triangle interactions:"+str(sumLine))
        print("\n")
        print("Mean:"+str(sumLine/pix))
        
   
#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    
    
    countInteractions(input_file)


#####################################################################
if __name__ == '__main__':
    main()
    