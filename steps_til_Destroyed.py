import tree_utils
import sys
from math import sqrt

def steps_til_Destroyed(filename,epsilon):
    
    results=[]
    
    #open file
    with open(filename,'r') as seqs_file:
        for line in seqs_file:
            lst_line = line.replace("\n","").split(",")
            nodes = int(lst_line[0])
            seq   = map(lambda x: float(x),lst_line[1:-1])
            
            #find the steps until distances are within
            #epsilon of max_dist
            max_dist = 2*sqrt(nodes)
            threshold = max_dist - epsilon
            steps=0
            for x in seq:
                if x > threshold:
                    break
                steps +=1
            
            results.append((nodes,steps))
            
    #write results to file
    with open("steps_til_destroyed",'a') as results_file:
        for record in results:
            a,b= record 
            results_file.write(str(a) + "," + str(b) + "\n")
            

        
if __name__=='__main__':
    if len(sys.argv)<2:
        print ("Too few arguments!!")
        print ("Usage: <nodes-plus-sequence filename>")
        sys.exit(-1)
    
    filename = sys.argv[1]
    
    steps_til_Destroyed(filename,0.1)