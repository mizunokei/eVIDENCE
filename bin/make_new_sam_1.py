import sys
import re

argv = sys.argv
out_f = open(argv[1])

for line in out_f:
	line = line.replace("\n","")
	line_l = line.split()

	if line_l[0].startswith("@"):
		continue

	flag = int(line_l[1])
	start = int(line_l[3])
	cigar = line_l[5]
	seq = line_l[9]

	if flag & 0x4 or flag & 0x8:
		continue

	pattern = r"\d+"
	cigar_num = re.split(r"\D",cigar)
	cigar_alp = re.split(pattern, cigar)
	iterator = re.finditer(pattern, cigar)

	stem_f = "GTAGCTCA"
	stem_r = "TGAGCTAC"

	if not flag & 0x10:
		barcode = seq[:6]
		line_l.append(barcode)
		if cigar_alp[1] == "H":
			continue

		S_num = int(cigar_num[0])
		if seq[6] == "A":
			stem = "AGTAGCTCA"
			counter = 0
			for i in range(9):
				if seq[6+i] == stem[i]:
					counter += 1
			if counter < 8:
				continue

			if cigar_alp[1] == "M":
				if S_num > 15:
					new_cigar = "15S" + str(S_num - 15) + "M"
					for i in range(1,len(cigar_num)-1):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
					new_start = start + 15

				if S_num == 15:
					if cigar_alp[2] == "D":
						new_cigar = "15S"
						for i in range(2,len(cigar_num)-1):
							new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
						new_start = start + 15 + int(cigar_num[1])
					if cigar_alp[2] == "I":
						new_cigar = "15S"
						for i in range(1,len(cigar_num)-1):
							new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
						new_start = start + 15
				if S_num < 15:
					sum = 0
					cigar_counter = 0
					start_num = 0
					l = []
					for match in iterator:
						tup = match.span()
						num = match.group()
						l.append(cigar[tup[1]])
						cigar_counter += 1
						if cigar[tup[1]] == "M":
							sum += int(num)
							start_num += int(num)
						if cigar[tup[1]] == "I":
							sum += int(num)
						if cigar[tup[1]] == "D":
							start_num += int(num)
						if sum >= 15:
							break
					if sum == 15:
						new_cigar = "15S"
						if cigar_alp[cigar_counter+1] == "D":
							for i in range(cigar_counter+1,len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
							new_start = start + start_num + int(cigar_num[cigar_counter])
						else:
							for i in range(cigar_counter,len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
							new_start = start + start_num
					if sum > 15:
						if cigar_alp[cigar_counter] == "M":
							new_cigar = "15S" + str(sum -15) + "M"
							for i in range(cigar_counter,len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
							new_start = start + start_num - (sum -15)							
						if cigar_alp[cigar_counter] == "I":
							new_cigar = "15S" + str(sum -15) + "I"
							for i in range(cigar_counter,len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
							new_start = start + start_num

			if cigar_alp[1] == "S":
				if S_num <= 15:
					cigar_num[0] = "15"
					cigar_num[1] = str(int(cigar_num[1]) - (15 - S_num))
					new_cigar = ""
					for i in range(len(cigar_num)-1):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
					new_start = start + (15 - S_num)
				if S_num > 15:
					cigar_num[0] = "15"
					cigar_num[1] = str(int(cigar_num[1]) - (15 - S_num))
					new_cigar = ""
					for i in range(len(cigar_num)-1):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
					new_start = start + (15 - S_num)
					for n in range(S_num - 15):
						new_seq = seq[n+15:n+23]
						if new_seq == stem_f:
							cigar_num[1] = str(int(cigar_num[1]) - (n+23 - int(cigar_num[0])))
							cigar_num[0] = str(23+n)
							new_cigar = ""
							for j in range(len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[j] + cigar_alp[j+1]
							new_start = start + (23+n - S_num)

			line_l[3] = str(new_start)
			line_l[5] = new_cigar
			print("\t".join(line_l))

		if seq[6] == "T":
			stem = "TCAGTAGCTCA"
			counter = 0
			for i in range(11):
				if seq[6+i] == stem[i]:
					counter += 1
			if counter < 10:
				continue

			if cigar_alp[1] == "M":
				if S_num > 17:
					new_cigar = "17S" + str(S_num - 17) + "M"
					for i in range(1,len(cigar_num)-1):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
					new_start = start + 17

				if S_num == 17:
					if cigar_alp[2] == "D":
						new_cigar = "17S"
						for i in range(2,len(cigar_num)-1):
							new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
						new_start = start + 17 + int(cigar_num[1])
					if cigar_alp[2] == "I":
						new_cigar = "17S"
						for i in range(1,len(cigar_num)-1):
							new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
						new_start = start + 17

				if S_num < 17:
					sum = 0
					cigar_counter = 0
					start_num = 0
					l = []
					for match in iterator:
						tup = match.span()
						num = match.group()
						l.append(cigar[tup[1]])
						cigar_counter += 1
						if cigar[tup[1]] == "M":
							sum += int(num)
							start_num += int(num)
						if cigar[tup[1]] == "I":
							sum += int(num)
						if cigar[tup[1]] == "D":
							start_num += int(num)
						if sum >= 17:
							break
					if sum == 17:
						new_cigar = "17S"
						if cigar_alp[cigar_counter+1] == "D":
							for i in range(cigar_counter+1,len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
							new_start = start + start_num + int(cigar_num[cigar_counter])
						else:
							for i in range(cigar_counter,len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
							new_start = start + start_num
					if sum > 17:
						if cigar_alp[cigar_counter] == "M":
							new_cigar = "17S" + str(sum -17) + "M"
							for i in range(cigar_counter,len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
							new_start = start + start_num - (sum -17)
						if cigar_alp[cigar_counter] == "I":
							new_cigar = "17S" + str(sum -17) + "I"
							for i in range(cigar_counter,len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
							new_start = start + start_num
						
			if cigar_alp[1] == "S":
				if S_num <= 17:
					cigar_num[0] = "17"
					cigar_num[1] = str(int(cigar_num[1]) - (17 - S_num))
					new_cigar = ""
					for i in range(len(cigar_num)-1):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
					new_start = start + (17 - S_num)
				if S_num > 17:
					cigar_num[0] = "17"
					cigar_num[1] = str(int(cigar_num[1]) - (17 - S_num))
					new_cigar = ""
					for i in range(len(cigar_num)-1):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
					new_start = start + (17 - S_num)
					for n in range(S_num - 17):
						new_seq = seq[n+17:n+25]
						if new_seq == stem_f:
							cigar_num[1] = str(int(cigar_num[1]) - (n+25 - int(cigar_num[0])))
							cigar_num[0] = str(25+n)
							new_cigar = ""
							for j in range(len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[j] + cigar_alp[j+1]
							new_start = start + (25+n - S_num)


			line_l[3] = str(new_start)
			line_l[5] = new_cigar
			print("\t".join(line_l))

		if seq[6] == "G":
			stem = "GTAGCTCA"
			counter = 0
			for i in range(8):
				if seq[6+i] == stem[i]:
					counter += 1
			if counter < 7:
				continue

			if cigar_alp[1] == "M":
				if S_num > 14:
					new_cigar = "14S" + str(S_num - 14) + "M"
					for i in range(1,len(cigar_num)-1):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
					new_start = start + 14

				if S_num == 14:
					if cigar_alp[2] == "D":
						new_cigar = "14S"
						for i in range(2,len(cigar_num)-1):
							new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
						new_start = start + 14 + int(cigar_num[1])
					if cigar_alp[2] == "I":
						new_cigar = "14S"
						for i in range(1,len(cigar_num)-1):
							new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
						new_start = start + 14

				if S_num < 14:
					sum = 0
					cigar_counter = 0
					start_num = 0
					l = []
					for match in iterator:
						tup = match.span()
						num = match.group()
						l.append(cigar[tup[1]])
						cigar_counter += 1
						if cigar[tup[1]] == "M":
							sum += int(num)
							start_num += int(num)
						if cigar[tup[1]] == "I":
							sum += int(num)
						if cigar[tup[1]] == "D":
							start_num += int(num)
						if sum >= 14:
							break
					if sum == 14:
						new_cigar = "14S"
						if cigar_alp[cigar_counter+1] == "D":
							for i in range(cigar_counter+1,len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
							new_start = start + start_num + int(cigar_num[cigar_counter])
						else:
							for i in range(cigar_counter,len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
							new_start = start + start_num
					if sum > 14:
						if cigar_alp[cigar_counter] == "M":
							new_cigar = "14S" + str(sum -14) + "M"
							for i in range(cigar_counter,len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
							new_start = start + start_num - (sum -14)							
						if cigar_alp[cigar_counter] == "I":
							new_cigar = "14S" + str(sum -14) + "I"
							for i in range(cigar_counter,len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
							new_start = start + start_num
			if cigar_alp[1] == "S":
				if S_num <= 14:
					cigar_num[0] = "14"
					cigar_num[1] = str(int(cigar_num[1]) - (14 - S_num))
					new_cigar = ""
					for i in range(len(cigar_num)-1):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
					new_start = start + (14 - S_num)
				if S_num > 14:
					cigar_num[0] = "14"
					cigar_num[1] = str(int(cigar_num[1]) - (14 - S_num))
					new_cigar = ""
					for i in range(len(cigar_num)-1):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
					new_start = start + (14 - S_num)
					for n in range(S_num - 14):
						new_seq = seq[n+14:n+22]
						if new_seq == stem_f:
							cigar_num[1] = str(int(cigar_num[1]) - (n+22 - int(cigar_num[0])))
							cigar_num[0] = str(22+n)
							new_cigar = ""
							for j in range(len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[j] + cigar_alp[j+1]
							new_start = start + (22+n - S_num)


			line_l[3] = str(new_start)
			line_l[5] = new_cigar
			print("\t".join(line_l))

		if seq[6] == "C":
			stem = "CAGTAGCTCA"
			counter = 0
			for i in range(10):
				if seq[6+i] == stem[i]:
					counter += 1
			if counter < 9:
				continue

			if cigar_alp[1] == "M":
				if S_num > 16:
					new_cigar = "16S" + str(S_num - 16) + "M"
					for i in range(1,len(cigar_num)-1):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
					new_start = start + 16

				if S_num == 16:
					if cigar_alp[2] == "D":
						new_cigar = "16S"
						for i in range(2,len(cigar_num)-1):
							new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
						new_start = start + 16 + int(cigar_num[1])
					if cigar_alp[2] == "I":
						new_cigar = "16S"
						for i in range(1,len(cigar_num)-1):
							new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
						new_start = start + 16

				if S_num < 16:
					sum = 0
					cigar_counter = 0
					start_num = 0
					l = []
					for match in iterator:
						tup = match.span()
						num = match.group()
						l.append(cigar[tup[1]])
						cigar_counter += 1
						if cigar[tup[1]] == "M":
							sum += int(num)
							start_num += int(num)
						if cigar[tup[1]] == "I":
							sum += int(num)
						if cigar[tup[1]] == "D":
							start_num += int(num)
						if sum >= 16:
							break
					if sum == 16:
						new_cigar = "16S"
						if cigar_alp[cigar_counter+1] == "D":
							for i in range(cigar_counter+1,len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
							new_start = start + start_num + int(cigar_num[cigar_counter])
						else:
							for i in range(cigar_counter,len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
							new_start = start + start_num
					if sum > 16:
						if cigar_alp[cigar_counter] == "M":
							new_cigar = "16S" + str(sum -16) + "M"
							for i in range(cigar_counter,len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
							new_start = start + start_num - (sum -16)							
						if cigar_alp[cigar_counter] == "I":
							new_cigar = "16S" + str(sum -16) + "I"
							for i in range(cigar_counter,len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
							new_start = start + start_num
			if cigar_alp[1] == "S":
				if S_num <= 16:
					cigar_num[0] = "16"
					cigar_num[1] = str(int(cigar_num[1]) - (16 - S_num))
					new_cigar = ""
					for i in range(len(cigar_num)-1):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
					new_start = start + (16 - S_num)
				if S_num > 16:
					cigar_num[0] = "16"
					cigar_num[1] = str(int(cigar_num[1]) - (16 - S_num))
					new_cigar = ""
					for i in range(len(cigar_num)-1):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
					new_start = start + (16 - S_num)
					for n in range(S_num - 16):
						new_seq = seq[n+16:n+24]
						if new_seq == stem_f:
							cigar_num[1] = str(int(cigar_num[1]) - (n+24 - int(cigar_num[0])))
							cigar_num[0] = str(24+n)
							new_cigar = ""
							for j in range(len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[j] + cigar_alp[j+1]
							new_start = start + (24+n - S_num)


			line_l[3] = str(new_start)
			line_l[5] = new_cigar
			print("\t".join(line_l))

	if flag & 0x10:
		barcode = seq[-6:]
		line_l.append(barcode)
		if cigar_alp[-1] == "H":
			continue

		S_num = int(cigar_num[-2])
		if seq[-7] == "A":
			stem = "TGAGCTACTGA"
			counter = 0
			for i in range(11):
				if seq[-17+i] == stem[i]:
					counter += 1
			if counter < 10:
				continue

			if cigar_alp[-1] == "M":
				if S_num > 17:
					new_cigar = ""
					for i in range(len(cigar_num)-2):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
					new_cigar = new_cigar + str(S_num - 17) + "M17S"

				if S_num == 17:
					if cigar_alp[-2] == "D":
						new_cigar = ""
						for i in range(len(cigar_num)-3):
							new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
						new_cigar = new_cigar + "17S"
					if cigar_alp[-2] == "I":
						new_cigar = ""
						for i in range(len(cigar_num)-2):
							new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
						new_cigar = new_cigar + "17S"

				if S_num < 17:
					sum = 0
					cigar_counter = 0
					l = []
					for i in range(2,len(cigar_num)+1):
						l.append(cigar_alp[-i+1])
						cigar_counter += 1
						if cigar_alp[-i+1] == "M" or cigar_alp[-i+1] == "I":
							sum += int(cigar_num[-i])
						if sum >= 17:
							break
					if sum == 17:
						new_cigar = "17S"
						if cigar_alp[-cigar_counter-1] == "D":
							for i in range(cigar_counter+3,len(cigar_num)+1):
								new_cigar = cigar_num[-i] + cigar_alp[-i+1] + new_cigar
						else:
							for i in range(cigar_counter+2,len(cigar_num)+1):
								new_cigar = cigar_num[-i] + cigar_alp[-i+1] + new_cigar
					if sum > 17:
						if cigar_alp[-cigar_counter] == "M":
							new_cigar = str(sum -17) + "M" + "17S"
							for i in range(cigar_counter+2,len(cigar_num)+1):
								new_cigar = cigar_num[-i] + cigar_alp[-i+1] + new_cigar
						if cigar_alp[-cigar_counter] == "I":
							new_cigar = str(sum -17) + "I" + "17S"
							for i in range(cigar_counter+2,len(cigar_num)+1):
								new_cigar = cigar_num[-i] + cigar_alp[-i+1] + new_cigar

			if cigar_alp[-1] == "S":
				if S_num <= 17:
					cigar_num[-2] = "17"
					cigar_num[-3] = str(int(cigar_num[-3]) - (17 - S_num))
					new_cigar = ""
					for i in range(len(cigar_num)-1):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
				if S_num > 17:
					cigar_num[-2] = "17"
					cigar_num[-3] = str(int(cigar_num[-3]) - (17 - S_num))
					new_cigar = ""
					for i in range(len(cigar_num)-1):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
					for n in range(S_num - 17):
						new_seq = seq[-(n+25):-(n+17)]
						if new_seq == stem_r:
							cigar_num[-3] = str(int(cigar_num[-3]) - (n+25 - int(cigar_num[-2])))
							cigar_num[-2] = str(n+25)
							new_cigar = ""
							for j in range(len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[j] + cigar_alp[j+1]

			line_l[5] = new_cigar
			print("\t".join(line_l))
		
		if seq[-7] == "T":
			stem = "TGAGCTACT"
			counter = 0
			for i in range(9):
				if seq[-15+i] == stem[i]:
					counter += 1
			if counter < 8:
				continue

			if cigar_alp[-1] == "M":
				if S_num > 15:
					new_cigar = ""
					for i in range(len(cigar_num)-2):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
					new_cigar = new_cigar + str(S_num - 15) + "M15S"

				if S_num == 15:
					if cigar_alp[-2] == "D":
						new_cigar = ""
						for i in range(len(cigar_num)-3):
							new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
						new_cigar = new_cigar + "15S"
					if cigar_alp[-2] == "I":
						new_cigar = ""
						for i in range(len(cigar_num)-2):
							new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
						new_cigar = new_cigar + "15S"

				if S_num < 15:
					sum = 0
					cigar_counter = 0
					l = []
					for i in range(2,len(cigar_num)+1):
						l.append(cigar_alp[-i+1])
						cigar_counter += 1
						if cigar_alp[-i+1] == "M" or cigar_alp[-i+1] == "I":
							sum += int(cigar_num[-i])
						if sum >= 15:
							break
					if sum == 15:
						new_cigar = "15S"
						if cigar_alp[-cigar_counter-1] == "D":
							for i in range(cigar_counter+3,len(cigar_num)+1):
								new_cigar = cigar_num[-i] + cigar_alp[-i+1] + new_cigar
						else:
							for i in range(cigar_counter+2,len(cigar_num)+1):
								new_cigar = cigar_num[-i] + cigar_alp[-i+1] + new_cigar
					if sum > 15:
						if cigar_alp[-cigar_counter] == "M":
							new_cigar = str(sum -15) + "M" + "15S"
							for i in range(cigar_counter+2,len(cigar_num)+1):
								new_cigar = cigar_num[-i] + cigar_alp[-i+1] + new_cigar
						if cigar_alp[-cigar_counter] == "I":
							new_cigar = str(sum -15) + "I" + "15S"
							for i in range(cigar_counter+2,len(cigar_num)+1):
								new_cigar = cigar_num[-i] + cigar_alp[-i+1] + new_cigar

			if cigar_alp[-1] == "S":
				if S_num <= 15:
					cigar_num[-2] = "15"
					cigar_num[-3] = str(int(cigar_num[-3]) - (15 - S_num))
					new_cigar = ""
					for i in range(len(cigar_num)-1):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
				if S_num > 15:
					cigar_num[-2] = "15"
					cigar_num[-3] = str(int(cigar_num[-3]) - (15 - S_num))
					new_cigar = ""
					for i in range(len(cigar_num)-1):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
					for n in range(S_num - 15):
						new_seq = seq[-(n+23):-(n+15)]
						if new_seq == stem_r:
							cigar_num[-3] = str(int(cigar_num[-3]) - (n+23 - int(cigar_num[-2])))
							cigar_num[-2] = str(n+23)
							new_cigar = ""
							for j in range(len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[j] + cigar_alp[j+1]


			line_l[5] = new_cigar
			print("\t".join(line_l))

		if seq[-7] == "G":
			stem = "TGAGCTACTG"
			counter = 0
			for i in range(10):
				if seq[-16+i] == stem[i]:
					counter += 1
			if counter < 9:
				continue

			if cigar_alp[-1] == "M":
				if S_num > 16:
					new_cigar = ""
					for i in range(len(cigar_num)-2):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
					new_cigar = new_cigar + str(S_num - 16) + "M16S"

				if S_num == 16:
					if cigar_alp[-2] == "D":
						new_cigar = ""
						for i in range(len(cigar_num)-3):
							new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
						new_cigar = new_cigar + "16S"
					if cigar_alp[-2] == "I":
						new_cigar = ""
						for i in range(len(cigar_num)-2):
							new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
						new_cigar = new_cigar + "16S"

				if S_num < 16:
					sum = 0
					cigar_counter = 0
					l = []
					for i in range(2,len(cigar_num)+1):
						l.append(cigar_alp[-i+1])
						cigar_counter += 1
						if cigar_alp[-i+1] == "M" or cigar_alp[-i+1] == "I":
							sum += int(cigar_num[-i])
						if sum >= 16:
							break
					if sum == 16:
						new_cigar = "16S"
						if cigar_alp[-cigar_counter-1] == "D":
							for i in range(cigar_counter+3,len(cigar_num)+1):
								new_cigar = cigar_num[-i] + cigar_alp[-i+1] + new_cigar
						else:
							for i in range(cigar_counter+2,len(cigar_num)+1):
								new_cigar = cigar_num[-i] + cigar_alp[-i+1] + new_cigar
					if sum > 16:
						if cigar_alp[-cigar_counter] == "M":
							new_cigar = str(sum -16) + "M" + "16S"
							for i in range(cigar_counter+2,len(cigar_num)+1):
								new_cigar = cigar_num[-i] + cigar_alp[-i+1] + new_cigar
						if cigar_alp[-cigar_counter] == "I":
							new_cigar = str(sum -16) + "I" + "16S"
							for i in range(cigar_counter+2,len(cigar_num)+1):
								new_cigar = cigar_num[-i] + cigar_alp[-i+1] + new_cigar

			if cigar_alp[-1] == "S":
				if S_num <= 16:
					cigar_num[-2] = "16"
					cigar_num[-3] = str(int(cigar_num[-3]) - (16 - S_num))
					new_cigar = ""
					for i in range(len(cigar_num)-1):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
				if S_num > 16:
					cigar_num[-2] = "16"
					cigar_num[-3] = str(int(cigar_num[-3]) - (16 - S_num))
					new_cigar = ""
					for i in range(len(cigar_num)-1):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
					for n in range(S_num - 16):
						new_seq = seq[-(n+24):-(n+16)]
						if new_seq == stem_r:
							cigar_num[-3] = str(int(cigar_num[-3]) - (n+24 - int(cigar_num[-2])))
							cigar_num[-2] = str(n+24)
							new_cigar = ""
							for j in range(len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[j] + cigar_alp[j+1]


			line_l[5] = new_cigar
			print("\t".join(line_l))

		if seq[-7] == "C":
			stem = "TGAGCTAC"
			counter = 0
			for i in range(8):
				if seq[-14+i] == stem[i]:
					counter += 1
			if counter < 7:
				continue

			if cigar_alp[-1] == "M":
				if S_num > 14:
					new_cigar = ""
					for i in range(len(cigar_num)-2):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
					new_cigar = new_cigar + str(S_num - 14) + "M14S"

				if S_num == 14:
					if cigar_alp[-2] == "D":
						new_cigar = ""
						for i in range(len(cigar_num)-3):
							new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
						new_cigar = new_cigar + "14S"
					if cigar_alp[-2] == "I":
						new_cigar = ""
						for i in range(len(cigar_num)-2):
							new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
						new_cigar = new_cigar + "14S"

				if S_num < 14:
					sum = 0
					cigar_counter = 0
					l = []
					for i in range(2,len(cigar_num)+1):
						l.append(cigar_alp[-i+1])
						cigar_counter += 1
						if cigar_alp[-i+1] == "M" or cigar_alp[-i+1] == "I":
							sum += int(cigar_num[-i])
						if sum >= 14:
							break
					if sum == 14:
						new_cigar = "14S"
						if cigar_alp[-cigar_counter-1] == "D":
							for i in range(cigar_counter+3,len(cigar_num)+1):
								new_cigar = cigar_num[-i] + cigar_alp[-i+1] + new_cigar
						else:
							for i in range(cigar_counter+2,len(cigar_num)+1):
								new_cigar = cigar_num[-i] + cigar_alp[-i+1] + new_cigar
					if sum > 14:
						if cigar_alp[-cigar_counter] == "M":
							new_cigar = str(sum -14) + "M" + "14S"
							for i in range(cigar_counter+2,len(cigar_num)+1):
								new_cigar = cigar_num[-i] + cigar_alp[-i+1] + new_cigar
						if cigar_alp[-cigar_counter] == "I":
							new_cigar = str(sum -14) + "I" + "14S"
							for i in range(cigar_counter+2,len(cigar_num)+1):
								new_cigar = cigar_num[-i] + cigar_alp[-i+1] + new_cigar

			if cigar_alp[-1] == "S":
				if S_num <= 14:
					cigar_num[-2] = "14"
					cigar_num[-3] = str(int(cigar_num[-3]) - (14 - S_num))
					new_cigar = ""
					for i in range(len(cigar_num)-1):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
				if S_num > 14:
					cigar_num[-2] = "14"
					cigar_num[-3] = str(int(cigar_num[-3]) - (14 - S_num))
					new_cigar = ""
					for i in range(len(cigar_num)-1):
						new_cigar = new_cigar + cigar_num[i] + cigar_alp[i+1]
					for n in range(S_num - 14):
						new_seq = seq[-(n+22):-(n+14)]
						if new_seq == stem_r:
							cigar_num[-3] = str(int(cigar_num[-3]) - (n+22 - int(cigar_num[-2])))
							cigar_num[-2] = str(n+22)
							new_cigar = ""
							for j in range(len(cigar_num)-1):
								new_cigar = new_cigar + cigar_num[j] + cigar_alp[j+1]


			line_l[5] = new_cigar
			print("\t".join(line_l))
