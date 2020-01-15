'''
Created on Oct 27, 2017

@author: nanda
'''

import argparse
import textwrap
import os
import gzip
from _collections import defaultdict

#####################################################################



def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    extract cis interactions in a given matrix
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_tab_matrix_file' ,
                        help = "Input tab matrix file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    parser.add_argument("-o" ,
                        metavar = 'output_matrix_file' ,
                        help = "Output tab matrix file" ,
                        dest = "output",
                        required = True ,
                        type = str)
    parser.add_argument("-f" ,
                        metavar = 'cluster file' ,
                        help = "Input cluster file" ,
                        dest = "cluster",
                        required = True ,
                        type = str)
    parser.add_argument("-n" ,
                        metavar = 'cluster number' ,
                        help = "cluster number to be extracted" ,
                        dest = "number",
                        required = True ,
                        type = str)

    return parser.parse_args()

#####################################################################