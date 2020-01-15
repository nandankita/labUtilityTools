'''
Created on Mar 29, 2019

@author: nanda
python ~/aTools/utilities/scalingPlotDomainsWrapper.py -i ../Dino-HiC-Dplus.40000.cool -d domains -r 40000

python ~/aTools/utilities/scalingPlotDomainsWrapper.py -i ../../HiC-Dplus.dinov1.0-chr95Clusters.no_filter.1000.mcool -d domains -r 50000

'''
import argparse
import textwrap
import os
import cooltools
import importlib.util
import io
from _collections import defaultdict
import itertools
import cooler
from gapEstimate import gapEstimate
from dumpCool2CworldTrans import dumpTransMatrix
from scalingPlotNonDiagonal import calculateScalingNonDiagonal
from scalingPlotDiagonal import calculateScalingDiagonal


#####################################################################
# spec = importlib.util.spec_from_file_location("dumpTransMatrix", "/home/an27w/aTools/utilities/dumpCool2CworldTrans.py")
# dumpCool2CworldTrans = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(dumpCool2CworldTrans)
# 
# spec2 = importlib.util.spec_from_file_location("scalingPlotNonDiagonal", "/home/an27w/aTools/utilities/scalingPlotNonDiagonal.py")
# scalingPlotNonDiagonal = importlib.util.module_from_spec(spec2)
# spec2.loader.exec_module(scalingPlotNonDiagonal)

#####################################################################



def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Scaling plot wrapper, cut out the domains and get scaling plots for all cutout domains
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_cooler_file' ,
                        help = "Input cooler file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-r" ,
                        metavar = 'desired resolution' ,
                        help = "desired resolution" ,
                        dest = "res",
                        required = True ,
                        type = str)
    
    parser.add_argument("-d" ,
                        metavar = 'input_domain_file' ,
                        help = "Input domain, chr,st,end file" ,
                        dest = "domain",
                        required = True ,
                        type = str)
    
    return parser.parse_args()
#####################################################################
def calDominas(domain_file):
    with open(domain_file) as inDM:
        domainList=defaultdict(list)
        end=0
        for line in inDM:
            line=line.rstrip("\n")
            v=line.split("\t")
            if(int(v[1])==1):
                st=1
                continue
            else:
                end=int(v[2])
                domainList[v[0]].append(v[0]+":"+"-".join([str(st),str(end)]))
                st=end+1
    return domainList

#####################################################################
def cutDomainMatricesAndScaling(cooler_file,domain_file,res):
    c = cooler.Cooler(cooler_file+"::/resolutions/"+res)
    resolution=c.info['bin-size']
    
    domainList=calDominas(domain_file)
    
    
    for keys,values in domainList.items():
        oldlocX=0
        row=0
        domain=1
        for i in values:
            locX=i
            locY=i
            if(not oldlocX == locX):
                row+=1
                oldlocX = locX
            filename = keys+"-row"+str(row)+"-domain"+str(domain)+"-diagonal.matrix"
            print(filename, locX, locY)
            dumpTransMatrix(cooler_file, filename,res,locX+","+locY,True,True)
            calculateScalingDiagonal(filename,resolution)
    
           
    for keys,values in domainList.items():
        combs=itertools.combinations(values, 2)
        oldlocX=0
        row=0
        domain=2
        for i in (list(combs)):
            locX=i[0]
            locY=i[1]
            if(not oldlocX == locX):
                row+=1
                domain=2
                oldlocX = locX
            filename = keys+"-row"+str(row)+"-domain"+str(domain)+".matrix"
            print(filename, locX, locY)
            domain+=1
            dumpTransMatrix(cooler_file, filename,res,locX+","+locY,True,True)
            calculateScalingNonDiagonal(filename,resolution)
            
    

#####################################################################

def main():
    arguments = get_arguments()
    cooler_file = os.path.abspath(arguments.input)
    domain_file = os.path.abspath(arguments.domain)
    res = arguments.res
    cutDomainMatricesAndScaling(cooler_file,domain_file,res)
    
    #drawScaling(cooler_file, domain_file)


#####################################################################
if __name__ == '__main__':
    main()
    