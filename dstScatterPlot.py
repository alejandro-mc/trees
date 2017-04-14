import glob
import os
import sys
import matplotlib.pyplot as plt
from random import random
import numpy as np
import numpy.linalg as la

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
    
    plt.subplot(121)
    for x,y in zip(__xdata__,__ydata__):
        plt.scatter(x,y,s=10,c= (random(),random(),random()),edgecolor='face',linewidths=5)
    
    #compute correlations 
    corrvals = []
    m = len(__xdata__)
    LOGX = np.log(np.array(__xdata__))
    LOGY = np.log(np.array(__ydata__) + 0.0001)#added small delta to avoid division by zero
    
    for i in range(m):
        corrvals.append(np.dot(LOGX[i],LOGY[i]) / (la.norm(LOGX[i]) * la.norm(LOGY[i]))) 
    
    
    #plot correlation histogram as a subplot
    plt.subplot(122)
    plt.hist(corrvals,100)
    
    
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