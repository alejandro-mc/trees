from tree_utils import *
import w_tree_utils as wtu
import numpy as np
import os
import sys
from math import sqrt

__pid__ = 0
__prefix__ = "DST_"


#daf: distance algorithm file
def randTreeDistances(daf,size,runs,seed,weighted = False):
    global __pid__
    global __prefix__
    
    #set the seed
    random.seed(seed)
    if weighted:
        np.random.seed(seed)
    
    outfile = __prefix__ + str(size) + "_"+\
                       str(runs)  + "_" + str(seed) 
    
    #create a file to write all the trees
    #write current sequence to file
    infile = "tmptrees" + str(__pid__)
    with open(infile,'w') as treefile:
        if not weighted:
            for k in range(runs):
                rand_tree = genRandBinTree(list(range(size)))
                treefile.write(toNewickTree(rand_tree) + "\n")
        else:
            for k in range(runs):
                rand_tree = wtu.normalizeTree(wtu.genRandBinTree(list(range(size)),np.random.exponential),sqrt(2*(size-1)))
                treefile.write(wtu.toNewickTree(rand_tree) + "\n")
    
            
    #assumes GTP file is in current working directory
    #outfile       = "tmpdist" + str(__pid__) + ".csv"
    os.system("java -jar " + daf + " -o " + outfile + " " + infile)
    #cleanup
    os.system("rm " + infile)


if __name__=='__main__':
    if len(sys.argv)<5:
        print ("Too few arguments!!")
        print ("Usage: [-w] <distance algorithm file .jar> <size or size range> <no. runs> <seed or seed range>")
        sys.exit(-1)
    
    WEIGHTED = False
    if len(sys.argv) == 6:
        WEIGHTED = sys.argv.pop(1) == '-w'
    
    dist_algo_file = sys.argv[1]
    
    if dist_algo_file != "gtp.jar":
        __prefix__ = "DRF_"
    
    if WEIGHTED:
        __prefix__ = 'W' + __prefix__
    
    
    #take a single size or a range of sizes
    if ":" in sys.argv[2]:
        size_start, size_end = map(lambda x: int(x),sys.argv[2].split(':'))
    else:
        size_start = int(sys.argv[2])
        size_end   = size_start + 1
    
    
    size_range = range(size_start,size_end)
    
    runs  = int(sys.argv[3])
    
    #take a single seed or a range of seeds
    if ":" in sys.argv[4]:
        seed_start,seed_end = map(lambda x: int(x),sys.argv[4].split(':'))
    else:
        seed_start = int(sys.argv[4])
        seed_end   = seed_start + 1
    
    seed_range = range(seed_start,seed_end)
    
    #set pid property
    __pid__ = os.getpid()

    for size in size_range:
        for seed in seed_range:
            randTreeDistances(dist_algo_file,size,runs,seed,WEIGHTED)