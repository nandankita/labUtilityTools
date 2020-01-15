'''
Created on Mar 16, 2017

@author: nanda
'''
import argparse
import textwrap
import os
import gzip

#####################################################################


def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Remove the lines from unselected Index and create new matrix without those lines.
    1 based index file
    python ~/aTools/utilities/extractMatrixRemoveBins.py  -i teset23.matrix -s testIndex
    
    python ~/aTools/utilities/extractMatrixRemoveBins.py  -i Dino-HiC-Dplus_chr7_1000_dino_iced.matrix.gz -s unselectedIndexchr7 -c 7
    
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_matrix_gz_file' ,
                        help = "Input Matrix gz file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-s" ,
                        metavar = 'unselected index file' ,
                        help = "unselected_index_file" ,
                        dest = "order",
                        required = True ,
                        type = str)
    parser.add_argument("-c" ,
                        metavar = 'chromosome' ,
                        help = "chromosome for file name" ,
                        dest = "chr",
                        required = True ,
                        type = str)
    
    return parser.parse_args()

#####################################################################

def removeBins(input_file,unselected_order,chr):
    out=os.path.abspath('') 
    output_file=out+"/chr"+str(chr)+"-binsRemoved-rearranged.matrix.gz"
    with open(unselected_order, 'r') as orderFH: 
        orders=[]
        for line in orderFH:
            line = line.rstrip('\n')
            if (line != ""):
                orders.append(line)

    orderList = set(list(map(int, orders)))
    rLen = len(orderList)
    rowOrderIndex= [x for x in orderList]
    colOrderIndex= [x for x in orderList]
    count=0
    #totalInteractions = 0
    with gzip.open(input_file, 'rt') as inMatrixFH, gzip.open(output_file, 'wt') as outMatrixFH:
        for x in inMatrixFH:
            x = x.rstrip('\n')
            values=x.split("\t")
            if(count==0):
                colOrderIndex.insert(0,0)
                mLen = int((values[0].split("x"))[0])-rLen
                mSize = str(mLen)+"x"+str(mLen)
                for index in sorted(colOrderIndex, reverse=True):
                    del values[index]
                values.insert(0,mSize)
                outMatrixFH.write("\t".join(values))
                outMatrixFH.write("\n")
                del colOrderIndex[0]
            elif((count>0) and (count not in rowOrderIndex)):
                #totalInteractions += sum(list(map(float, values[1:len(values)])))
                for index in sorted(colOrderIndex, reverse=True):
                    del values[index]
                outMatrixFH.write("\t".join(values))
                outMatrixFH.write("\n")
            count+=1
    #print(totalInteractions)
                
    
#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    unselected_order = os.path.abspath(arguments.order)
    chr = arguments.chr
    removeBins(input_file,unselected_order,chr)


#####################################################################
if __name__ == '__main__':
    main()
