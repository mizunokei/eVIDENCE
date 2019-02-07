import sys
import re

argv = sys.argv
open_f = open(argv[1])
out_f =  open(argv[2])
head_counter = 0
genotype_dic = {}

for line in out_f:
	line = line.replace("\n","")
	line_l = line.split()

	if line_l[0].startswith("#"):
		continue
	name = line_l[0]+"_"+line_l[1]

	genotype = line_l[3]
	genotype_dic[name] = genotype

for line in open_f:
	line = line.replace("\n", "")
	line_l = line.split()

	pos = line_l[0]+"_"+line_l[1]
	ref = line_l[2].upper()
	total = line_l[3]
	seq = line_l[4]
	num_dot = seq.count(".")
	num_comma = seq.count(",")
	num_g = seq.count("g")
	num_a = seq.count("a")
	num_G = seq.count("G")
	num_A = seq.count("A")
	num_T = seq.count("T")
	num_t = seq.count("t")
	num_C = seq.count("C")
	num_c = seq.count("c")

	if head_counter == 0:
		print("#chr","\tpos","\tref","\tvar","\ttotal","\tforward_ref","\treverse_ref","\tforward_var","\treverse_var")
		head_counter += 1
		continue	

	if pos in genotype_dic:
		i = genotype_dic[pos]
		if i == "A":
			var = "A"
			forward_var = num_A
			reverse_var = num_a
			print(line_l[0],"\t",line_l[1],"\t",ref,"\t",var,"\t",total,"\t",num_dot,"\t",num_comma,"\t",forward_var,"\t",reverse_var)
		if i == "T":
			var = "T"
			forward_var = num_T
			reverse_var = num_t
			print(line_l[0],"\t",line_l[1],"\t",ref,"\t",var,"\t",total,"\t",num_dot,"\t",num_comma,"\t",forward_var,"\t",reverse_var)
		if i == "G":
			var = "G"
			forward_var = num_G
			reverse_var = num_g
			print(line_l[0],"\t",line_l[1],"\t",ref,"\t",var,"\t",total,"\t",num_dot,"\t",num_comma,"\t",forward_var,"\t",reverse_var)
		if i == "C":
			var = "C"
			forward_var = num_C
			reverse_var = num_c
			print(line_l[0],"\t",line_l[1],"\t",ref,"\t",var,"\t",total,"\t",num_dot,"\t",num_comma,"\t",forward_var,"\t",reverse_var)


