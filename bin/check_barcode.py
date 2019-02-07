import sys

argv = sys.argv

out_candidate_f = open(argv[1])

pos_dic = {}

for line in out_candidate_f:
	line = line.replace("\n","")
	line_l = line.split()

	if line_l[0].startswith("#"):
		print(line+"\tbarcode")
		continue

	pos = line_l[0]+"_"+line_l[1]+"_"+line_l[3]
	pos_dic[pos] = line

out_f = open(argv[2])

pre_pos = ""
barcode_l = []

for line in out_f:
	line = line.replace("\n","")
	line_l = line.split()

	if line_l[0].startswith("#"):
		continue
	barcode = line_l[-1]
	pos = line_l[0]+"_"+line_l[1]+"_"+line_l[3]

	if pos != pre_pos and pre_pos != "":
		if pre_pos not in pos_dic:
			pre_pos = pos
			barcode_l = []
			barcode_l.append(barcode)
			continue
		counter = 0
		for b in barcode_l:
			b_f = b.split("_")[0]
			b_r = b.split("_")[1]
			if counter == 0:
				b_f_0 = b.split("_")[0]
				b_r_0 = b.split("_")[1]
			if b_f_0 != b_f and b_r_0 != b_r:
				pre_pos = pos
				break
			counter += 1
			if counter == len(barcode_l):
				print(pos_dic[pre_pos],"\t",barcode_l)
		barcode_l = []
	pre_pos = pos
	barcode_l.append(barcode)
if pre_pos in pos_dic:
	counter = 0
	for b in barcode_l:
		b_f = b.split("_")[0]
		b_r = b.split("_")[1]
		if counter == 0:
			b_f_0 = b.split("_")[0]
			b_r_0 = b.split("_")[1]
		if b_f_0 != b_f and b_r_0 != b_r:
			pre_pos = pos
			break
		counter += 1
		if counter == len(barcode_l):
			print(pos_dic[pre_pos],"\t",barcode_l)
