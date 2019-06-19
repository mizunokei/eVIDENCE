import sys
import re

argv = sys.argv

mut_dic = {}
out_snv = open(argv[1])
for line in out_snv:
        line = line.replace("\n","")
        line_l = line.split()

        if line_l[0].startswith("#"):
                continue
        mut_dic.setdefault(line_l[0],[]).append(int(line_l[1]))
out_indel = open(argv[2])
for line in out_indel:
        line = line.replace("\n","")
        line_l = line.split()

        if line_l[0].startswith("#"):
                continue
        mut_dic.setdefault(line_l[0],[]).append(int(line_l[1]))
#print(mut_dic)

out_f = open(argv[3])

pre_name = ""
result_l = []

for line in out_f:
        line = line.replace("\n","")
        line_l = line.split()

        if line_l[0].startswith("@"):
                continue

        name = line_l[0]
        if name != pre_name and pre_name != "":
                for r in result_l:
                        r_l = r.split()
                        chrm = r_l[2]
                        pos = int(r_l[3])
                        if chrm in mut_dic:
                                for p in mut_dic[chrm]:
                                        if pos-10 <= p <= pos+200:
                                                for r in result_l:
                                                        print(r)

                                                break
                                else:
                                        continue
                                break
                result_l = []
        pre_name = name
        result_l.append(line)

for r in result_l:
        r_l = r.split()
        chrm = r_l[2]
        pos = int(r_l[3])
        if chrm in mut_dic:
                for p in mut_dic[chrm]:
                        if pos-10 <= p <= pos+200:
                                for r in result_l:
                                        print(r)
                                break
                        else:
                                continue
                        break
