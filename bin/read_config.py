import sys

f = open(sys.argv[1])
target = sys.argv[2]

for line in f:
        line = line.replace("\n", "")
        if target in line:
                output = (line.split("=", ))[1]
                print(output)
                break
