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
    rearrange a matrix in a given order file.
    python ~/aTools/utilities/rearrangeMatrix.py -i rearranged_clusterAll.matrix -o selectedOrderAll -c currentOrder  
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
    
    return parser.parse_args()

#####################################################################
def rearrangeMatrix(input_file,order_file,order_current):
    with open(input_file) as inFH, open(order_file) as orderFH, open(order_current) as currFH, open("rearranged.matrix","w") as outFH:
        new_order = []
        old_order = []
        count = 0
        for line in orderFH:
            line=line.rstrip("\n")
            line=line.rstrip()
            new_order.append(line)
        for c in currFH:
            c = c.rstrip("\n")
            c = c.rstrip() 
            old_order.append(c)
        m = []
        order_list = []
        for n in new_order:
            idx=old_order.index(n)
            order_list.append(idx)
        print("order Index created") 
        for matrixLine in inFH:
            if(count == 0):
                count+=1
            else:
                matrixLine=matrixLine.rstrip("\n")
                matrixLine=matrixLine.split("\t")
                del matrixLine[0]
                m.append(matrixLine)
        print("Matrix read")
        #A = [[m[i][j] for j in order_list] for i in order_list]
        A = [m[i] for i in order_list]
        leng=len(new_order)
        print("neworder Length",leng)
        new_order.insert(0, str(leng)+"x"+str(leng))
        outFH.write("\t".join(new_order))
        del new_order[0]
        outFH.write("\n")
        count=0
        for a in A:
            a.insert(0, new_order[count])
            outFH.write("\t".join(a))
            outFH.write("\n")
            count+=1
        

#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    order_file = os.path.abspath(arguments.order)
    order_current = os.path.abspath(arguments.current)
    
    rearrangeMatrix(input_file,order_file,order_current)


#####################################################################
if __name__ == '__main__':
    main()

