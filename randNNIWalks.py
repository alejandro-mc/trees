#randNNIWalks.py
#writes random SPR walks to files
#calls GTP on each NNI random walk file to get
#the ditances between each tree and the first tree of the sequence
#the results are written to csv files with lines delimited by \t
import tree_utils as tu
import w_tree_utils as wtu
import os
import sys
import numpy as np
import random
from math import sqrt

__pid__ = 0
__prefix__ = "NNI_"

#daf: distance algorithm file
def randNNIwalk(daf,size,steps,runs,seed,weighted = False):
    global __pid__
    global __prefix__
    
    #set the seed
    random.seed(seed)
    np.random.seed(seed)
    
    #select tree utils module
    if weighted:
        tum = wtu
        genRandBinTree = lambda leaves: wtu.genRandBinTree(leaves,np.random.exponential)
    else:
        tum = tu
        genRandBinTree = lambda leaves: tu.genRandBinTree(leaves)
        tum.treeNorm = lambda x: 0.25
    
    out_file_name = __prefix__ + str(size) + "_" + str(steps) + "_" +\
                    str(runs)  + "_" + str(seed) 
    
    normsfile_name = out_file_name + '.norms'
    
    #create a file for each spr sequence
    for k in range(runs):
        rand_tree     = genRandBinTree(list(range(size)))
        total_nodes   = size-1
        #write current sequence to file
        infile_prefix = "tmpnniseq" + str(__pid__)
        infile        = infile_prefix + str(k)
        with open(infile,'w') as treefile, open(normsfile_name,'w') as nrmfile:
            treefile.write(tum.toNewickTree(rand_tree) + "\n")
            current_tree = rand_tree
            
            #write tree norms-----
            #save norm of first tree
            norm1 = sqrt(tum.treeNorm(rand_tree))
            walknorms = ''
            
            
            for i in range(steps):
                current_tree = tum.randNNI(current_tree,total_nodes)
                treefile.write(tum.toNewickTree(current_tree) + "\n")
                
                #write ||T1|| + ||T2||
                walknorms += str(norm1 + sqrt(tum.treeNorm(current_tree))) + ',' 
            
            #write norms sequence
            nrmfile.write(walknorms[0:-1] + '\n')
            
        #assumes GTP file is in current working directory
        outfile       = "tempseq" + str(__pid__) + ".csv"
        infile_prefix = "tmpnniseq" + str(__pid__)
        infile        = infile_prefix + str(k)
        os.system("java -jar " + daf + " -r 0 -o " + outfile + " " + infile)
        #append output to final sequence file
        os.system("cat " + outfile + " | ./toLines.py >> " + out_file_name)
        #cleanup
        os.system("rm " + outfile)
        os.system("rm " + infile_prefix + "*")


if __name__=='__main__':
    if len(sys.argv)<6:
        print ("Too few arguments!!")
        print ("Usage: [-w] <distance algorithm file .jar> <size or size range> <no. NNI steps> <no. runs> <seed or seed range>")
        sys.exit(-1)
    
    WEIGHTED = False
    if len(sys.argv) == 7:
        WEIGHTED = sys.argv.pop(1) == '-w'
    
    dist_algo_file = sys.argv[1]
    
    if dist_algo_file != "gtp.jar":
        __prefix__ = "RNI_"
    
    
    if WEIGHTED:
        __prefix__ = 'W' + __prefix__
    else:
        __prefix__ = 'U' + __prefix__
    
    #take a single size or a range of sizes
    if ":" in sys.argv[2]:
        size_start, size_end = map(lambda x: int(x),sys.argv[2].split(':'))
    else:
        size_start = int(sys.argv[2])
        size_end   = size_start + 1
    
    
    size_range = range(size_start,size_end)
    
    steps = int(sys.argv[3])
    runs  = int(sys.argv[4])
    
    #take a single seed or a range of seeds
    if ":" in sys.argv[5]:
        seed_start,seed_end = map(lambda x: int(x),sys.argv[5].split(':'))
    else:
        seed_start = int(sys.argv[5])
        seed_end   = seed_start + 1
    
    seed_range = range(seed_start,seed_end)
    
    #set pid property before calling randSPRWalk
    __pid__ = os.getpid()

    for size in size_range:
        for seed in seed_range:
            randNNIwalk(dist_algo_file,size,steps,runs,seed,WEIGHTED)