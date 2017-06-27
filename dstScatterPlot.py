import glob
import os
import sys
import matplotlib.pyplot as plt
from random import random
import numpy as np
import numpy.linalg as la
from functools import reduce

__xdata__ = []
__ydata__ = []
__power__ = 1

def gatherStats(filenames):
    global __xdata__
    global __ydata__
    global __power__
    
    #for each file open the file add stats for each line and step
    for filename in filenames:
        
        #check for norm files and load values to list
        normsfile_name = filename + '.norms'
        if os.path.isfile(normsfile_name):
            def norm_stream(): 
                with open(normsfile_name,'r') as nrmfile:
                    for line in nrmfile:
                        trimmed = line[0:-1]
                        norms = list(map(lambda x : float(x) ,trimmed.split(',')))
                        for i in range(len(norms)):
                            yield norms[i]
        else:
            def norm_stream():
                while True:
                    yield 1
        
        
        filename2 = filename[:6] + "2" + filename[7:]
        
        with open(filename,'r') as dstfile1, open(filename2,'r') as dstfile2:
            
            #display filenames being processed
            print("gathering data from: ",filename,"and",filename2)
            
            for line1,line2 in zip(dstfile1,dstfile2):
                trimmed1   = line1[0:-1]
                distances1 = list(map(lambda x : pow(float(x),__power__) ,trimmed1.split(',')))
                
                trimmed2   = line2[0:-1]
                distances2 = list(map(lambda x : float(x) ,trimmed2.split(',')))
                
                #nomalize distances
                norm_dist1=[]
                norm_dist2 =[]
                for dst1,dst2 in zip(distances1,distances2):
                    norm = next(norm_stream())
                    norm_dist1.append(dst1 / norm)
                    norm_dist2.append(dst2 / norm)
                
                #remove zero distances
                filtered_dst1 = []
                filtered_dst2 = []
                for dst1,dst2 in zip(norm_dist1,norm_dist2):
                    if dst1 != 0 and dst2 != 0:
                        filtered_dst1.append(dst1)
                        filtered_dst2.append(dst2)
                
                #add filteres distance sequences to data
                __xdata__.append(filtered_dst1)
                __ydata__.append(filtered_dst2)
                    


def plotWalks():
    global __xdata__
    global __ydata__
    
    plt.subplot(121)
    
    LOGX = [[np.log(j) for j in i] for i in __xdata__]
    LOGY = [[np.log(j) for j in i] for i in __ydata__]
    
    
    for x,y in zip(LOGX,LOGY):
        plt.scatter(x,y,s=10,c= (random(),random(),random()),edgecolor='face',linewidths=5)
    
    
    #compute correlations and 
    corrvals = []
    m = len(__xdata__)
    
    
    #fit line through log of points
    flat_logx = reduce(lambda a,b: a+b,LOGX,[])#flatten LOGX
    flat_logy = reduce(lambda a,b: a+b,LOGY,[])#flatten LOGY
    
    A = np.vstack([flat_logx ,np.ones(len(flat_logx))]).T
    theta1,theta0 = la.lstsq(A,flat_logy)[0]
    print(theta1,theta0)#print parameters
    
    #plot fitted line
    x0 = int(min(LOGX[0]))
    xn = int(max(LOGX[0]))
    fitx = np.arange(x0,xn,0.1)
    plt.plot(fitx,theta1*fitx + theta0)
    
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
    dstfiles = list(filter(lambda x: '.norms' not in x,dstfiles))
    
    gatherStats(dstfiles)

    
    #do domething with the stats
    plotWalks()