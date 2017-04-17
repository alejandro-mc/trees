import glob
import os
import sys
import matplotlib.pyplot as plt
from math import *
from random import random

__xdata__ = []
__ydata__ = []

def gatherStats(filenames):
    global __xdata__
    global __ydata__
    
    #for each file open the file add stats for each line and step
    for filename in filenames:
        
        filename2 = filename[:5] + "2" + filename[6:]
        print("gathering data from: " + filename,' and ', filename2)
        
        with open(filename,'r') as dist_file1, open(filename2,'r') as dist_file2:
            for line1 in dist_file1:
                
                trimmed1 = line1[0:-1]
                vals1 = trimmed1.split('\t')
                if len(vals1) == 3:
                    distance1 = float(vals1[2])
                    __xdata__.append(distance1)
            
            for line2 in dist_file2:
                
                trimmed2 = line2[0:-1]
                vals2 = trimmed2.split('\t')
                if len(vals2) == 3:
                    distance2 = float(vals2[2])
                    __ydata__.append(distance2)
            
                


def plotDists():
    global __xdata__
    global __ydata__
    
    plt.scatter(__xdata__,__ydata__,s=10,c= (random(),random(),random()),edgecolor='face',linewidths=5)
    
    plt.show()
                

if __name__=='__main__':
    if len(sys.argv)<3:
        print ("Too few arguments!!")
        print ("Usage: <prefix> <no. leaves>")
        sys.exit(-1)
   
    dstfiles = glob.glob( sys.argv[1] + "1_" + sys.argv[2] + "_*")
        
    gatherStats(dstfiles)
    
    #plot the data
    plotDists()