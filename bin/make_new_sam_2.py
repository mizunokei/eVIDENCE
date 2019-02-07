import sys
import re

argv = sys.argv
out_f = open(argv[1])

pre_name = ""
result_l = []

for line in out_f:
	line = line.replace("\n","")
	line_l = line.split()

	name = line_l[0]

	if name != pre_name and pre_name != "":
		counter_M_D_1 = 0
		counter_M_D_2 = 0

		if len(result_l) != 2:
			pre_name = name
			result_l = []
			result_l.append(line)
			continue

		read_1 = result_l[0]
		read_2 = result_l[1]

		read_1_l = read_1.split()
		read_2_l = read_2.split()

		read_1_flag = int(read_1_l[1])
		read_2_flag = int(read_2_l[1])

		read_1_cigar = read_1_l[5]
		read_2_cigar = read_2_l[5]

		read_1_cigar_l = []
		read_2_cigar_l = []

		read_1_seq = read_1_l[9]
		read_2_seq = read_2_l[9]

		read_1_q = read_1_l[10]
		read_2_q = read_2_l[10]

		barcode_1 = read_1_l[-1]
		barcode_2 = read_2_l[-1]

		pattern = r"\d+"
		iterator_1 = re.finditer(pattern, read_1_cigar)
		iterator_2 = re.finditer(pattern, read_2_cigar)

		cigar_alp_1 = re.split(pattern, read_1_cigar)
		cigar_alp_2 = re.split(pattern, read_2_cigar)
		cigar_num_1 = re.split(r"\D", read_1_cigar)
		cigar_num_2 = re.split(r"\D", read_2_cigar)

		for match in iterator_1:
			tup = match.span()
			num = match.group()
			if read_1_cigar[tup[1]] == "D" or read_1_cigar[tup[1]] == "M":
				counter_M_D_1 += int(num)
			if read_1_cigar[tup[1]] == "M":
				for i in range(int(num)):
					read_1_cigar_l.append("M")
			if read_1_cigar[tup[1]] == "I":
				for i in range(int(num)):
					read_1_cigar_l.append("I")
			if read_1_cigar[tup[1]] == "S":
				for i in range(int(num)):
					read_1_cigar_l.append("S")
			index = [i for i,x in enumerate(read_1_cigar_l) if x =="S"]
			read_1_seq_l = [read_1_seq[i] for i in range(len(read_1_seq)) if not i in index]
			read_1_l[9] = "".join(read_1_seq_l)
			read_1_q_l = [read_1_q[i] for i in range(len(read_1_q)) if not i in index]
			read_1_l[10] = "".join(read_1_q_l)

		for match in iterator_2:
			tup = match.span()
			num = match.group()
			if read_2_cigar[tup[1]] == "D" or read_2_cigar[tup[1]] == "M":
				counter_M_D_2 += int(num)
			if read_2_cigar[tup[1]] == "M":
				for i in range(int(num)):
					read_2_cigar_l.append("M")
			if read_2_cigar[tup[1]] == "I":
				for i in range(int(num)):
					read_2_cigar_l.append("I")
			if read_2_cigar[tup[1]] == "S":
				for i in range(int(num)):
					read_2_cigar_l.append("S")
			index = [i for i,x in enumerate(read_2_cigar_l) if x =="S"]
			read_2_seq_l = [read_2_seq[i] for i in range(len(read_2_seq)) if not i in index]
			read_2_l[9] = "".join(read_2_seq_l)
			read_2_q_l = [read_2_q[i] for i in range(len(read_2_q)) if not i in index]
			read_2_l[10] = "".join(read_2_q_l)

		start_1 = int(read_1_l[3])
		start_2 = int(read_2_l[3])
		end_1 = start_1 + counter_M_D_1 - 1 
		end_2 = start_2 + counter_M_D_2 - 1


		if read_1_l[6] != "=":
			if read_1_flag & 0x40:
				barcode = barcode_1+"_"+barcode_2
			if read_1_flag & 0x80:
				barcode = barcode_2+"_"+barcode_1
			read_1_l[0] = read_1_l[0]+":"+barcode+":0:0"
			read_2_l[0] = read_2_l[0]+":"+barcode+":0:0"
			print("\t".join(read_1_l))
			print("\t".join(read_2_l))

		elif not read_1_flag & 0x2:
			if not read_1_flag & 0x10 and read_2_flag & 0x10:
				if cigar_alp_1[-1] == "S":
					if int(cigar_num_1[-2]) > int(cigar_num_2[-2]):
						pre_name = name
						result_l = []
						result_l.append(line)
						continue
				if cigar_alp_2[1] == "S":
					if int(cigar_num_2[0]) > int(cigar_num_1[0]):
						pre_name = name
						result_l = []
						result_l.append(line)
						continue
				barcode = barcode_1+"_"+barcode_2
			elif read_1_flag & 0x10 and not read_2_flag & 0x10:
				if cigar_alp_1[1] == "S":
					if int(cigar_num_1[0]) > int(cigar_num_2[0]):
						pre_name = name
						result_l = []
						result_l.append(line)
						continue
				if cigar_alp_2[-1] == "S":
					if int(cigar_num_2[-2]) > int(cigar_num_1[-2]):
						pre_name = name
						result_l = []
						result_l.append(line)
						continue
				barcode = barcode_2+"_"+barcode_1
			else:
				if read_1_flag & 0x40:
					barcode = barcode_1+"_"+barcode_2
				if read_1_flag & 0x80:
					barcode = barcode_2+"_"+barcode_1
			read_1_l[0] = read_1_l[0]+":"+barcode+":0:0"
			read_2_l[0] = read_2_l[0]+":"+barcode+":0:0"
			print("\t".join(read_1_l))
			print("\t".join(read_2_l))
			
		else:
			if not read_1_flag & 0x10:
				if cigar_alp_1[-1] == "S":
					if int(cigar_num_1[-2]) > int(cigar_num_2[-2]):
						pre_name = name
						result_l = []
						result_l.append(line)
						continue
				if cigar_alp_2[1] == "S":
					if int(cigar_num_2[0]) > int(cigar_num_1[0]):
						pre_name = name
						result_l = []
						result_l.append(line)
						continue
				barcode = barcode_1+"_"+barcode_2
				if start_1 <= start_2 and end_1 <= end_2:
					read_1_l[0] = read_1_l[0]+":"+barcode+":0:0"
					read_2_l[0] = read_2_l[0]+":"+barcode+":0:0"
					print("\t".join(read_1_l))
					print("\t".join(read_2_l))
				if start_1 > start_2 and end_1 <= end_2:
					cut = start_1 - start_2
					counter = 0
					for i in cigar_alp_2:
						counter += 1
						if i == "M":
							break
					if cigar_alp_2[counter] == "I" and int(cigar_num_2[counter-1]) > int(cigar_num_2[counter-2]) - cut:
						cut += int(cigar_num_2[counter-1])
					read_1_l[0] = read_1_l[0]+":"+barcode+":0:"+str(cut)
					read_2_l[0] = read_2_l[0]+":"+barcode+":0:"+str(cut)
					read_2_l[9] = read_2_l[9][cut:]
					read_2_l[10] = read_2_l[10][cut:]
					print("\t".join(read_1_l))
					print("\t".join(read_2_l))
				if start_1 <= start_2 and end_1 > end_2:
					cut = end_1 - end_2
					counter = 0
					for i in reversed(cigar_alp_1):
						counter += 1
						if i == "M":
							break
					if cigar_alp_1[-counter-1] == "I" and int(cigar_num_1[-counter-2]) > int(cigar_num_1[-counter-1]) - cut:
						cut += int(cigar_num_1[-counter-2])
					read_1_l[0] = read_1_l[0]+":"+barcode+":"+str(cut)+":0"
					read_2_l[0] = read_2_l[0]+":"+barcode+":"+str(cut)+":0"
					read_1_l[9] = read_1_l[9][:-cut]
					read_1_l[10] = read_1_l[10][:-cut]
					print("\t".join(read_1_l))
					print("\t".join(read_2_l))
				if start_1 > start_2 and end_1 > end_2:
					cut1 = end_1 - end_2
					cut2 = start_1 - start_2
					counter1 = 0
					for i in reversed(cigar_alp_1):
						counter1 += 1
						if i == "M":
							break
					if cigar_alp_1[-counter1-1] == "I" and int(cigar_num_1[-counter1-2]) > int(cigar_num_1[-counter1-1]) - cut1:
						cut1 += int(cigar_num_1[-counter1-2])
					counter2 = 0
					for i in cigar_alp_2:
						counter2 += 1
						if i == "M":
							break
					if cigar_alp_2[counter2] == "I" and int(cigar_num_2[counter2-1]) > int(cigar_num_2[counter2-2]) - cut2:
						cut2 += int(cigar_num_2[counter2-1])
					read_1_l[0] = read_1_l[0]+":"+barcode+":"+str(cut1)+":"+str(cut2)
					read_2_l[0] = read_2_l[0]+":"+barcode+":"+str(cut1)+":"+str(cut2)
					read_1_l[9] = read_1_l[9][:-cut1]
					read_1_l[10] = read_1_l[10][:-cut1]
					read_2_l[9] = read_2_l[9][cut2:]
					read_2_l[10] = read_2_l[10][cut2:]
					print("\t".join(read_1_l))
					print("\t".join(read_2_l))

			if read_1_flag & 0x10:
				if cigar_alp_1[1] == "S":
					if int(cigar_num_1[0]) > int(cigar_num_2[0]):
						pre_name = name
						result_l = []
						result_l.append(line)
						continue
				if cigar_alp_2[-1] == "S":
					if int(cigar_num_2[-2]) > int(cigar_num_1[-2]):
						pre_name = name
						result_l = []
						result_l.append(line)
						continue
				barcode = barcode_2+"_"+barcode_1
				if start_2 <= start_1 and end_2 <= end_1:
					read_1_l[0] = read_1_l[0]+":"+barcode+":0:0"
					read_2_l[0] = read_2_l[0]+":"+barcode+":0:0"
					print("\t".join(read_1_l))
					print("\t".join(read_2_l))
				if start_2 <= start_1 and end_2 > end_1:
					cut = end_2 - end_1
					counter = 0
					for i in reversed(cigar_alp_2):
						counter += 1
						if i == "M":
							break
					if cigar_alp_2[-counter-1] == "I" and int(cigar_num_2[-counter-2]) > int(cigar_num_2[-counter-1]) - cut:
						cut += int(cigar_num_2[-counter-2])
					read_1_l[0] = read_1_l[0]+":"+barcode+":"+str(cut)+":0"
					read_2_l[0] = read_2_l[0]+":"+barcode+":"+str(cut)+":0"
					read_2_l[9] = read_2_l[9][:-cut]
					read_2_l[10] = read_2_l[10][:-cut]
					print("\t".join(read_1_l))
					print("\t".join(read_2_l))
				if start_2 > start_1 and end_2 <= end_1:
					cut = start_2 - start_1
					counter = 0
					for i in cigar_alp_1:
						counter += 1
						if i == "M":
							break
					if cigar_alp_1[counter] == "I" and int(cigar_num_1[counter-1]) > int(cigar_num_1[counter-2]) - cut:
						cut += int(cigar_num_1[counter-1])
					read_1_l[0] = read_1_l[0]+":"+barcode+":0:"+str(cut)
					read_2_l[0] = read_2_l[0]+":"+barcode+":0:"+str(cut)
					read_1_l[9] = read_1_l[9][cut:]
					read_1_l[10] = read_1_l[10][cut:]
					print("\t".join(read_1_l))
					print("\t".join(read_2_l))
				if start_2 > start_1 and end_2 > end_1:
					cut1 = start_2 - start_1
					cut2 = end_2 - end_1
					counter1 = 0
					for i in cigar_alp_1:
						counter1 += 1
						if i == "M":
							break
					if cigar_alp_1[counter1] == "I" and int(cigar_num_1[counter1-1]) > int(cigar_num_1[counter1-2]) - cut1:
						cut1 += int(cigar_num_1[counter1-1])
					counter2 = 0
					for i in reversed(cigar_alp_2):
						counter2 += 1
						if i == "M":
							break
					if cigar_alp_2[-counter2-1] == "I" and int(cigar_num_2[-counter2-2]) > int(cigar_num_2[-counter2-1]) - cut2:
						cut2 += int(cigar_num_2[-counter2-2])

					read_1_l[0] = read_1_l[0]+":"+barcode+":"+str(cut2)+":"+str(cut1)
					read_2_l[0] = read_2_l[0]+":"+barcode+":"+str(cut2)+":"+str(cut1)
					read_1_l[9] = read_1_l[9][cut1:]
					read_1_l[10] = read_1_l[10][cut1:]
					read_2_l[9] = read_2_l[9][:-cut2]
					read_2_l[10] = read_2_l[10][:-cut2]
					print("\t".join(read_1_l))
					print("\t".join(read_2_l))
		result_l = []
	result_l.append(line)
	pre_name = name

if len(result_l) == 2:
	counter_M_D_1 = 0
	counter_M_D_2 = 0

	read_1 = result_l[0]
	read_2 = result_l[1]

	read_1_l = read_1.split()
	read_2_l = read_2.split()

	read_1_flag = int(read_1_l[1])
	read_2_flag = int(read_2_l[1])

	read_1_cigar = read_1_l[5]
	read_2_cigar = read_2_l[5]

	read_1_cigar_l = []
	read_2_cigar_l = []

	read_1_seq = read_1_l[9]
	read_2_seq = read_2_l[9]

	read_1_q = read_1_l[10]
	read_2_q = read_2_l[10]

	pattern = r"\d+"
	iterator_1 = re.finditer(pattern, read_1_cigar)
	iterator_2 = re.finditer(pattern, read_2_cigar)

	cigar_alp_1 = re.split(pattern, read_1_cigar)
	cigar_alp_2 = re.split(pattern, read_2_cigar)
	cigar_num_1 = re.split(r"\D", read_1_cigar)
	cigar_num_2 = re.split(r"\D", read_2_cigar)

	for match in iterator_1:
		tup = match.span()
		num = match.group()
		if read_1_cigar[tup[1]] == "D" or read_1_cigar[tup[1]] == "M":
			counter_M_D_1 += int(num)
		if read_1_cigar[tup[1]] == "M":
			for i in range(int(num)):
				read_1_cigar_l.append("M")
		if read_1_cigar[tup[1]] == "I":
			for i in range(int(num)):
				read_1_cigar_l.append("I")
		if read_1_cigar[tup[1]] == "S":
			for i in range(int(num)):
				read_1_cigar_l.append("S")
		index = [i for i,x in enumerate(read_1_cigar_l) if x =="S"]
		read_1_seq_l = [read_1_seq[i] for i in range(len(read_1_seq)) if not i in index]
		read_1_l[9] = "".join(read_1_seq_l)
		read_1_q_l = [read_1_q[i] for i in range(len(read_1_q)) if not i in index]
		read_1_l[10] = "".join(read_1_q_l)

	for match in iterator_2:
		tup = match.span()
		num = match.group()
		if read_2_cigar[tup[1]] == "D" or read_2_cigar[tup[1]] == "M":
			counter_M_D_2 += int(num)
		if read_2_cigar[tup[1]] == "M":
			for i in range(int(num)):
				read_2_cigar_l.append("M")
		if read_2_cigar[tup[1]] == "I":
			for i in range(int(num)):
				read_2_cigar_l.append("I")
		if read_2_cigar[tup[1]] == "S":
			for i in range(int(num)):
				read_2_cigar_l.append("S")
		index = [i for i,x in enumerate(read_2_cigar_l) if x =="S"]
		read_2_seq_l = [read_2_seq[i] for i in range(len(read_2_seq)) if not i in index]
		read_2_l[9] = "".join(read_2_seq_l)
		read_2_q_l = [read_2_q[i] for i in range(len(read_2_q)) if not i in index]
		read_2_l[10] = "".join(read_2_q_l)

	start_1 = int(read_1_l[3])
	start_2 = int(read_2_l[3])
	end_1 = start_1 + counter_M_D_1 - 1 
	end_2 = start_2 + counter_M_D_2 - 1

	if read_1_l[6] != "=":
		if read_1_flag & 0x40:
			barcode = barcode_1+"_"+barcode_2
		if read_1_flag & 0x80:
			barcode = barcode_2+"_"+barcode_1
		read_1_l[0] = read_1_l[0]+":"+barcode+":0:0"
		read_2_l[0] = read_2_l[0]+":"+barcode+":0:0"
		print("\t".join(read_1_l))
		print("\t".join(read_2_l))

	elif not read_1_flag & 0x2:
		if not read_1_flag & 0x10 and read_2_flag & 0x10:
			barcode = barcode_1+"_"+barcode_2
			if not(cigar_alp_1[-1] == "S" and int(cigar_num_1[-2]) > int(cigar_num_2[-2])) and not(cigar_alp_2[1] == "S" and int(cigar_num_2[0]) > int(cigar_num_1[0])):
				read_1_l[0] = read_1_l[0]+":"+barcode+":0:0"
				read_2_l[0] = read_2_l[0]+":"+barcode+":0:0"
				print("\t".join(read_1_l))
				print("\t".join(read_2_l))
		elif read_1_flag & 0x10 and not read_2_flag & 0x10:
			barcode = barcode_2+"_"+barcode_1
			if not(cigar_alp_2[-1] == "S" and int(cigar_num_2[-2]) > int(cigar_num_1[-2])) and not(cigar_alp_1[1] == "S" and int(cigar_num_1[0]) > int(cigar_num_2[0])):
				read_1_l[0] = read_1_l[0]+":"+barcode+":0:0"
				read_2_l[0] = read_2_l[0]+":"+barcode+":0:0"
				print("\t".join(read_1_l))
				print("\t".join(read_2_l))
		else:
			if read_1_flag & 0x40:
				barcode = barcode_1+"_"+barcode_2
			if read_1_flag & 0x80:
				barcode = barcode_2+"_"+barcode_1
			read_1_l[0] = read_1_l[0]+":"+barcode+":0:0"
			read_2_l[0] = read_2_l[0]+":"+barcode+":0:0"
			print("\t".join(read_1_l))
			print("\t".join(read_2_l))

	else:
		if not read_1_flag & 0x10:
			barcode = barcode_1+"_"+barcode_2
			if not(cigar_alp_1[-1] == "S" and int(cigar_num_1[-2]) > int(cigar_num_2[-2])) and not(cigar_alp_2[1] == "S" and int(cigar_num_2[0]) > int(cigar_num_1[0])):
				if start_1 <= start_2 and end_1 <= end_2:
					read_1_l[0] = read_1_l[0]+":"+barcode+":0:0"
					read_2_l[0] = read_2_l[0]+":"+barcode+":0:0"
				if start_1 > start_2 and end_1 <= end_2:
					cut = start_1 - start_2
					counter = 0
					for i in cigar_alp_2:
						counter += 1
						if i == "M":
							break
					if cigar_alp_2[counter] == "I" and int(cigar_num_2[counter-1]) > int(cigar_num_2[counter-2]) - cut:
						cut += int(cigar_num_2[counter-1])
					read_1_l[0] = read_1_l[0]+":"+barcode+":0:"+str(cut)
					read_2_l[0] = read_2_l[0]+":"+barcode+":0:"+str(cut)
					read_2_l[9] = read_2_l[9][cut:]
					read_2_l[10] = read_2_l[10][cut:]
				if start_1 <= start_2 and end_1 > end_2:
					cut = end_1 - end_2
					counter = 0
					for i in reversed(cigar_alp_1):
						counter += 1
						if i == "M":
							break
					if cigar_alp_1[-counter-1] == "I" and int(cigar_num_1[-counter-2]) > int(cigar_num_1[-counter-1]) - cut:
						cut += int(cigar_num_1[-counter-2])
					read_1_l[0] = read_1_l[0]+":"+barcode+":"+str(cut)+":0"
					read_2_l[0] = read_2_l[0]+":"+barcode+":"+str(cut)+":0"
					read_1_l[9] = read_1_l[9][:-cut]
					read_1_l[10] = read_1_l[10][:-cut]
				if start_1 > start_2 and end_1 > end_2:
					cut1 = end_1 - end_2
					cut2 = start_1 - start_2
					counter1 = 0
					for i in reversed(cigar_alp_1):
						counter1 += 1
						if i == "M":
							break
					if cigar_alp_1[-counter1-1] == "I" and int(cigar_num_1[-counter1-2]) > int(cigar_num_1[-counter1-1]) - cut1:
						cut1 += int(cigar_num_1[-counter1-2])
					counter2 = 0
					for i in cigar_alp_2:
						counter2 += 1
						if i == "M":
							break
					if cigar_alp_2[counter2] == "I" and int(cigar_num_2[counter2-1]) > int(cigar_num_2[counter2-2]) - cut2:
						cut2 += int(cigar_num_2[counter2-1])
					read_1_l[0] = read_1_l[0]+":"+barcode+":"+str(cut1)+":"+str(cut2)
					read_2_l[0] = read_2_l[0]+":"+barcode+":"+str(cut1)+":"+str(cut2)
					read_1_l[9] = read_1_l[9][:-cut1]
					read_1_l[10] = read_1_l[10][:-cut1]
					read_2_l[9] = read_2_l[9][cut2:]
					read_2_l[10] = read_2_l[10][cut2:]
				print("\t".join(read_1_l))
				print("\t".join(read_2_l))

		if read_1_flag & 0x10:
			barcode = barcode_2+"_"+barcode_1
			if not(cigar_alp_2[-1] == "S" and int(cigar_num_2[-2]) > int(cigar_num_1[-2])) and not(cigar_alp_1[1] == "S" and int(cigar_num_1[0]) > int(cigar_num_2[0])):
				if start_2 <= start_1 and end_2 <= end_1:
					read_1_l[0] = read_1_l[0]+":"+barcode+":0:0"
					read_2_l[0] = read_2_l[0]+":"+barcode+":0:0"
				if start_2 <= start_1 and end_2 > end_1:
					cut = end_2 - end_1
					counter = 0
					for i in reversed(cigar_alp_2):
						counter += 1
						if i == "M":
							break
					if cigar_alp_2[-counter-1] == "I" and int(cigar_num_2[-counter-2]) > int(cigar_num_2[-counter-1]) - cut:
						cut += int(cigar_num_2[-counter-2])
					read_1_l[0] = read_1_l[0]+":"+barcode+":"+str(cut)+":0"
					read_2_l[0] = read_2_l[0]+":"+barcode+":"+str(cut)+":0"
					read_2_l[9] = read_2_l[9][:-cut]
					read_2_l[10] = read_2_l[10][:-cut]
				if start_2 > start_1 and end_2 <= end_1:
					cut = start_2 - start_1
					counter = 0
					for i in cigar_alp_1:
						counter += 1
						if i == "M":
							break
					if cigar_alp_1[counter] == "I" and int(cigar_num_1[counter-1]) > int(cigar_num_1[counter-2]) - cut:
						cut += int(cigar_num_1[counter-1])
					read_1_l[0] = read_1_l[0]+":"+barcode+":0:"+str(cut)
					read_2_l[0] = read_2_l[0]+":"+barcode+":0:"+str(cut)
					read_1_l[9] = read_1_l[9][cut:]
					read_1_l[10] = read_1_l[10][cut:]
				if start_2 > start_1 and end_2 > end_1:
					cut1 = start_2 - start_1
					cut2 = end_2 - end_1
					counter1 = 0
					for i in cigar_alp_1:
						counter1 += 1
						if i == "M":
							break
					if cigar_alp_1[counter1] == "I" and int(cigar_num_1[counter1-1]) > int(cigar_num_1[counter1-2]) - cut1:
						cut1 += int(cigar_num_1[counter1-1])
					counter2 = 0
					for i in reversed(cigar_alp_2):
						counter2 += 1
						if i == "M":
							break
					if cigar_alp_2[-counter2-1] == "I" and int(cigar_num_2[-counter2-2]) > int(cigar_num_2[-counter2-1]) - cut2:
						cut2 += int(cigar_num_2[-counter2-2])
					read_1_l[0] = read_1_l[0]+":"+barcode+":"+str(cut2)+":"+str(cut1)
					read_2_l[0] = read_2_l[0]+":"+barcode+":"+str(cut2)+":"+str(cut1)
					read_1_l[9] = read_1_l[9][cut1:]
					read_1_l[10] = read_1_l[10][cut1:]
					read_2_l[9] = read_2_l[9][:-cut2]
					read_2_l[10] = read_2_l[10][:-cut2]
				print("\t".join(read_1_l))
				print("\t".join(read_2_l))

