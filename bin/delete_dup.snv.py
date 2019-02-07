import sys

argv = sys.argv

out_f = open(argv[1])
pre_name = ""
counter = 0
result = ""
barcode_l = []
del_counter = 0

for line in out_f:
	line = line.replace("\n","")
	line_l = line.split()
	name = line_l[0]+"_"+line_l[1]+"_"+line_l[3]
	barcode = line_l[-1]

	if line_l[0].startswith("#"):
		print(line_l[0]+"\t"+line_l[1]+"\t"+line_l[2]+"\t"+line_l[3]+"\t"+line_l[4]+"\t"+line_l[5]+"\t"+line_l[6])
		continue

	if name != pre_name and pre_name != "":
		b_f_dic = {}
		b_r_dic = {}
		for b in barcode_l:
			b_f = b.split("_")[0]
			b_r = b.split("_")[1]
			if b_f not in b_f_dic:
				b_f_dic[b_f] = 1
			else:
				b_f_dic[b_f] += 1
			if b_r not in b_r_dic:
				b_r_dic[b_r] = 1
			else:
				b_r_dic[b_r] += 1
		new_barcode_l = []
		for k_f,v_f in sorted(b_f_dic.items(), key = lambda x:x[1], reverse = True):
			if v_f >= 2:
				for k_r,v_r in sorted(b_r_dic.items(), key = lambda x:x[1], reverse = True):
					if v_r >= 2:
						v_f -= 1
						if v_f >= 1:
							new_barcode_l.append(k_f+"_"+k_r)
							b_r_dic[k_r] -= 1
		for b in barcode_l:
			if b in new_barcode_l:
				counter -= 1
				del_counter += 1
		result_l = result.split()
		print(result_l[0]+"\t"+result_l[1]+"\t"+result_l[2]+"\t"+result_l[3]+"\t"+str(int(result_l[4])-del_counter)+"\t"+str(counter)+"\t"+str(counter/(int(result_l[4])-del_counter)*100))
		counter = 0
		barcode_l = []
		del_counter = 0
	counter += 1
	pre_name = name
	result = line
	barcode_l.append(barcode)

b_f_dic = {}
b_r_dic = {}
b_f_list = []
b_r_list = []
for b in barcode_l:
	b_f = b.split("_")[0]
	b_r = b.split("_")[1]
	if b_f not in b_f_dic:
		b_f_dic[b_f] = 1
	else:
		b_f_dic[b_f] += 1
	if b_r not in b_r_dic:
		b_r_dic[b_r] = 1
	else:
		b_r_dic[b_r] += 1
new_barcode_l = []
for k_f,v_f in sorted(b_f_dic.items(), key = lambda x:x[1], reverse = True):
	if v_f >= 2:
		for k_r,v_r in sorted(b_r_dic.items(), key = lambda x:x[1], reverse = True):
			if v_r >= 2:
				v_f -= 1
				if v_f >= 1:
					new_barcode_l.append(k_f+"_"+k_r)
					b_r_dic[k_r] -= 1
for b in barcode_l:
	if b in new_barcode_l:
		counter -= 1
		del_counter += 1
result_l = result.split()
print(result_l[0]+"\t"+result_l[1]+"\t"+result_l[2]+"\t"+result_l[3]+"\t"+str(int(result_l[4])-del_counter)+"\t"+str(counter)+"\t"+str(counter/(int(result_l[4])-del_counter)*100))
