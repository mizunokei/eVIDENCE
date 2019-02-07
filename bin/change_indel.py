import sys

argv = sys.argv

out_f = open(argv[1])

pre_name = ""

for line in out_f:
	line = line.replace("\n","")
	line_l = line.split()

	if line_l[0].startswith("#"):
		continue

	name = line_l[0]+"_"+line_l[1]+"_"+line_l[2]+"_"+line_l[3]

	if name == pre_name:
		continue

	print(line)

	pre_name = name
