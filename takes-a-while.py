#takes-a-while.py will run a loop that will take some time
#to finish after htat it will write a to a file

with open('syncfile','w') as f:
     f.write("The program started runing")

count = 0
for i in range(100000000):
    count += 1


with open('syncfile','w') as f:
     f.write("The program finished running")

