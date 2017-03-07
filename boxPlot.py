import glob
import os
import sys
import matplotlib.pyplot as plt

__stats__ = []

def gatherStats(filenames):
    global __stats__
    
    #for each file open the file add stats for each line and step
    for filename in filenames:
        with open(filename,'r') as sprfile:
            for line in sprfile:
                trimmed   = line[0:-1]
                distances = list(map(lambda x : float(x) ,trimmed.split(',')))
                for i in range(len(distances)):
                    #add distance data to stats
                    #for now we just add to the list
                    #later will contain min max and histogram to handle
                    #large ammounts of data efficiently
                    if i < len(__stats__):
                        __stats__[i].append(distances[i])
                    else:
                        __stats__.append([distances[i]])
    

def firstN(n):
    return __stats__[0:n]

def plotWalks():
    plt.boxplot(firstN(20))
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