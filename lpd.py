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
    

def writeSeqDistsancesToFile(tfname,index,ofname):
    
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
        
        #count the number of leaf pairs (cherries) 
        #the reference tree has in common with the current tree
        count = 0
        for p in currentleafset:#for each leaf pair in the current tree
            if leafset_ref.get(p,False):#if the pair is in the original tree
                count +=1#count it
        
        #the distance is the fraction of leaf pairs that ref has in common with
        #the current tree
        dists.append(1 - (count / refpair_count))
    
    
    #write distances to file
    with open(ofname,'w') as outfile:
        for i in range(len(dists)):
            outfile.write(str(index) + '\t' + str(index + 1 + i) + '\t' + str(dists[i]) + '\n')
            
def writeAllDistsancesToFile(tfname,ofname):
    
    dists    = []
    leafsets = []
    
    with open(tfname,'r') as treefile:    
        lines = treefile.readlines()
    
    def appendLeafs(p):#appends leaves to currentleafset **dictionary**
        sortedLeaves = sorted(p)
        currentleafset[(sortedLeaves[0],sortedLeaves[1])] = True
    
    #get leaf pair set for each tree and store in leafsets
    for line in lines:
        current_tree = newickToNestedLst(line[:-1].replace(';',''))
        currentleafset = {}
        getLeafPairs(current_tree,appendLeafs)
        leafsets.append(currentleafset)
    
    #for each pair of tree leafsets compute the distance 
    #as the |leafpairs in comon - no. of leaf pairs of the most balanced of the two trees|
    #print(leafsets)
    for i in range(len(leafsets)):
        for j in range(i+1,len(leafsets)):
            #set leaf set 1 and two s.t. len(leafset2) > len(leafset1)
            leafset1,leafset2 = sorted([leafsets[i],leafsets[j]],key=(lambda x: len(x)))
            
            #count leafsets in common
            count = 0
            for p in leafset1:
                if leafset2.get(p,False):
                    count +=1
            
            #compute the distance as the ratio 1 - (leafs in common / no. leaf pairs for both trees)
            dists.append(1 - (float(2*count) / float(len(leafset1) + len(leafset2))))
            
    #write distances to file
    with open(ofname,'w') as outfile:
        k=0
        for i in range(len(leafsets)):
            for j in range(i+1,len(leafsets)):
                outfile.write(str(i) + '\t' + str(j) + '\t' + str(dists[k]) + '\n')
                #print(str(i) + '\t' + str(j) + '\t' + str(dists[k]) + '\n')
                k+=1
            

if __name__=='__main__':
    if len(sys.argv)<4:
        print ("Too few arguments!!")
        print ("Usage: <tree file name> <init tree index> <output file name> <-a :to compute intertree distances, nothing otherwise>")
        sys.exit(-1)
    
    tfname = sys.argv[1]
    index  = int(sys.argv[2])
    ofname = sys.argv[3]
    
    #select all intertree distances or distances relative to tree(i)
    if len(sys.argv) == 5:
        if sys.argv[4] == '-a':
            writeAllDistsancesToFile(tfname,ofname)
        else:
            print("Parameter 4 must be -a or empty")
            sys.exit(-1)
    else:
        writeSeqDistsancesToFile(tfname,index,ofname)
        
        