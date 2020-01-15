import sys
import numpy
import argparse
import textwrap
import os
import cooltools
from cooltools.io import cool2cworld
import cooler

#####################################################################

def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Calculate scaling data for a non diagonal domain
    
    python ~/aTools/utilities/cool2cworld.py -i HiC-D7plus.smic1.0.no_filter.1000.mcool -o test-cD7plus-10kb.raw.matrix -r 10000 -l chr1 -iced true -iced_unity true
    python ~/aTools/utilities/cool2cworld.py -i Dino-HiC-cD7plus.smic1.0.no_filter.1000.mcool -o cD7plus-100kb.raw.matrix -r 100000  -iced false -iced_unity false
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_mcool_file' ,
                        help = "Input mcool file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    parser.add_argument("-o" ,
                        metavar = 'output_matrix_file' ,
                        help = "output matrix file" ,
                        dest = "outFile",
                        required = True ,
                        type = str)
    parser.add_argument("-r" ,
                        metavar = 'resolution' ,
                        help = "resolution of matrix file" ,
                        dest = "resolution",
                        required = True ,
                        type = str)
    
    parser.add_argument("-l" ,
                        metavar = 'location/region' ,
                        help = "location/region" ,
                        dest = "region",
                        required = False ,
                        default = "",
                        type = str)
    
    parser.add_argument("-iced" ,
                        metavar = 'iced' ,
                        help = "iced" ,
                        dest = "iced",
                        required = False ,
                        default = True,
                        type = lambda x: (str(x).lower() == 'true'))
    
    parser.add_argument("-iced_unity" ,
                        metavar = 'iced_unity' ,
                        help = "iced_unity" ,
                        dest = "iced_unity",
                        required = False ,
                        default = True,
                        type = lambda x: (str(x).lower() == 'true'))
    
    

    return parser.parse_args()

#####################################################################
def coolCworld(coolerFile,outFile,resolution,region,iced,iced_unity):
    c = cooler.Cooler(coolerFile+"::/resolutions/"+resolution)
    print(c.info)
    print(iced,iced_unity,region)
    cool2cworld.dump_cworld(c, out=outFile, region=region, iced=iced, iced_unity=iced_unity)

#####################################################################

def main():
    arguments = get_arguments()
    coolerFile = os.path.abspath(arguments.input)
    outFile = os.path.abspath(arguments.outFile)
    resolution = str(arguments.resolution)
    region = str(arguments.region)
    iced = arguments.iced
    iced_unity = arguments.iced_unity
    
    coolCworld(coolerFile,outFile,resolution,region,iced,iced_unity)


#####################################################################
if __name__ == '__main__':
    main()