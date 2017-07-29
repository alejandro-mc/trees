import numpy as np
import random
import os
import sys
from math import sqrt

__pid__ = 0

#daf1: distance algorithm file
def randTreeDistances(daf1,daf2,size,runs,seed,weighted=False):
    global __pid__
    global __prefix__
    
    #set the seed
    random.seed(seed)
    np.random.seed(seed)
    
    #compose output file name
    outpref = 'DST' + daf1[0].upper() + daf2[0].upper()
    
    #prepend the weighted prefix
    if weighted:
        outpref = 'W' + outpref
    else:
        outpref = 'U' + outpref
    
    
    #select toNewickTree,randSPR,treeNorm, and genRandBinTree functions
    #from the correct tree utils module
    if weighted:
        from w_tree_utils import toNewickTree,randNNI,treeNorm
        import w_tree_utils as wtu
        genRandBinTree = lambda leaves: wtu.genRandBinTree(leaves,np.random.exponential)
    else:
        from tree_utils import toNewickTree,randNNI,genRandBinTree
        treeNorm = lambda x: 0.25
    
        
    #file name for first dst file
    out_file_name1 = outpref + "1_" + str(size) + "_" + str(runs)  + "_" + str(seed) 
        
    #file name for second dst file
    out_file_name2 = outpref + "2_" + str(size) + "_" + str(runs)  + "_" + str(seed)
    
    
    #verify that files don't exist
    dirlist = os.listdir()
    if (out_file_name1 in dirlist or out_file_name2 in dirlist):
        print("Files", out_file_name1,"or",out_file_name2,"already exist in this directory.")
        return
    
    #create a file to write all the trees
    #write current sequence to file
    infile = "tmptrees" + str(__pid__)
    with open(infile,'w') as treefile:
        for k in range(runs):
            rand_tree = genRandBinTree(list(range(size)))
            treefile.write(toNewickTree(rand_tree) + "\n")
    
   
    #assumes GTP file is in current working directory
    os.system("java -jar " + daf1 + " -o " + out_file_name1 + " " + infile)
    
    
    #compute other distance
    if daf2.split('.')[1] == 'py':
        os.system("python lpd.py " + infile + " 0 " + out_file_name2 + " -a")
    else:
        os.system("java -jar " + daf2 + " -o " + out_file_name2 + " " + infile)
    
    #cleanup
    os.system("rm " + infile)    
    

if __name__=='__main__':
    if len(sys.argv)<5:
        print ("Too few arguments!!")
        print ("Usage: [-w] <GR GL or RL> <size or size range> <no. runs> <seed or seed range>")
        sys.exit(-1)
        
    WEIGHTED = False
    if len(sys.argv) == 6:
        WEIGHTED = sys.argv.pop(1) == '-w'
     
    #select distance algorithm file according to code
    code = sys.argv[1]
    code = code.upper()
    
    if code[0] == 'G':
        dist_algo_file1 = 'gtp.jar'
    elif code[0] == 'R':
        dist_algo_file1 = 'rfd.jar'
    
    if code[1] == 'L':
        dist_algo_file2 = 'lpd.py'
    elif code[1] == 'R':
        dist_algo_file2 = 'rfd.jar'    
        
    
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
            randTreeDistances(dist_algo_file1,dist_algo_file2,size,runs,seed,WEIGHTED)