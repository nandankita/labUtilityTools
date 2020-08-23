'''
Created on Mar 28, 2019

@author: nanda

python ~/aTools/utilities/dumpCool2CworldTrans.py -i ../HiC-Dplus.dinov1.0-chr95Clusters.no_filter.1000.mcool 
-o chr4-domain2.matrix -l chr4:1-2050000,chr4:2050001-3450000 -r 50000 -iced True -iced_unity True

python ~/aTools/utilities/dumpCool2CworldTrans.py -i HiC-Dplus.dino-missingClusters95.no_filter.1000.mcool 
-o D-trans-chr4-cluster4.raw50kb.matrix -l cluster4,chr4 -r 50000 -iced false -iced_unity false

python ~/aTools/utilities/dumpCool2CworldTrans.py -i HiC-mDplus.dino-missingClusters95.no_filter.1000.mcool -o mastigotes-mD-trans-chr4-cluster4-50kbiced.matrix -l cluster4,chr4 -r 50000 -iced true -iced_unity true

'''
import argparse
import textwrap
import os
import cooltools
import cooler   
from cooltools.io import fastsavetxt
import io

#####################################################################



def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    extract trans interactions from a cooler file
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_cooler_file' ,
                        help = "Input cooler file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    parser.add_argument("-o" ,
                        metavar = 'output_matrix_file' ,
                        help = "output matrix file" ,
                        dest = "output",
                        required = True ,
                        type = str)
    
    parser.add_argument("-l" ,
                        metavar = 'location' ,
                        help = "location" ,
                        dest = "location",
                        required = True ,
                        type = str)
    
    parser.add_argument("-r" ,
                        metavar = 'desired resolution' ,
                        help = "desired resolution" ,
                        dest = "res",
                        required = True ,
                        type = str)
    
    parser.add_argument("-iced" ,
                        metavar = 'iced' ,
                        help = "iced" ,
                        dest = "iced",
                        required = False ,
                        default = False,
                        type = lambda x: (str(x).lower() == 'true'))
    
    parser.add_argument("-iced_unity" ,
                        metavar = 'iced_unity' ,
                        help = "iced_unity" ,
                        dest = "iced_unity",
                        required = False ,
                        default = False,
                        type = lambda x: (str(x).lower() == 'true'))
    

    return parser.parse_args()

#####################################################################
def dumpTransMatrix(input_file, out, res,location, iced, iced_unity):
    c = cooler.Cooler(input_file+"::/resolutions/"+res)
    
    gname = c.info['genome-assembly']
    l=location.split(",")
    xloc=l[0]
    yloc=l[1]
    
    xbins=c.bins().fetch(xloc)
    ybins=c.bins().fetch(yloc)
    
    nbinsX = len(xbins)
    nbinsY = len(ybins)
    
    
    xStartIndx= c.bins().fetch(xloc)[:].index.values.astype(int)[0]
    xEndIndx= c.bins().fetch(xloc)[:].index.values.astype(int)[-1]+1
    yStartIndx= c.bins().fetch(yloc)[:].index.values.astype(int)[0]
    yEndIndx= c.bins().fetch(yloc)[:].index.values.astype(int)[-1]+1
    
    ##SPECIAL CASE FOR SCALING PLOT
    if(xEndIndx-1==yStartIndx):
        xEndIndx-=1
    
    
    #print(xStartIndx,xEndIndx,yStartIndx,yEndIndx)
    
    col_headers = '\t'.join(
        ['{}x{}'.format(nbinsX, nbinsY)] +
        ['{}|{}|{}:{}-{}'.format(
            binidx, gname, b.chrom, b.start+1, b.end)
         for binidx, b in ybins.iterrows()
        ]
    ).encode()
    
    row_headers = [
        '{}|{}|{}:{}-{}'.format(
            binidx1, gname, b1.chrom, b1.start+1, b1.end).encode()
        for binidx1, b1 in xbins.iterrows()
    ]
    
       
    mat = c.matrix(balance=iced)[xStartIndx:xEndIndx,yStartIndx:yEndIndx]

    
    if (iced and (not iced_unity)):
        print("hello")
        mat *= (c._load_attrs('/bins/weight')['scale'])
    
    
    if not(out):
        out = io.BytesIO(b'')
    if issubclass(type(out), str) or issubclass(type(out), bytearray):
        if out.endswith('.gz'):
            writer = fastsavetxt.gzipWriter(out)
            out_pipe = writer.stdin
            close_out_func = writer.communicate
        else:
            writer = open(out, 'wb')
            out_pipe = writer
            close_out_func = writer.flush
    elif hasattr(out, 'write'):
        out_pipe = out
        close_out_func = fastsavetxt.empty_func
    
    
    fastsavetxt.array2txt(
        mat,
        out_pipe,
        format_string = b'%.8f' if iced_unity else b'%.4lf',
        header=col_headers,
        row_headers = row_headers,
    )
   
    if issubclass(type(out), io.BytesIO):
        return out.getvalue()
    else:
        close_out_func()


#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    output_file = os.path.abspath(arguments.output)
    res = arguments.res
    location = str(arguments.location)
    iced = bool(arguments.iced)
    iced_unity = bool(arguments.iced_unity)
    
    
    dumpTransMatrix(input_file, output_file, res, location,iced,iced_unity)


#####################################################################
if __name__ == '__main__':
    main()
    