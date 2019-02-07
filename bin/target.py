import sys
import re

argv = sys.argv

out_bed_f = open(argv[1])

target_dic = {}

for line in out_bed_f:
	line = line.replace("\n","")
	line_l = line.split()

	name = line_l[0]
	start = line_l[1]
	end = line_l[2]
	target_dic.setdefault(name,[]).append((int(start)-100,int(end)+100))

out_snv_f = open(argv[2])

for line in out_snv_f:
	line = line.replace("\n","")
	line_l = line.split()

	if line_l[0].startswith("#"):
		print(line)

	name = line_l[0]
	pos = line_l[1]

	if name in target_dic:
		for r in target_dic[name]:
			if r[0] <= int(pos) <= r[1]:
				print(line)
