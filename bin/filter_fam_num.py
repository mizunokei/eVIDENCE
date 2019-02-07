import sys

argv = sys.argv

out_f = open(argv[1])
num = int(argv[2])
depth = int(argv[3])

for line in out_f:
	line = line.replace("\n","")
	line_l = line.split()

	if line_l[0].startswith("#"):
		print(line)
		continue
	if int(line_l[4]) >= depth and int(line_l[5]) >= num:
		print(line)

