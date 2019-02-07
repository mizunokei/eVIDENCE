import sys
import numpy as np
import scipy as sp
from scipy import stats

argv = sys.argv
out_f = open(argv[1])

for line in out_f:
	line = line.replace("\n","")
	line_l = line.split()

	if line_l[0].startswith("#"):
		print(line,"\tp")
		continue
	if int(line_l[-4]) == 0 and int(line_l[-3]) == 0:
		line_l[-4] = "1"
		line_l[-3] = "1"

	array = np.array([[int(line_l[-4]),int(line_l[-3])],[int(line_l[-2]),int(line_l[-1])]])

	if int(line_l[-4]) == 0 and int(line_l[-2]) == 0:
		p = 1.0
	elif int(line_l[-3]) == 0 and int(line_l[-1]) == 0:
		p = 1.0
	else:
		p = sp.stats.fisher_exact(array)[1]
	if p < 0.001:
		print(line,"\t",p)
