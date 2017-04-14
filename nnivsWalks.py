#gtp_vs_lpic_Walks.py
from tree_utils import *
import os
import sys

__pid__ = 0

#daf: distance algorithm file
def randNNIwalk(daf1,daf2,size,steps,runs,seed):
    global __pid__
    
    #set the seed
    random.seed(seed)
    
    outpref = 'NNI' + daf1[0].upper() + daf2[0].upper()
        
    out_file_name = outpref + "1_" + str(size) + "_" + str(steps) + "_" +\
                    str(runs)  + "_" + str(seed) 
        
    #file name for lpd distance file
    out_file_name2 = outpref + "2_" + str(size) + "_" + str(steps) + "_" +\
                         str(runs)  + "_" + str(seed)
    
    #create a file for each nni sequence
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
        os.system("java -jar " + daf1 + " -r 1 -o " + outfile + " " + infile)
        #append output to final sequence file
        os.system("cat " + outfile + " | ./toLines.py >> " + out_file_name)
        
        #compute other distance
        outfile2 = "tempnniseq2" + str(__pid__) + ".csv"
        if daf2.split('.')[1] == 'py':
            os.system("python lpd.py " + infile + " 1 " + outfile2)
        else:
            os.system("java -jar " + daf2 + " -r 1 -o " + outfile2 + " " + infile)
        
        #append output to second sequence file
        os.system("cat " + outfile2 + " | ./toLines.py >> " + out_file_name2)
        
        #cleanup gtp files
        os.system("rm " + outfile)
        os.system("rm " + infile_prefix + "*")
        os.system("rm " + outfile2)
        
        
if __name__=='__main__':
    if len(sys.argv)<6:
        print ("Too few arguments!!")
        print ("Usage: <GR GL or RL> <size or size range> <no. NNI steps> <no. runs> <seed or seed range>")
        sys.exit(-1)
    
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
    
    
    #dist_algo_file = sys.argv[1]
    
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
    
    #set pid property before calling randNNIWalk
    __pid__ = os.getpid()

    for size in size_range:
        for seed in seed_range:
            randNNIwalk(dist_algo_file1,dist_algo_file2,size,steps,runs,seed)