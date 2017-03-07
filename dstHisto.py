import glob
import os
import sys
import matplotlib.pyplot as plt
from math import *

__stats__ = []


def gatherStats(filenames):
    global __stats__
    
    #for each file open the file add stats for each line and step
    for filename in filenames:
        with open(filename,'r') as dist_file:
            for line in dist_file:
                stripped = line[0:-1]
                vals = stripped.split('\t')
                if len(vals) == 3:
                    distance = float(vals[2])
                    __stats__.append(distance)


def plotHistogram(bincount):
    global __stats__
    
    plt.hist(__stats__,bins=bincount)
    plt.show()
                

if __name__=='__main__':
    if len(sys.argv)<3:
        print ("Too few arguments!!")
        print ("Usage: <no. leaves> <no. bins>")
        sys.exit(-1)
    
    bincount = int(sys.argv[2])
    
    files = glob.glob( "DST_" + sys.argv[1] + "_*")
    
    for i in files:
        print("gathering data from: " + i)
        gatherStats(files)
    
    #do domething with the stats
    plotHistogram(bincount)