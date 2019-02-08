import sys

argv = sys.argv

out_f = open(argv[1])

for line in out_f:
	line = line.replace("\n","")
	line_l = line.split()

	if line_l[0].startswith("#"):
		continue

	line_l[0] = line_l[0].strip("chr")

	if line_l[3].startswith("+"):
		ref = "-"
		alt = line_l[3].strip("+")
		start = line_l[1]
		end = line_l[1]

	elif line_l[3].startswith("-"):
		start = str(int(line_l[1])+1)
		end = str(int(line_l[1])+len(line_l[3])-1)
		ref = line_l[3].strip("-")
		alt = "-"
	else:
		start = line_l[1]
		end = line_l[1]
		ref = line_l[2]
		alt = line_l[3]
	print(line_l[0]+"\t"+start+"\t"+end+"\t"+ref+"\t"+alt+"\t"+line_l[4]+"\t"+line_l[5]+"\t"+line_l[6])

