import glob
import os
import sys
import matplotlib.pyplot as plt
from random import random

__xdata__ = []
__ydata__ = []
__power__ = 1

def gatherStats(filenames):
    global __xdata__
    global __ydata__
    global __power__
    
    #for each file open the file add stats for each line and step
    for filename in filenames:
        
        filename2 = filename[:5] + "2" + filename[6:]
        
        with open(filename,'r') as dstfile1, open(filename2,'r') as dstfile2:
            for line1,line2 in zip(dstfile1,dstfile2):
                trimmed1   = line1[0:-1]
                distances1 = list(map(lambda x : pow(float(x),__power__) ,trimmed1.split(',')))
                
                trimmed2   = line2[0:-1]
                distances2 = list(map(lambda x : float(x) ,trimmed2.split(',')))
                
                __xdata__.append(distances1)
                __ydata__.append(distances2)
                    


def plotWalks():
    global __xdata__
    global __ydata__
    
    for x,y in zip(__xdata__,__ydata__):
        plt.scatter(x,y,s=10,c= (random(),random(),random()),edgecolor='face',linewidths=5)
    
    plt.show()


if __name__=='__main__':
    if len(sys.argv)<3:
        print ("Too few arguments!!")
        print ("Usage: <prefix> <no. leaves>")
        sys.exit(-1)

    dstfiles = glob.glob( sys.argv[1] + "1_" + sys.argv[2] + "_*")
    
    for i in dstfiles:
        print("gathering data from: " + i)
        gatherStats(dstfiles)
    
    #do domething with the stats
    plotWalks()