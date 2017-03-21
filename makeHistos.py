import glob
import os
import sys
import matplotlib.pyplot as plt
from math import *

__stats__ = []#[min,max,histo]

#histogram settings
__min__ = 0
__max__ = 0
__bincount__ = 0

class histogram:
    def __init__(self,bincount,maximum,minimum):
        self.bincount = bincount
        self.minimum  = minimum
        self.maximum  = maximum
        self.count    = 0
        self.bins     = [0] * bincount #bins get init to zero
        
        self.__binmapfactor__ = bincount / (maximum - minimum)
        
    def addData(self,data_point):
        
        #map data point to a bin
        point_bin = int(data_point * self.__binmapfactor__)
        print("data_point: ",data_point,"point_bin: ",point_bin)
        print("bin has")
        
        self.bins[point_bin] += 1
        self.count +=1
        #print(self.bins)
    
    def getPercentiles(self):
        percentiles = []
        binsize = (self.maximum - self.minimum) / self.bincount 
        
        #get 0.25 percentile
        t1 =  self.count * 0.25
        curr_bin = 0
        count = 0
        while count < t1:
            count += self.bins[curr_bin]
            curr_bin +=1
        
        percentiles.append(curr_bin * binsize)
        
        #get 0.5 percentile
        t2 =  self.count * 0.5
        while count < t2:
            count += self.bins[curr_bin]
            curr_bin +=1
            
        percentiles.append(curr_bin * binsize)
        
        #get 0.75 percentile
        t3 =  self.count * 0.75
        while count < t3:
            count += self.bins[curr_bin]
            curr_bin +=1
            
        percentiles.append(curr_bin * binsize)
        
        
        return percentiles
    

#stat is a list of the form [min,max,histogram]
def updateStat(stat,data_pt):
    statmin,statmax,histo = stat
    #print(statmin,statmax,histo)
    newstat = []
    
    newstat.append(min(statmin,data_pt))
    newstat.append(max(statmax,data_pt))
    
    #update histogram
    histo.addData(data_pt)
    newstat.append(histo)
    
    return newstat


def gatherStats(filenames):
    global __stats__
    global __min__
    global __max__
    global __bincount__
    
    #for each file open the file add stats for each line and step
    for filename in filenames:
        with open(filename,'r') as sprfile:
            for line in sprfile:
                trimmed   = line[0:-1]
                distances = list(map(lambda x : float(x) ,trimmed.split(',')))
                for i in range(len(distances)):
                    
                    if i < len(__stats__):
                        __stats__[i] = updateStat(__stats__[i],distances[i])
                    else:
                        newstat = [distances[i]] * 2
                        
                        hist    = histogram(__bincount__,__max__,__min__)
                        hist.addData(distances[1])
                        newstat.append(hist)
                        
                        __stats__.append(newstat)


def firstN(n):
    return __stats__[0:n]


#stats: [[p25,median,p75,miny,maxy] ,... ]
def get_boxplot_from_stats(stats):
    
    #create boxplot instance with len(stats) boxes
    boxplot = plt.boxplot([[]]*len(stats))
    
    box_no = 0
    for p25,median,p75,miny,maxy in stats:
        
        #set caps
        boxplot['caps'][2*box_no].set_ydata([miny,miny])#lower
        boxplot['caps'][2*box_no + 1].set_ydata([maxy,maxy])#higher
        
        #set medians
        boxplot['medians'][box_no].set_ydata([median,median])
        
        #set whiskers
        boxplot['whiskers'][2*box_no].set_ydata([miny,p25])
        boxplot['whiskers'][2*box_no + 1].set_ydata([p75,maxy])
        
        #set box
        boxplot['boxes'][box_no].set_ydata([p25,p25,p75,p75,p25])
        
        box_no +=1
    
    return boxplot


def plotWalks():
    global __max__
    
    minmax = [[s[0],s[1]] for s in firstN(19)]
    histograms = [s[2] for s in firstN(19)]
    percentiles    = [h.getPercentiles() for h in histograms]
    #medians  = list(map(lambda s: s[1],stats))
    #intervals = list(map(lambda s: [s[0],s[2]],stats))
    stats = [ p + mm for p,mm in zip(percentiles,minmax)]
    #plt.boxplot(data,usermedians=medians)
    #print(zip(minmax,stats))
    get_boxplot_from_stats(stats)
    plt.axis([0,20,0,__max__])
    plt.show()


if __name__=='__main__':
    if len(sys.argv)<4:
        print ("Too few arguments!!")
        print ("Usage: <prefix> <no. leaves> <bin count>")
        sys.exit(-1)
    
    #set up histogram parameters
    leaves  = int(sys.argv[2])
    __max__      = 2 * sqrt(leaves - 1)
    __min__      = 0
    __bincount__ = int(sys.argv[3])
    
    files = glob.glob( sys.argv[1] + "_" + sys.argv[2] + "_*")
    
    for i in files:
        print("gathering data from: " + i)
        gatherStats(files)
    
    #do domething with the stats
    plotWalks()