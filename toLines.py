#!/usr/bin/env python
import sys

if __name__ == "__main__":
    strline = ""
    for line in sys.stdin:
        ignored,x,y = line.split("\t")
        
        if x=="1":
            strline += "\n"
        
        strline += y.replace("\n","") + ","
        
    
    print(strline[1:-1])