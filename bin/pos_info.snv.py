import re
import sys

from collections import Counter

argv = sys.argv

chro = argv[2].split("_")[0]
pos = argv[2].split("_")[1]
ref = argv[2].split("_")[2]
var = argv[2].split("_")[3]

out_f = open(argv[1]+chro+".txt")

barcode_base_dic = {}
mdz_dic = {}
cigar_dic ={}

variant_100_l = []

barcode_q20_f = {}
barcode_q20_r = {}

for line in out_f:
	line = line.replace("\n","")
	line_l = line.split()
	if int(line_l[4]) < 20 or int(line_l[19]) < 20:
		continue

	if line_l[2] != chro:
		continue
	if line_l[17] != chro:
		continue

	pattern = r"\d+"
	barcode = line_l[-1]

	cigar_f = line_l[5]
	seq_f = line_l[9]
	mdz_f = line_l[12]
	pos_f = line_l[3]
	q_score_f = line_l[10]
	chro_f = line_l[2]

	cigar_l_f = []
	cigar_l_2_f = []
	pos_l_f = []

	cigar_r = line_l[20]
	seq_r = line_l[24]
	mdz_r = line_l[27]
	pos_r = line_l[18]
	q_score_r = line_l[25]
	chro_r = line_l[17]

	cigar_l_r = []
	cigar_l_2_r = []
	pos_l_r = []	

	pattern2 = r"\D"

	matchL_f = re.findall(pattern2, mdz_f.split(":")[-1])
	matchL_r = re.findall(pattern2, mdz_r.split(":")[-1])

	if len(matchL_f) >= 3:
		continue
	if len(matchL_r) >= 3:
		continue

	if len(matchL_f) == 2:
		if len(re.findall(pattern, mdz_f.split(":")[-1])) == 3:
			if int(re.findall(pattern, mdz_f.split(":")[-1])[1]) < 10:
				continue

	if len(matchL_r) == 2:
		if len(re.findall(pattern, mdz_r.split(":")[-1])) == 3:
			if int(re.findall(pattern, mdz_r.split(":")[-1])[1]) < 10:
				continue

	iterator_f = re.finditer(pattern, cigar_f)
	for match in iterator_f:
		tup = match.span()
		num = match.group()

		if cigar_f[tup[1]] == "M":
			for i in range(int(num)):
				cigar_l_f.append("M")
				cigar_l_2_f.append("M")
				pos_l_f.append("M")
		if cigar_f[tup[1]] == "I":
			for i in range(int(num)):
				cigar_l_f.append("I")
				cigar_l_2_f.append("I")
		if cigar_f[tup[1]] == "S":
			for i in range(int(num)):
				cigar_l_2_f.append("S")
		if cigar_f[tup[1]] == "D":
			for i in range(int(num)):
				pos_l_f.append("D")


	index_f = [i for i,x in enumerate(cigar_l_2_f) if x =="S"]
	index_2_f = [i for i,x in enumerate(cigar_l_2_f) if x =="I"]
	index_3_f = [i for i,x in enumerate(pos_l_f) if x =="D"]
	seq_l_2_f = [seq_f[i] for i in range(len(seq_f)) if not i in index_f and not i in index_2_f]	
	q_score_l_2_f = [q_score_f[i] for i in range(len(q_score_f)) if not i in index_f and not i in index_2_f]

	if index_3_f != []:
		for i in index_3_f:
			seq_l_2_f.insert(i,"D")
			q_score_l_2_f.insert(i,"D")

	iterator_r = re.finditer(pattern, cigar_r)
	for match in iterator_r:
		tup = match.span()
		num = match.group()

		if cigar_r[tup[1]] == "M":
			for i in range(int(num)):
				cigar_l_r.append("M")
				cigar_l_2_r.append("M")
				pos_l_r.append("M")
		if cigar_r[tup[1]] == "I":
			for i in range(int(num)):
				cigar_l_r.append("I")
				cigar_l_2_r.append("I")
		if cigar_r[tup[1]] == "S":
			for i in range(int(num)):
				cigar_l_2_r.append("S")
		if cigar_r[tup[1]] == "D":
			for i in range(int(num)):
				pos_l_r.append("D")


	index_r = [i for i,x in enumerate(cigar_l_2_r) if x =="S"]
	index_2_r = [i for i,x in enumerate(cigar_l_2_r) if x =="I"]
	index_3_r = [i for i,x in enumerate(pos_l_r) if x =="D"]
	seq_l_2_r = [seq_r[i] for i in range(len(seq_r)) if not i in index_r and not i in index_2_r]	
	q_score_l_2_r = [q_score_r[i] for i in range(len(q_score_r)) if not i in index_r and not i in index_2_r]

	if index_3_r != []:
		for i in index_3_r:
			seq_l_2_r.insert(i,"D")
			q_score_l_2_r.insert(i,"D")

	if int(pos_f) <= int(pos) < int(pos_f) + len(seq_l_2_f):
		if ord(q_score_l_2_f[int(pos)-int(pos_f)])-33 >= 20:
			barcode_base_dic.setdefault(barcode,[]).append(seq_l_2_f[int(pos)-int(pos_f)])
			cigar_dic.setdefault(barcode,[]).append(cigar_f)
			if len(matchL_f) == 1:
				mdz_dic.setdefault(barcode,[]).append(mdz_f.split(":")[-1])
		else:
			if barcode not in barcode_q20_f:
				barcode_q20_f[barcode] = 1
			else:
				barcode_q20_f[barcode] += 1

	elif int(pos_r) <= int(pos) < int(pos_r) + len(seq_l_2_r):
		if ord(q_score_l_2_r[int(pos)-int(pos_r)])-33 >= 20:
			barcode_base_dic.setdefault(barcode,[]).append(seq_l_2_r[int(pos)-int(pos_r)])
			cigar_dic.setdefault(barcode,[]).append(cigar_r)
			if len(matchL_r) == 1:
				mdz_dic.setdefault(barcode,[]).append(mdz_r.split(":")[-1])
		else:
			if barcode not in barcode_q20_r:
				barcode_q20_r[barcode] = 1
			else:
				barcode_q20_r[barcode] += 1

print("#chr"+"\tpos"+"\tref"+"\tvar"+"\ttotal_family_num"+"\tfamily_member_num"+"\tref_num"+"\tvar_num"+"\tvar_rate"+"\tbase_q<20_num"+"\tcigar""\tmdz"+"\tbarcode")

for k,v in barcode_base_dic.items():
	num_ref = Counter(v)[ref]
	num_var = Counter(v)[var]
	if k not in barcode_q20_f:
		barcode_q20_f[k] = 0
	if k not in barcode_q20_r:
		barcode_q20_r[k] = 0
	base_q20_num = barcode_q20_f[k]+barcode_q20_r[k]

	if k not in mdz_dic:
		mdz_dic[k] = ["NA"]
	mdz_counter = Counter(mdz_dic[k])
	if k not in cigar_dic:
		cigar_dic[k] = ["NA"]
	cigar_counter = Counter(cigar_dic[k])

	print(chro,"\t",pos,"\t",ref,"\t",var,"\t",len(barcode_base_dic),"\t",len(v),"\t",num_ref,"\t",num_var,"\t",num_var/len(v)*100,"\t",base_q20_num,"\t",cigar_counter.most_common(1)[0][0],"\t",mdz_counter.most_common(1)[0][0],"\t",k)

