import glob
import os
import sys
import matplotlib.pyplot as plt

__xdata__ = []
__ydata__ = []

def gatherStats(filenames):
    global __xdata__
    global __ydata__
    
    #for each file open the file add stats for each line and step
    for filename in filenames:
        
        lpddists_filename = "SPRLPD" + filename[6:]
        
        with open(filename,'r') as sprfile, open(lpddists_filename,'r') as lpdfile:
            for gtpline,lpdline in zip(sprfile,lpdfile):
                gtptrimmed   = gtpline[0:-1]
                gtpdistances = list(map(lambda x : float(x) ,gtptrimmed.split(',')))
                
                lpdtrimmed   = lpdline[0:-1]
                lpddistances = list(map(lambda x : float(x) ,lpdtrimmed.split(',')))
                
                __xdata__.append(gtpdistances)
                __ydata__.append(lpddistances)
                    


def plotWalks():
    global __xdata__
    global __ydata__
    
    for x,y in zip(__xdata__,__ydata__):
        plt.scatter(x,y)
    
    plt.show()


if __name__=='__main__':
    if len(sys.argv)<3:
        print ("Too few arguments!!")
        print ("Usage: <prefix> <no. leaves>")
        sys.exit(-1)

    spr_files = glob.glob( sys.argv[1] + "_" + sys.argv[2] + "_*")
    
    for i in spr_files:
        print("gathering data from: " + i)
        gatherStats(spr_files)
    
    #do domething with the stats
    plotWalks()