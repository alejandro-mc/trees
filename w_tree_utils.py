import random
import numpy as np
from math import ceil
from math import factorial
random.seed()


#functions to access useful parameters of a weighted tree
def leftSubtree(tree):
    children = tree[0]
    return children[0]

def rightSubtree(tree):
    children = tree[0]
    return children[1]

def children(tree):
    return tree[0]

#the stem weight is the weight of the edge connecting tree to it's parent
def stem_weight(tree):
    return tree[1]

#functions to perform tree rotations or NNI moves
def rotateLeft(tree):
    #
    lS = leftSubtree
    rS = rightSubtree
    sW = stem_weight
    return [[[[lS(tree),lS(rS(tree))],sW(rS(tree))],rS(rS(tree))],sW(tree)] 

def rotateRight(tree):
    lS = leftSubtree
    rS = rightSubtree
    sW = stem_weight
    return [[lS(lS(tree)),[[rS(lS(tree)),rS(tree)], sW(lS(tree)) ]], sW(tree)]

#return rotated subtree if it can be rotated
#otherwise returns []
def randRotate(tree):
    
    actions = []
    
    if isinstance(children(leftSubtree(tree)),list):
        actions.append(rotateRight)
    
    if isinstance(children(rightSubtree(tree)),list):
        actions.append(rotateLeft)
    
    length = len(actions) 
    if length != 0:
        return actions[random.randint(0,length -1)](tree)
    else:
        return []


__rotation_performed__ = False

def rotateNode(tree,targetNode,i):
    global __rotation_performed__
    #base cases
    
    #leaf
    if not isinstance(children(tree),list):
        return (tree,i-1)
    
    #target node reached
    if targetNode == i:
        rotated = randRotate(tree)
        if rotated != []:
            __rotation_performed__ = True
            return (rotated,i+1)
        else:
            return (tree,i)
    
    #rotation performed
    if targetNode < i:
        return (tree,i)
    
    #recursive calls
    left,j  = rotateNode(leftSubtree(tree),targetNode,i+1)
    right,k = rotateNode(rightSubtree(tree),targetNode,j+1)
    
    stem_weight = tree[1]
    return ([[left,right],stem_weight],k)
    
#perform a random NNI move
def randNNI(tree,total_nodes):
    
    global __rotation_performed__
    __rotation_performed__ = False
    
    while True:
        targetNode = random.randint(1,total_nodes)
        [rotated,_],_ = rotateNode([tree,0],targetNode,1)
        if __rotation_performed__:
            return rotated


#generates a binary tree
#randdist is the distribution function to generate edge lengths/weights
def genRandBinTree(leaves,randdist):
    
    while len(leaves) > 1:
        #pick two random elements
        a = random.randint(0,len(leaves)-1)
        sibling1 = [leaves[a],randdist()]
        del leaves[a]
        b = random.randint(0,len(leaves)-1)
        sibling2 = [leaves[b],randdist()]
        del leaves[b]
        
        leaves.append([sibling1,sibling2])
        
    return leaves[0]


#convert tree to Newick format
def toNewickSubTree(tree):
    
    #case leaf reached
    if not isinstance(tree[0],list):
        return str(tree[0]) + ':' + str(tree[1]) 
    
    ntree = "("
    for subtree in tree[0]:
        ntree += toNewickSubTree(subtree) + ","
    
    return ntree[0:-1] + "):" + str(tree[1])

def toNewickTree(tree):
    ntree = "("
    for subtree in tree:
        ntree += toNewickSubTree(subtree) + ","
    return ntree[0:-1] + ")"

def newickToNestedLst(newick_tree):
    return eval(newick_tree.replace(":1","").replace("(","[").replace(")","]"))



#create count nodes
def countNodes(tree):
    if not isinstance(tree[0],list):
        return 0
    
    return 1 + countNodes(tree[0][0]) + countNodes(tree[0][1])


def branchNorm(branch):
    
    #base case
    if not isinstance(branch[0],list):#leaf
        return branch[1]**2
    
    
    left_child  = branch[0][0]
    right_child = branch[0][1]
    stem_weight = branch[1]
    
    #recursive
    return stem_weight**2 + branchNorm(left_child) + branchNorm(right_child)


def treeNorm(tree):
    return branchNorm(tree[0]) + branchNorm(tree[1])

#perform random SPR move
__prunedbranch__ = []
__prunelevel__ = -1
def randSPR(tree,total_nodes):
    global __prunedbranch__
    global __prunelevel__ 
    __prunelevel__ = -1
    
    targetNode = random.randint(1,total_nodes)
    pruned,n = __prune__([tree,0],targetNode,0)
    
    if not isinstance(pruned[0],list):#if the pruned tree is a leaf return the original tree
        return (tree,0) 
    elif len(pruned[0]) < 2:
        return (tree,0)
    
    targetNode = random.randint(1,total_nodes - countNodes(__prunedbranch__) - 1)
        
    [newtree,_],_ = __regraft__(pruned,targetNode,0) 
    return newtree,0



def __prune__(tree,targetNode,visited_nodes):
    global __prunedbranch__
    global __prunelevel__
    
    __prunelevel__ += 1 #tree level increases with every call
    
    #basecases
    
    #tree is a leaf
    if not isinstance(tree[0],list):
        __prunelevel__ -= 1
        return (tree,visited_nodes + 0)#no nodes where visited no pruning
    
    #we don't want to visit any nodes after target node has been reached
    if targetNode == visited_nodes:
        __prunelevel__ -= 1
        return (tree,visited_nodes + 0)
    
    #(not a leaf) or (target not reached) ==> node visited
    #therefore we count current node as visited and write visited_nodes+1
    
    #node to be pruned
    if  targetNode == visited_nodes+1:
        
        #special case adjacent to root
        if __prunelevel__ == 0:
            whichBranch = random.randint(0,1)
            __prunedbranch__ = tree[0][whichBranch]
            weight_other_branch = tree[0][not whichBranch][1]
            __prunedbranch__[1] += weight_other_branch
            
            #return pruned subtree as root
            notpruned = tree[0][not whichBranch]
            stemless = notpruned[0]#remove branch stem
            __prunelevel__ -= 1
            return ([stemless,0],visited_nodes+1)
        
        
        #general case----------------------
        
        #[[[A,w1],[B,w2]],w3]
        #WLOG let the selected branch be [B,w2]
        whichBranch = random.randint(0,1)
        __prunedbranch__ = tree[0][whichBranch]
        #return pruned subtree
        #[A,w1+w3]
        notpruned =  tree[0][not whichBranch]
        A = notpruned[0]
        w1 = notpruned[1]
        w3 = tree[1]
        __prunelevel__ -= 1
        return ([A,w1+w3],visited_nodes+1)
    

    
    #recursive step
    subtree1, visited_nodes1 = __prune__(tree[0][0],targetNode,visited_nodes + 1)
    subtree2, visited_nodes2 = __prune__(tree[0][1],targetNode,visited_nodes1)
    #visited_nodes2 is the total
    return ([[subtree1,subtree2],tree[1]],visited_nodes2)


#__regraft__ uses the same logic as __prune__ except it performs a different
#operation on the target node
def __regraft__(tree,targetNode,visited_nodes):
    global __prunedbranch__
    #basecases
    
    #tree is a leaf
    if not isinstance(tree[0],list):
        return (tree,visited_nodes + 0)#no nodes where visited no pruning
    
    #we don't want to visit any nodes after target node has been reached
    if targetNode == visited_nodes:
        return (tree,visited_nodes + 0)
    
    #(not a leaf) or (target not reached) ==> node visited
    #therefore we count current node as visited and write visited_nodes+1
    
    #attach to edge after targetNode
    
    
    if  targetNode == visited_nodes+1:
        alpha = random.random()
        
        leftbranch  = tree[0][0]
        rightbranch = tree[0][1]
        
        A  = leftbranch[0]
        w1 = leftbranch[1]
        
        B  = rightbranch[0]
        w2 = rightbranch[1]
        
        w3 = tree[1]
        
        if random.randint(0,1) == 0:
            #insert __prunedbranch__ at A
            #[[[A,w1],[B,w2]],w3] --> [[ [[[A,alpha*w1],__prunedbranch__],(1-alpha)*w1]  ,[B,w2]],w3] 
            return ([[ [[[A,alpha*w1],__prunedbranch__],(1-alpha)*w1],
                       rightbranch], w3], visited_nodes+1)
        else:
            #insert __prunedbranch__ at B
            #[[[A,w1],[B,w2]],w3] --> [[  [A,w1],[[[B,alpha*w2],__prunedbranch__],(1-alpha)*w2]],w3]
            return ([[ leftbranch,
                       [[[B,alpha*w2],__prunedbranch__],(1-alpha)*w2]], w3],visited_nodes+1)

    
    #recursive step
    subtree1, visited_nodes1 = __regraft__(tree[0][0],targetNode,visited_nodes + 1)
    subtree2, visited_nodes2 = __regraft__(tree[0][1],targetNode,visited_nodes1)
    #visited_nodes2 is the total
    return ([[subtree1,subtree2],tree[1]],visited_nodes2)

