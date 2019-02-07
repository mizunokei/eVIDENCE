import sys

argv = sys.argv

out_f = open(argv[1])

counter = 0

for line in out_f:
	line = line.replace("\n","")
	line_l = line.split()

	if line_l[0].startswith("#"):
		if counter == 0:
			print(line)
			counter = 1
		continue
	if int(line_l[7]) != 0:
		print(line)
