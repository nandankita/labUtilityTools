'''
Created on Oct 25, 2017

@author: nanda
'''

# coding: utf-8

# We'll try to gather some deeper insight into cooler and loop-calling  here:

import argparse
import textwrap
import os
import cooler
import cooltools
import pandas as pd
import numpy as np
import cooltools.expected as cooltool_exp
from cooler.contrib.dask import daskify

#####################################################################


def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Compute Trans and cis expected from a cooler file, requires cool tools
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_cooler_file' ,
                        help = "Input cooler file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    return parser.parse_args()

#####################################################################
def createExp(input_file):
    
    #put my cooler file here
    c = cooler.Cooler(input_file)
    print(c.info)
    
    fileName=os.path.basename(input_file)
    o=str(fileName).split(".")
    outFileCis=o[0]+".cis.expected"
    outFileTrans=o[0]+".trans.expected"
    
    # #### Next thing is an expected calculations:
    # 
    # it requires direct access to the Cooler object, region name and chunksize.
    # 
    # Beware: zoomified coolers won't work for now, because inside expected calculations we rely on the `pixels` group of HDF5 file, in case of zoomified cooler, one would need to access `/11/pixels` group for example.
    # 
    
    
    # see expected code to understand, why we use a tuple of 1 to extract the whole chromosome stuff:
    # syntax for regions: "chrX:10,000-20,000"
    # other way: ('chrX',10000,2000)
    # whole chromosome ('chrX',)
    
    #region = ('chr17',)
    #region2 = ('chrX',)
    #regions = [region,region2]
    regions = [('chr1',),
    ('chr2',),
    ('chr3',),
    ('chr4',),
    ('chr5',),
    ('chr6',),
    ('chr7',),
    ('chr8',),
    ('chr9',),
    ('chr10',),
    ('chr11',),
    ('chr12',),
    ('chr13',),
    ('chr14',),
    ('chr15',),
    ('chr16',),
    ('chr17',),
    ('chr18',),
    ('chr19',),
    ('chr20',),
    ('chr21',),
    ('chr22',),
    ('chrX',),
    ('chrY',),
    ('chrM',)]
    
    chromosomes=['chr1',
 'chr2',
 'chr3',
 'chr4',
 'chr5',
 'chr6',
 'chr7',
 'chr8',
 'chr9',
 'chr10',
 'chr11',
 'chr12',
 'chr13',
 'chr14',
 'chr15',
 'chr16',
 'chr17',
 'chr18',
 'chr19',
 'chr20',
 'chr21',
 'chr22',
 'chrX',
 'chrY',
 'chrM']
    # 
    res = cooltool_exp.compute_expected(c, regions, chunksize=1000000)
    
    pixels = daskify(c.filename, 'pixels', chunksize=1000000)
    trans_sum, trans_area = cooltool_exp.compute_trans_expected(c,pixels,chromosomes)
    transExp=trans_sum/trans_area
    #expected = res.loc['chr17']['balanced.avg']
    # res.head()  - to check what's inside
    res.to_csv(outFileCis)
    with open(outFileTrans, "w") as OUTFH:
        OUTFH.write("trans_sum\ttrans_area\ttransExp\n") 
        OUT="{}\t{}\t{}".format(trans_sum,trans_area,transExp)
        OUTFH.write(OUT)
    
    #res.to_pickle('expected_chr17')


#####################################################################    

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    
    
    createExp(input_file)


#####################################################################
if __name__ == '__main__':
    main()