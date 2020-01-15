'''
Created on May 6, 2017

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
    expand subscaffolds to bins
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_matrix_tab_file' ,
                        help = "Input Matrix tab file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-o" ,
                        metavar = 'correct order file' ,
                        help = "correct_order_file" ,
                        dest = "order",
                        required = True ,
                        type = str)
    
    parser.add_argument("-c" ,
                        metavar = 'old/current order file of matrix' ,
                        help = "old_order_file" ,
                        dest = "current",
                        required = True ,
                        type = str)
    parser.add_argument("-b" ,
                        metavar = 'bin size of matrix' ,
                        help = "bin_size" ,
                        dest = "binsize",
                        required = True ,
                        type = str)
    
    
    return parser.parse_args()

def expandrange(st_index,end_index,binSize):
    binList=[]
    st=st_index
    end=binSize
    nub_bins=int(end_index)/binSize
    for i in range(0,nub_bins):
        a=str(st)+"-"+str(end)
        binList.append(a)
        st=end+1
        end=end+binSize
    return(binList)
##############################
def duplicates(lst, item):
    return [i for i, x in enumerate(lst) if x == item]

#####################################################################
def rearrangeMatrix(input_file,order_file,order_current,binSize):
    with gzip.open(input_file) as inFH, open(order_file) as orderFH, open(order_current) as currFH, open("rearranged.matrix","w") as outFH:
        new_order = []
        old_order = []
        for line in orderFH:
            line=line.rstrip("\n")
            line=line.rstrip()
            a=line.split("__")
            bin_range=expandrange(a[1],a[2],binSize)
            for bins in bin_range:
                heading=a[0]+":"+bins
                new_order.append(heading)
        print(new_order, "new_order")
        print(len(new_order), "new_order")
        for c in currFH:
            c = c.rstrip("\n")
            c = c.rstrip() 
            old_order.append(c)
        print(len(old_order), "old_order")
        m = []
        order_list = []
        compared_from_old=[0]*len(old_order)
        for n in new_order:
            if(old_order.index(n)):
                idx=old_order.index(n)
                order_list.append(idx)
                compared_from_old[idx]=1
        remaining_elements=duplicates(compared_from_old,0)
        final_order_indx=order_list+remaining_elements
        remaining_heading=list(set(old_order) - set(new_order))
        final_order=new_order+remaining_heading
        print(len(final_order), "final_order")
        for matrixLine in inFH:
            matrixLine=matrixLine.rstrip("\n")
            matrixLine=matrixLine.split("\t")
            del matrixLine[0]
            m.append(matrixLine)
        A = [[m[i][j] for j in final_order_indx] for i in final_order_indx]
        leng=len(final_order)
        final_order.insert(0, str(leng)+"x"+str(leng))
        outFH.write("\t".join(final_order))
        del final_order[0]
        outFH.write("\n")
        count=0
        for a in A:
            a.insert(0, final_order[count])
            outFH.write("\t".join(a))
            outFH.write("\n")
            count+=1
        

#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    order_file = os.path.abspath(arguments.order)
    order_current = os.path.abspath(arguments.current)
    binsize=int(arguments.binsize)
    
    rearrangeMatrix(input_file,order_file,order_current,binsize)


#####################################################################
if __name__ == '__main__':
    main()
