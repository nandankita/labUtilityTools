'''
Created on Oct 20, 2017

@author: nanda
'''
import argparse
import textwrap
import os
from collections import defaultdict
from functools import partial


#####################################################################


def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    add coordinates to subscaffolds
    ''') )

    parser.add_argument("-p" ,
                        metavar = 'input_scaffold_list_with_position' ,
                        help = "input_scaffold_listi_with_position" ,
                        dest = "position",
                        required = True ,
                        type = str)
    
    parser.add_argument("-s" ,
                        metavar = 'correct_order_scaffold' ,
                        help = "correct_order_scaffold" ,
                        dest = "scaffold",
                        required = True ,
                        type = str)
    
      
    parser.add_argument("-o" ,
                        metavar = 'output_file_name' ,
                        help = "output file name" ,
                        dest = "output",
                        required = True ,
                        type = str)
    

    return parser.parse_args()
#################
def expandrange(st_index,end_index,binSize):
    binList=[]
    st=int(st_index)
    if(int(st_index)==0):
        st=1
        end=int(st_index)+binSize
        nub_bins=((int(end_index)-int(st_index))/binSize)-1
    else:
        end=int(st_index)-1+binSize
        nub_bins=(int(end_index)-int(st_index))/binSize
    print(nub_bins)
    for i in range(0,nub_bins+1):
        a=str(st)+"-"+str(end)
        binList.append(a)
        st=end+1
        end=end+binSize
    return(binList)

#####################################################################
def addPosition(position,scaffold,out):
    dictScaffolds=defaultdict(list)
    with open(position) as pos, open(scaffold) as sc, open(out, "w") as outFile:
        for p in pos:
            p = p.rstrip("\n")
            p = p.rstrip()
            elm=p.split("\t")
            dictScaffolds[elm[0]]=elm[1]
        for s in sc:
            s = s.rstrip("\n")
            s = s.rstrip()
            sub = s[0:len(s)-1]
            a=dictScaffolds[s].split("-")
            bin_range=expandrange(a[0],a[1],40000)
            for bins in bin_range:
                print(a)
                print(s,bin_range)
                outFile.write(sub+":"+bins)
                outFile.write("\n")
            


#####################################################################

def main():
    arguments = get_arguments()
    position = os.path.abspath(arguments.position)
    scaffold = os.path.abspath(arguments.scaffold)
    out = os.path.abspath(arguments.output)
    
    addPosition(position,scaffold,out)


#####################################################################
if __name__ == '__main__':
    main()

