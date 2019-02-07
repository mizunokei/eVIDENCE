import sys

argv = sys.argv

input_f = open(argv[1])

pre_chr = ""

for line in input_f:
	line = line.replace("\n","")
	line_l = line.split()

	chr = line_l[2]

	if pre_chr != chr:
		file_name = argv[2]+chr+".txt"
		out_f = open(file_name, "w")
	print(line, file = out_f)
	pre_chr = chr

