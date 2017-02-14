import tree_utils
import csv


def findDistructionDistance(num_files,epsilon):
    #get number of nodes from file
    for k in range(num_files):
        with open("sprseq" + srt(k),"r") as seq:
            newick_tree = seq.readline()
            tree = newickToNestedLst(newick_tree)
            number_nodes = countNodes(tree)

        max_dist = 2*sqrt(number_nodes)

        count_steps=0
        with open("seq" + srt(k) +".csv", 'r') as distfile:
            dist_reader = csv.reader(distfile,delimiter='\t')

            for row in dist_reader:
                #row 2 is the geo distance
                if float(row[2]) > (max_dist * 0.9):
                    break
            
                count_steps+=1
        
        print((number_nodes,count_steps))

        
if __name__=='__main__':
    if len(sys.argv)<2:
        print ("Too few arguments!!")
        print ("Usage: <no. inpput files>")
        sys.exit(-1)
    
    num_files = sys.argv[1]
    
    findDistructionDistance(num_files)