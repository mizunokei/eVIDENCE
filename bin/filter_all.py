import sys

argv = sys.argv
out_f = open(argv[1])

pre_name = ""
result_l = []

for line in out_f:
        line = line.replace("\n","")
        line_l = line.split()

        if line_l[0].startswith("#"):
                print(line)
                continue
        name = line_l[1]+"_"+line_l[3]
        if name != pre_name and pre_name != "":
                for l in result_l:
                        l_l = l.split()
                        l_l[4] = str(len(result_l))
                        print("\t".join(l_l))
                result_l = []

        if "N" not in line_l[-1]:

                if int(line_l[5]) >= 3 and int(line_l[7]) == 0:
                        result_l.append(line)
                if 3 <= int(line_l[5]) < 20 and 2 < int(line_l[7]):
                        result_l.append(line)
                if 20 <= int(line_l[5]) and (int(line_l[5])//10)+1 < int(line_l[7]):
                        result_l.append(line)
        pre_name = name
for l in result_l:
        l_l = l.split()
        l_l[4] = str(len(result_l))
        print("\t".join(l_l))
