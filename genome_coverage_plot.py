#!/bin/env python3

# AUTHOR:
#        Hakan Ozadam
#        Dekker Laboratory
#        UMASS Medical School / HHMI
#        RNA Therapeutics Institute
#        Albert Sherman Center, ASC4-1009
#        368 Plantation Street
#        Worcester, MA 01605
#        USA
#
#################################################################

from sys import stdout
import argparse
import os
import re
import shutil
from subprocess import Popen, PIPE, TimeoutExpired
from glob import glob
import datetime
import numpy as np
import matplotlib
import matplotlib.mlab as mlab
import gzip
from collections import OrderedDict

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
#from matplotlib.backends.backend_pdf import PdfPages

#################################################################

def verbose_print(*args, **kwargs):
    return 0
    print(*args, **kwargs)


##################################################################

def get_arguments():
    parser = argparse.ArgumentParser(description=
    '''
         For a given hic matrix (matrix.gz)
         This script finds the sum of each column and plots it
         against the column (bin) positions.

         The actual sums are normalized by total matrix sum
         by dividing the matrix sum to column sum

         A typical resolution used, for say human genome is 1M
    ''')
    parser.add_argument("-i" ,
                        help = "Input file. It is in matrix.gz format" ,
                        required = True ,
                        type = str)
    parser.add_argument("-o" ,
                        help = "Output file prefix." ,
                        required = True ,
                        type = str)
    parser.add_argument("-y" ,
                        help = "Y axis maximum value." ,
                        required = False ,
                        default = 0.001,
                        type = float)
    parser.add_argument("-t" ,
                        help = "Graph Title" ,
                        required = False ,
                        default = "Genome Coverage",
                        type = str)
    arguments = parser.parse_args()
    return arguments


##################################################################

def sum_columns(input_file):

    with gzip.open(input_file, "rt") as input_stream:
        line = input_stream.readline()
        while line[0] == "#":
            line = input_stream.readline()
        header_contents = line.split()
        size = int(header_contents[0].split("x")[0])
        column_sums = [0] * size
        
        for line in input_stream:
            line_contents = line.strip().split()
            del(line_contents[0])
            for i in range(0,size):
                column_sums[i] += float(line_contents[i])


    return column_sums, header_contents[1:]



###################################################################
def get_header_info(headers_array):
    header_info = OrderedDict()
    header_boundaries = list()

    for current_header in headers_array:
        pre_contents = current_header.split("|")
        if len(pre_contents) < 3:
            continue
        contents = pre_contents[2].split(":")
        chromosome = contents[0]
        positions = list(map(int, contents[1].split("-") ) )
        if header_info.get(chromosome) != None:
            header_info[chromosome]["end_bin"] = int(pre_contents[0])
            header_info[chromosome]["end_position"] = int( positions[1] )
        else:
            header_info[chromosome] = {"start_bin": int(pre_contents[0]),
                                        "end_bin": int(pre_contents[0]),
                                        "start_position" : int( positions[0]),
                                        "end_position" : int( positions[1])}

    for chromosome, chr_info in header_info.items():
        header_boundaries.append(chr_info["end_bin"])
    return header_boundaries, header_info

######################################################################

def get_chromosome_label_positions(info_dictionary):
    labels = list()
    positions = list()

    for chromosome, contents in info_dictionary.items():
        labels.append(chromosome)
        positions.append(int( (contents["start_bin"] + contents["end_bin"]) / 2 ))

    return positions, labels

###################################################################

def main():
    arguments = get_arguments()
    y_max = arguments.y

    column_sums , headers = sum_columns(arguments.i)
    header_boundaries, header_info = get_header_info(headers)
    label_positions, labels = get_chromosome_label_positions(header_info)

    # Fix x-axis coordinates to do such a filtering!!!
    #filtered_sums = [ x for x in column_sums if x > 100 ]

    filtered_sums = column_sums

    all_sum = sum(filtered_sums)
    normalized_frequencies = [ z / all_sum for z in filtered_sums ]

    sorted_sums = sorted(normalized_frequencies)
    sorted_length = len(sorted_sums)
    clip_margin = int( (sorted_length / 100) * 2)
    print(sorted_length, clip_margin)
    filtered_sorted_sums = sorted_sums[ clip_margin: sorted_length - clip_margin ]

    mean_freq = np.mean(filtered_sorted_sums)
    mean_std = np.std(filtered_sorted_sums)
    print(mean_freq, mean_std)

    matplotlib.rcParams.update({'font.size': 30})
    y = normalized_frequencies
    x = np.arange(len(y))
    fig = plt.figure()
    axes = plt.gca()
    axes.set_ylim([0, y_max])
    ax = plt.subplot(111)
    ax.plot(x, y, label='$y = sum of bins')
    #ax.vlines(header_boundaries, 0, y_max)
    plt.xticks(label_positions, labels , rotation='vertical')

    for i, chromosome in enumerate(header_info.values()):
        if i % 2 == 0:
            ax.fill_between([chromosome["start_bin"]-1,
                              chromosome["start_bin"]-1,
                              chromosome["end_bin"],
                              chromosome["end_bin"]],
            y1 = 0, y2=y_max, facecolor='green', alpha = 0.2 )

    plt.subplots_adjust(bottom=0.15)
    plt.title(arguments.t, fontsize = 40)
    fig.set_size_inches(60, 30)
    ax.tick_params(direction='out', pad=35)
    ax.set_xlabel('Bins')
    ax.set_ylabel('Relative Column Sum = Bin Total / Matrix Total')
    #plt.show()

    fig.savefig(arguments.o + '_plot.pdf')

    #############
    matplotlib.rcParams.update({'font.size': 8})


    fig2 = plt.figure()
    pre_hist_frequencies = [z for z in column_sums if z > 0 ]
    hist_frequencies = (pre_hist_frequencies)
    n, bins, patches = plt.hist(hist_frequencies,  histtype='bar',
                                bins = int(len(hist_frequencies)),
                                normed = False, facecolor='green', alpha=0.75)

    plt.xlabel('Bin Counts')
    plt.ylabel('Normalized Frequency')
    plt.title(arguments.t + ' Histogram')
    plt.grid(False)
    fig2.savefig(arguments.o +  '_hist.pdf')

    normalized_counts_file = arguments.o + "__normailzed_counts.tsv.gz"

    with gzip.open(normalized_counts_file, "wt") as counts_output_stream:
        line_tuples = zip(headers, normalized_frequencies, column_sums)
        print("\t".join(("#position", "Normalized_Count", "Raw_Count")),
              file=counts_output_stream)

        for line_content in line_tuples:
            print("\t".join(map(str, line_content)), file=counts_output_stream)


###############################################################################

if __name__ == '__main__':
    main()
