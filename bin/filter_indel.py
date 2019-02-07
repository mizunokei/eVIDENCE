import sys
from collections import Counter

argv = sys.argv

out_f = open(argv[1])

result_l = []
pre_name = ""
counter = 0

var_num_l = []
ref_var_num_l = []

del_count = 0

for line in out_f:
	line = line.replace("\n","")
	line_l = line.split()
	if line_l[0].startswith("#"):
		print(line_l[0],"\t",line_l[1],"\t",line_l[2],"\t",line_l[3],"\t",line_l[4],"\tindel_family_number","\tVAF","\t",line_l[5],"\t",line_l[6],"\t",line_l[7],"\t",line_l[8],"\t",line_l[9],"\t",line_l[10],"\t",line_l[11],"\t",line_l[12])
		continue

	ref_num = int(line_l[6])
	var_num = int(line_l[7])
	ref_var_num = line_l[6]+"_"+line_l[7]
	name = line_l[0]+"_"+line_l[1]+"_"+line_l[3]
	insertion_q = line_l[-4]

	q_score_l = []
	insertion_q_l = insertion_q.split("_")
	for s in insertion_q_l:
		if s != "":
			for i in s:
				q_score_l.append(ord(i) - 33)
	if q_score_l != [] and min(q_score_l) < 20:
		counter += 1
		del_count += 1
		continue

	if name != pre_name and pre_name != "":
		for r in ref_var_num_l:
			ref = int(r.split("_")[0])
			var = int(r.split("_")[1])
			if ref >= 2 and var > 2:
				result_l = []

		del_count = del_count+Counter(var_num_l)[1]+Counter(var_num_l)[2]
		for l in result_l:
			l_l = l.split()
			if int(l_l[7]) > 2:
				print(l_l[0],"\t",l_l[1],"\t",l_l[2],"\t",l_l[3],"\t",str(int(l_l[4])-del_count),"\t",str(counter-del_count),"\t",str((counter-del_count)/(int(l_l[4])-del_count)*100),"\t",l_l[5],"\t",l_l[6],"\t",l_l[7],"\t",l_l[8],"\t",l_l[9],"\t",l_l[10],"\t",l_l[11],"\t",l_l[12])
		var_num_l = []
		ref_var_num_l = []
		result_l = []
		pre_name = ""
		counter = 0
		del_count = 0
	pre_name = name
	var_num_l.append(var_num)
	ref_var_num_l.append(ref_var_num)
	result_l.append(line)
	counter += 1

for r in ref_var_num_l:
	ref = int(r.split("_")[0])
	var = int(r.split("_")[1])
	if ref >= 2 and var > 2:
		result_l = []
del_count = del_count+Counter(var_num_l)[1]+Counter(var_num_l)[2]
for l in result_l:
	l_l = l.split()
	if int(l_l[7]) > 2:
		print(l_l[0],"\t",l_l[1],"\t",l_l[2],"\t",l_l[3],"\t",str(int(l_l[4])-del_count),"\t",str(counter-del_count),"\t",str((counter-del_count)/(int(l_l[4])-del_count)*100),"\t",l_l[5],"\t",l_l[6],"\t",l_l[7],"\t",l_l[8],"\t",l_l[9],"\t",l_l[10],"\t",l_l[11],"\t",l_l[12])
