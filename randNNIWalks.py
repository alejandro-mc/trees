#randNNIWalks.py
#writes random SPR walks to files
#calls GTP on each NNI random walk file to get
#the ditances between each tree and the first tree of the sequence
#the results are written to csv files with lines delimited by \t
from tree_utils import *
import os
import sys

__pid__ = 0

def randNNIwalk(size,steps,runs,seed):
    global __pid__
    
    #set the seed
    random.seed(seed)
    
    out_file_name = "NNI_" + str(size) + "_" + str(steps) + "_" +\
                    str(runs)  + "_" + str(seed) 
    
    #create a file for each spr sequence
    for k in range(runs):
        rand_tree     = genRandBinTree(list(range(size)))
        total_nodes   = countNodes(rand_tree)
        #write current sequence to file
        infile_prefix = "tmpnniseq" + str(__pid__)
        infile        = infile_prefix + str(k)
        with open(infile,'w') as treefile:
            treefile.write(toNewickTree(rand_tree) + "\n")
            current_tree = rand_tree
            for i in range(steps):
                current_tree = randNNI(current_tree,total_nodes)
                treefile.write(toNewickTree(current_tree) + "\n")
            
        #assumes GTP file is in current working directory
        outfile       = "tempseq" + str(__pid__) + ".csv"
        infile_prefix = "tmpnniseq" + str(__pid__)
        infile        = infile_prefix + str(k)
        os.system("java -jar gtp.jar -r 1 -o " + outfile + " " + infile)
        #append output to final sequence file
        os.system("cat " + outfile + " | ./toLines.py >> " + out_file_name)
        #cleanup
        os.system("rm " + outfile)
        os.system("rm " + infile_prefix + "*")


if __name__=='__main__':
    if len(sys.argv)<5:
        print ("Too few arguments!!")
        print ("Usage: <size or size range> <no. NNI steps> <no. runs> <seed or seed range>")
        sys.exit(-1)
    
    #take a single size or a range of sizes
    if ":" in sys.argv[1]:
        size_start, size_end = map(lambda x: int(x),sys.argv[1].split(':'))
    else:
        size_start = int(sys.argv[1])
        size_end   = size_start + 1
    
    
    size_range = range(size_start,size_end)
    
    steps = int(sys.argv[2])
    runs  = int(sys.argv[3])
    
    #take a single seed or a range of seeds
    if ":" in sys.argv[4]:
        seed_start,seed_end = map(lambda x: int(x),sys.argv[4].split(':'))
    else:
        seed_start = int(sys.argv[4])
        seed_end   = seed_start + 1
    
    seed_range = range(seed_start,seed_end)
    
    #set pid property before calling randSPRWalk
    __pid__ = os.getpid()

    for size in size_range:
        for seed in seed_range:
            randNNIwalk(size,steps,runs,seed)