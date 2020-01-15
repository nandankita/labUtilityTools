'''
Created on Nov 5, 2018

@author: nanda
'''
import heapq

class Merger():
    """
    Algorithm based on: http://stackoverflow.com/questions/5055909/algorithm-for-n-way-merge
    """
    
    def __init__(self):
        try:
            #1. create priority queue
            self._heap = []
            self._output_file = open('outputfile.out', 'w+')
            
        except Exception, err_msg:
            print "Error while creating Merger: %s" % str(err_msg)
        
    def merge(self, input_files):
        try:
            # open all files
            open_files = []
            [open_files.append(open(file__, 'r')) for file__ in input_files]

            # 2. Iterate through each file f
            # enqueue the pair (nextNumberIn(f), f) using the first value as priority key
            [heapq.heappush(self._heap, (int(file__.readline()), file__)) for file__ in open_files]   
            
            # 3. While queue not empty
            # dequeue head (m, f) of queue
            # output m
            # if f not depleted
            # enqueue (nextNumberIn(f), f)
            while(self._heap):
                # get the smallest key
                smallest = heapq.heappop(self._heap)
                # write to output file
                self._output_file.write(str(smallest[0]) + self._delimiter_value())
                # read next line from current file
                read_line = smallest[1].readline()
                # check that this file has not ended
                if(len(read_line) != 0):
                    # add next element from current file
                    heapq.heappush(self._heap, (int(read_line), smallest[1]))
            # clean up
            [file__.close() for file__ in open_files]    
            self._output_file.close()
                                    
        except Exception, err_msg:
            print "Error while merging: %s" % str(err_msg)
        
    def _delimiter_value(self):
        return "\n"

def test():
    files = ['file1.in', 'file2.in', 'file3.in']
    merger = Merger()
    merger.merge(files)

if __name__ == '__main__':
    test()