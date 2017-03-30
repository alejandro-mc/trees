#computes the distance between two trees
#based on the number of leaves in common
from tree_utils import *
import os
import sys


#insertpairs is a function that adds pairs to a collection
#i.e. a dictionary or a list
#tree is a nested list representation of a tree
def getLeafPairs(tree,insertpairs):
    
    #recurse over the tree
    def findPair(tree):
        
        if not (isinstance(tree[0],list) or isinstance(tree[1],list)):#if we have a leaf pair
            insertpairs(tree)
        
        if isinstance(tree[0],list):
            findPair(tree[0])
        
        if isinstance(tree[1],list):
            findPair(tree[1])
    
    findPair(tree)
    

def writeDistsancesToFile(tfname,index,ofname):
    
    dists = []
    
    with open(tfname,'r') as treefile:    
        lines = treefile.readlines()
    
    #get first tree
    linei    = lines[index]
    tree1    = newickToNestedLst(linei[:-1].replace(';',''))
    leafset_ref = {}
    refpair_count = 0
    def insertRefpair(p):#insert leaf siblings as dictionary keys and updates refpair_count
        nonlocal refpair_count
        sortedLeaves = sorted(p)
        leafset_ref[(sortedLeaves[0],sortedLeaves[1])] =  True
        refpair_count += 1
    
    #find reference leaf set
    getLeafPairs(tree1,insertRefpair)
    
    def appendLeafs(p):#appends leaves to currentleafset list
        sortedLeaves = sorted(p)
        currentleafset.append((sortedLeaves[0],sortedLeaves[1]))
    
    for line in lines[index+1:]:
        
        current_tree = newickToNestedLst(line[:-1].replace(';',''))
        currentleafset = []
        getLeafPairs(current_tree,appendLeafs)
        
        count = 0
        for p in currentleafset:
            if leafset_ref.get(p,False):
                count +=1
        
        #the distance is no. leaf pairs of ref - count
        dists.append(refpair_count - count)
    
    
    #write distances to file
    with open(ofname,'w') as outfile:
        for i in range(len(dists)):
            outfile.write(str(index) + '\t' + str(index + 1 + i) + '\t' + str(dists[i]) + '\n')
            
            

if __name__=='__main__':
    if len(sys.argv)<4:
        print ("Too few arguments!!")
        print ("Usage: <tree file name> <init tree index> <output file name>")
        sys.exit(-1)
    
    tfname = sys.argv[1]
    index  = int(sys.argv[2])
    ofname = sys.argv[3]
    writeDistsancesToFile(tfname,index,ofname)
        
        