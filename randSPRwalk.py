#randSPRwalk.py
#writes random SPR walks to files
#calls GTP on each SPR random walk file to get
#the ditances between each tree and the first tree of the sequence
#the results are written to csv files with lines delimited by \t
from tree_utils import *
import os
import sys


def randSPRwalk(size,steps,runs,seed):
    #set the seed
    random.seed(seed)
    
    
    #write SPR sequence to file
    rand_tree = genRandBinTree(range(size))
    total_nodes = countNodes(rand_tree)

    #create a file for each spr sequence
    for k in range(runs):
        #write current sequence to file
        with open('sprseq' + str(k),'w') as treefile:
            treefile.write(toNewickTree(rand_tree) + "\n")
            current_tree = rand_tree
            for i in range(steps):
                current_tree = randSPR(current_tree,total_nodes)[0]
                treefile.write(toNewickTree(current_tree) + "\n")
            
        #assumes GTP file is in current working directory
        outfile = "seq" + str(k) + ".csv"
        infile  = "sprseq" + str(k)
        os.system("java -jar gtp.jar -r 1 -o " + outfile + " " + infile)


if __name__=='__main__':
    if len(sys.argv)<5:
        print ("Too few arguments!!")
        print ("Usage: <no. leaves> <no. SPR steps> <no. runs> <seed>")
        sys.exit(-1)
    
    size = sys.argv[1]
    steps = sys.argv[2]
    runs = sys.argv[3]
    seed = sys.argv[4]
    
    randSPRwalk(int(size),int(steps),int(runs),int(seed))