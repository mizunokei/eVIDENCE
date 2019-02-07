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

q_score_dic = {}


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

	matchL_f = re.findall(pattern2, cigar_f)
	matchL_r = re.findall(pattern2, cigar_r)

	if len(matchL_f) >= 4:
		continue
	if len(matchL_r) >= 4:
		continue

	iterator_f = re.finditer(pattern, cigar_f)
	for match in iterator_f:
		tup = match.span()
		num = match.group()

		if cigar_f[tup[1]] == "M":
			for i in range(int(num)):
				cigar_l_f.append("M")
				cigar_l_2_f.append("M")
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

	q_score_2_f = ""
	for q in q_score_l_2_f:
		q_score_2_f += q
	q_score_2_r = ""
	for q in q_score_l_2_r:
		q_score_2_r += q

	if int(pos_f) <= int(pos) < int(pos_f) + len(seq_l_2_f):
		if var.startswith("+"):
			barcode_base_dic.setdefault(barcode,[]).append(int(pos)-int(pos_f)+1)
			q_score_dic.setdefault(barcode,[]).append(q_score_2_f[int(pos)-int(pos_f)+1:int(pos)-int(pos_f)+len(var)])
		if var.startswith("-"):
			barcode_base_dic.setdefault(barcode,[]).append(int(pos)-int(pos_f)+1)
		cigar_dic.setdefault(barcode,[]).append(cigar_f)
		mdz_dic.setdefault(barcode,[]).append(mdz_f.split(":")[-1])

	elif int(pos_r) <= int(pos) < int(pos_r) + len(seq_l_2_r):
		if var.startswith("+"):
			barcode_base_dic.setdefault(barcode,[]).append(int(pos)-int(pos_r)+1)
			q_score_dic.setdefault(barcode,[]).append(q_score_2_r[int(pos)-int(pos_r)+1:int(pos)-int(pos_r)+len(var)])
		if var.startswith("-"):
			barcode_base_dic.setdefault(barcode,[]).append(int(pos)-int(pos_r)+1)
		cigar_dic.setdefault(barcode,[]).append(cigar_r)
		mdz_dic.setdefault(barcode,[]).append(mdz_r.split(":")[-1])

print("#chr"+"\tpos"+"\tref"+"\tvar"+"\ttotal_family_num"+"\tfamily_member_num"+"\tref_num"+"\tvar_num"+"\tvar_rate"+"\tinsertion_q"+"\tcigar""\tmdz"+"\tbarcode")

total_family_num = len(barcode_base_dic)

for k,v in barcode_base_dic.items():
	insertion_q = "_"
	counter = 0
	for i in range(len(barcode_base_dic[k])):
		if var.startswith("-"):
			if str(barcode_base_dic[k][i])+"M"+str(len(var)-1)+"D" in cigar_dic[k][i]:
				counter += 1
		if var.startswith("+"):
			if str(barcode_base_dic[k][i])+"M"+str(len(var)-1)+"I" in cigar_dic[k][i]:
				counter += 1
				insertion_q = insertion_q + q_score_dic[k][i] + "_"

	family_member = len(v)
	num_ref = family_member - counter
	num_var = counter
	var_rate = num_var/family_member*100

	mdz_counter = Counter(mdz_dic[k])
	cigar_counter = Counter(cigar_dic[k])

	print(chro,"\t",pos,"\t",ref,"\t",var,"\t",total_family_num,"\t",family_member,"\t",num_ref,"\t",num_var,"\t",var_rate,"\t",insertion_q,"\t",cigar_counter.most_common(1)[0][0],"\t",mdz_counter.most_common(1)[0][0],"\t",k)

