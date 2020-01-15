#!/home/eh37w/miniconda3/bin/python

#Erica Hildebrand
#11/2/17
#Converts cooler files into matrix.gz files in automated way. For 200kb bin - from single resolution files since those seem to have correct genome name for compartment script.

#Import packages - works in python or ipython on cluster
import cooler
import cooltools
import os
from cooltools.io import cool2cworld
import glob

path = "/nl/umw_job_dekker/users/an27w/distiller-dino-all/results/output/coolers/library_group"
PathFile = "{}/Dino-HiC-Dplus-R1.8000.cool".format(path)
path2 = "/nl/umw_job_dekker/users/an27w/distiller-dino-all/results/output/coolers/library_group/Dino-HiC-Dplus-R1-8000-chr"

#! is bash command - lists files in path directory - doesn't work if calling in script, so using glob instead
#files = !ls {multiresPath}
files = glob.glob(PathFile)

#Don't need to specify group since single resolution files.

for cname in files:
    cnameBase=cname.split("/")[9]
    cnameHead1=cnameBase.split(".")[0]
    #cnameHead="cnameHead1.split("__")[0]"
    cnameHead="Dino-HiC-Dplus-R1"
    #extract cooler file
    c = cooler.Cooler(cname)
    #use c.info to access data about cooler
    #cool2cworld
    for chrom in c.chromnames:
        out_dir = "{}/C-{}".format(path2, c.info['bin-size'])
        out_fname = "{}/C-{}/{}_{}_{}_dino_iced.matrix.gz".format(path2, c.info['bin-size'], cnameHead, chrom, c.info['bin-size'])
        os.makedirs(out_dir, exist_ok = True)
        cool2cworld.dump_cworld(c, out=out_fname, region=chrom, iced=True, iced_unity=True)
        
        c.chromnames[88:]
        
         c.bins()[69364:]
         c.bins()[13907:]
         
import cooltools
import os
from cooltools.io import cool2cworld
import cooler

res = c.info['bin-size']
gname = c.info['genome-assembly']
bins = c.bins()[:]
nbins = len(bins)


         
row_headers = [
         '{}|{}|{}:{}-{}'.format(
             binidx1, gname, b1.chrom, b1.start+1, b1.end).encode()
         for binidx1, b1 in bins.iterrows()
    ]        
         
         
         
         
with open("1kbHeadersFileBeforeRemoval","w") as OUT:
    for i in row_headers:
        b= i.decode("utf-8")
        OUT.write(b+"\n")




