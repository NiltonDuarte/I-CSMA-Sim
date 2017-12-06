import sys
import time
print sys.argv
"""
l = map(int, sys.argv[2:])
print l
class A:
	def __init__(self, a):
	 	self.a = a
	def get(self):
		return self.a
	def set(self):
		self.a=0
		return self

listA = [A(i) for i in range(4000000)]
init = time.clock()
l = [x.a - x.a for x in listA]
print time.clock() - init
print l[10] == 0

#l = map(int, sys.argv[2:])
init = time.clock()
l = map(lambda x: x.a-x.a, listA)
print time.clock() - init
print l[10] == 0


init = time.clock()
l = [x.set() for x in listA]
print time.clock() - init
print l[10].a == 0
#print l
#l = map(int, sys.argv[2:])
init = time.clock()
l = map(lambda x: x.set(), listA)
print time.clock() - init
print l[10].a == 0
"""
rho = [0.8, 0.9, 1.0]
beta =[0.1, 1, 1.5]
gamma = [2.0, 2.5]
algorithms = ["MICEe-ICSMA", "MICEe-CFv2", "MICEe-CFv4"]
#["MICE-ICSMAPURE", "MICEe-TrueCFGDv2", "MICEe-TrueCFGDv4", "MICEe-CFv2-UT", "MICEe-CFv4-UT", "MICE-ICSMAPURE-UT", "MICEe-TrueCFGDv2-UT", "MICEe-TrueCFGDv4-UT", "MICEe-CFv2-UT2", "MICEe-CFv4-UT2", "MICE-ICSMAPURE-UT2", "MICEe-TrueCFGDv2-UT2", "MICEe-TrueCFGDv4-UT2"]
#["MICE10-ICSMA", "MICEe-ICSMA", "MICE10-CFv2", "MICEe-CFv2", "MICE10-CFv4", "MICEe-CFv4", "MICE10-CFGDv2", "MICEe-CFGDv2", "MICE10-CFGDv4", "MICEe-CFGDv4" ]
#["ICSMA-UT2", "CFv4-UT2", "CFv2-UT2", "CFv2-NoQ-UT2", "CFv4-NoQ-UT2", "CFv4NQF-UT2", "CFv2NQF-UT2", "HICSMASEC-UT2", "HICSMASECNQF-UT2"]
#["ICSMA-UT", "CFv4-UT", "CFv2-UT", "CFv2-NoQ-UT", "CFv4-NoQ-UT", "CFv4NQF-UT", "CFv2NQF-UT", "HICSMASEC-UT", "HICSMASECNQF-UT"]#["ICSMA", "HICSMA", "HICSMASEC", "CFv4", "CFv2", "HICSMA-NCP2", "HICSMASEC-NCP2", "CFv2-NoQ", "CFv4-NoQ", "HICSMASECNQF", "CFv4NQF", "CFv2NQF",

hostname=['03']#,'02','03', '04', '11']#, '03', '04']
aux = 0
f = open('gridQsub.sh', 'w')
#for r in rho:
for b in beta:
	for r in rho:
		for algo in algorithms:
			for g in gamma:
				node = "node"+hostname[aux%len(hostname)]
				aux+=1
				argStr = "{} {} {} {}".format(b, r, algo, g)
				#f.write("qsub -e /homesim/nilton.gduarte/error.log -o /homesim/nilton.gduarte/output.log -V -b y -cwd -shell n -q all.q -l hostname="+node+" python sim_PROTOCOLO.py "+str(b)+" "+str(r))
				f.write("qsub -e /homesim/nilton.gduarte/error.log -o /homesim/nilton.gduarte/output.log -V -b y -cwd -shell n -q all.q -l hostname="+node+" python sim_PROTOCOLO.py "+str(argStr))
				f.write('\n')
				f.flush()
f.close()		

print "Finished"