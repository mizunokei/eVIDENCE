import sys

argv = sys.argv
pos_l = []

for i in range (1,len(argv)-1):
	out_exclude = open(argv[i])
	for line in out_exclude:
		line = line.replace("\n","")
		line_l = line.split()
		if line_l[0].startswith("#"):
			continue
		pos = line_l[0]+"_"+line_l[1]+"_"+line_l[3]
		pos_l.append(pos)

out_file = open(argv[-1])
for line in out_file:
	line = line.replace("\n","")
	line_l = line.split()
	pos = line_l[0]+"_"+line_l[1]+"_"+line_l[3]
	if pos not in pos_l:
		print(line)

