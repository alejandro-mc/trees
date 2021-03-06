#gtp_vs_lpic_Walks.py
from tree_utils import *
import os
import sys

__pid__ = 0

#daf: distance algorithm file
def randSPRwalk(daf,size,steps,runs,seed):
    global __pid__
    
    #set the seed
    random.seed(seed)
    
    out_file_name = "SPRGTP_" + str(size) + "_" + str(steps) + "_" +\
                    str(runs)  + "_" + str(seed) 
        
    #file name for lpd distance file
    out_file_name_lpd = "SPRLPD_" + str(size) + "_" + str(steps) + "_" +\
                         str(runs)  + "_" + str(seed)
    
    #create a file for each spr sequence
    for k in range(runs):
        rand_tree     = genRandBinTree(list(range(size)))
        total_nodes   = countNodes(rand_tree)
        #write current sequence to file
        infile_prefix = "tmpsprseq" + str(__pid__)
        infile        = infile_prefix + str(k)
        with open(infile,'w') as treefile:
            treefile.write(toNewickTree(rand_tree) + "\n")
            current_tree = rand_tree
            for i in range(steps):
                current_tree = randSPR(current_tree,total_nodes)[0]
                treefile.write(toNewickTree(current_tree) + "\n")
            
        #assumes GTP file is in current working directory
        outfile       = "tempseq" + str(__pid__) + ".csv"
        infile_prefix = "tmpsprseq" + str(__pid__)
        infile        = infile_prefix + str(k)
        os.system("java -jar " + daf + " -r 1 -o " + outfile + " " + infile)
        #append output to final sequence file
        os.system("cat " + outfile + " | ./toLines.py >> " + out_file_name)
        
        #compute the leaf pair distance
        outfile_lpd = "templpdseq" + str(__pid__) + ".csv"
        os.system("python lpd.py " + infile + " 1 " + outfile_lpd)
        #append output to lpd sequence file
        os.system("cat " + outfile_lpd + " | ./toLines.py >> " + out_file_name_lpd)
        
        #cleanup gtp files
        os.system("rm " + outfile)
        os.system("rm " + infile_prefix + "*")
        os.system("rm " + outfile_lpd)
        
        
if __name__=='__main__':
    if len(sys.argv)<6:
        print ("Too few arguments!!")
        print ("Usage: <distance algorithm file .jar> <size or size range> <no. SPR steps> <no. runs> <seed or seed range>")
        sys.exit(-1)
    
    dist_algo_file = sys.argv[1]
    
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
            randSPRwalk(dist_algo_file,size,steps,runs,seed)