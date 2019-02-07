import sys

argv = sys.argv

out_f = open(argv[1])

pre_name = ""
result_l = []

for line in out_f:
	line = line.replace("\n","")
	line_l = line.split()

	name = line_l[0]

	if line_l[0].startswith("@"):
		continue

	if line_l[2] == "*":
		continue

	if line_l[6] != "=":
		continue

	if len(line_l) != 15:
		continue

	if name != pre_name and pre_name != "":
		if len(result_l) ==2:
			l = result_l[0]
			l_l = l.split()
			barcode = l_l[0].split(":")[-3]
			print(result_l[0]+"\t"+result_l[1]+"\t"+barcode)
		result_l = []
	result_l.append(line)
	pre_name = name


if len(result_l) == 2:
	l = result_l[0]
	l_l = l.split()
	barcode = l_l[0].split(":")[-3]
	print(result_l[0]+"\t"+result_l[1]+"\t"+barcode)

