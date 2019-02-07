import sys

argv = sys.argv
input_f = open(argv[1])

pre_name = ""
result_l = []

for line in input_f:
	line = line.replace("\n","")
	line_l = line.split()

	name = line_l[0]

	if name != pre_name and pre_name != "":
		result1 = result_l[0]
		result1_l = result1.split()
		result2 = result_l[1]
		result2_l = result2.split()

		if len(result1_l) < 16 or len(result2_l) < 16:
			pre_name = name
			result_l = []
			result_l.append(line)
			continue

		if int(result1_l[1]) & 0x40 and int(result2_l[1]) & 0x80:
			print("@"+result1_l[0]+"\n"+result1_l[9]+"\n"+"+"+"\n"+result1_l[10])
		if int(result2_l[1]) & 0x40 and int(result1_l[1]) & 0x80:
			print("@"+result2_l[0]+"\n"+result2_l[9]+"\n"+"+"+"\n"+result2_l[10])
		result_l = []
	pre_name = name
	result_l.append(line)
result1 = result_l[0]
result1_l = result1.split()
result2 = result_l[1]
result2_l = result2.split()

if len(result1_l) >= 16 and len(result2_l) >= 16:
	if int(result1_l[1]) & 0x40 and int(result2_l[1]) & 0x80:
		print("@"+result1_l[0]+"\n"+result1_l[9]+"\n"+"+"+"\n"+result1_l[10])
	if int(result2_l[1]) & 0x40 and int(result1_l[1]) & 0x80:
		print("@"+result2_l[0]+"\n"+result2_l[9]+"\n"+"+"+"\n"+result2_l[10])
