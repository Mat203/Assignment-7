import sys
 
n = sys.argv[1]

with open('data.csv','r') as file:
    next_line = file.readline()

    while next_line:
        next_line = file.readline()
        print(next_line)