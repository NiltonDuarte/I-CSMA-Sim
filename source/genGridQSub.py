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

rho = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

beta = [0.1]#[0.01, 0.1, 1, 10, 100]
gamma = [2.5]#[0.01, 0.1, 1, 10, 100]
delayT = [1, 2, 3, 4, 5, 10, 15, 20]
#params = [(1.5, 'MICEe-CFv2', 2.5), (1.5,'MICEe-TrueCFGDv2', 2.5), (0,'CFv2-NoQ',0), (0.1, 'MICE-ICSMAPURE', 1.5), (0.1,'ICSMA',0), (1, 'MICE-ICSMAPURE', 1.5), (1.5, 'MICE-ICSMAPURE', 1.5), (0.1, 'MICE-ICSMAPURE', 0.5), (0.1, 'MICE-ICSMAPURE', 1.0), (0.1, 'MICE-ICSMAPURE', 2.5)]

#["MICEe-ICSMA", "MICEe-CFv2", "MICEe-CFv4"]
#["MICE-ICSMAPURE", "MICEe-TrueCFGDv2", "MICEe-TrueCFGDv4", "MICEe-CFv2-UT", "MICEe-CFv4-UT", "MICE-ICSMAPURE-UT", "MICEe-TrueCFGDv2-UT", "MICEe-TrueCFGDv4-UT", "MICEe-CFv2-UT2", "MICEe-CFv4-UT2", "MICE-ICSMAPURE-UT2", "MICEe-TrueCFGDv2-UT2", "MICEe-TrueCFGDv4-UT2"]
#["MICE10-ICSMA", "MICEe-ICSMA", "MICE10-CFv2", "MICEe-CFv2", "MICE10-CFv4", "MICEe-CFv4", "MICE10-CFGDv2", "MICEe-CFGDv2", "MICE10-CFGDv4", "MICEe-CFGDv4" ]
#["ICSMA-UT2", "CFv4-UT2", "CFv2-UT2", "CFv2-NoQ-UT2", "CFv4-NoQ-UT2", "CFv4NQF-UT2", "CFv2NQF-UT2", "HICSMASEC-UT2", "HICSMASECNQF-UT2"]
#["ICSMA-UT", "CFv4-UT", "CFv2-UT", "CFv2-NoQ-UT", "CFv4-NoQ-UT", "CFv4NQF-UT", "CFv2NQF-UT", "HICSMASEC-UT", "HICSMASECNQF-UT"]#["ICSMA", "HICSMA", "HICSMASEC", "CFv4", "CFv2", "HICSMA-NCP2", "HICSMASEC-NCP2", "CFv2-NoQ", "CFv4-NoQ", "HICSMASECNQF", "CFv4NQF", "CFv2NQF",

hostname=['01','01','01','02', '02', '10', '10', '10', '11', '11', '11','03']#, '04']
aux = 0
f = open('gridQsub.sh', 'w')

algorithms = ["MICE-ICSMAPURE",     "MICEe-CFv2",     "MICEe-TrueCFGDv2",     "MICEe-CFv4",     "MICEe-TrueCFGDv4",
						  "MICE-ICSMAPURE-UT",  "MICEe-CFv2-UT",  "MICEe-TrueCFGDv2-UT",  "MICEe-CFv4-UT",  "MICEe-TrueCFGDv4-UT",
						  "MICE-ICSMAPURE-UT2", "MICEe-CFv2-UT2", "MICEe-TrueCFGDv2-UT2", "MICEe-CFv4-UT2", "MICEe-TrueCFGDv4-UT2"]
algorithms = ["MICE-ICSMAPURE",     "MICEe-TrueCFGDv2",  "MICEe-TrueCFGDv4",
				"MICE-ICSMAPURE-UT",  "MICEe-TrueCFGDv2-UT", "MICEe-TrueCFGDv4-UT",
				"MICE-ICSMAPURE-UT2", "MICEe-TrueCFGDv2-UT2", "MICEe-TrueCFGDv4-UT2"]
algorithms = []
#MICE Algo's - depende de gamma, beta e rho
if False:
	for b in beta:
		for r in rho:
			for algo in algorithms:
				for g in gamma:
					for T in delayT:
						node = "node"+hostname[aux%len(hostname)]
						aux+=1
						argStr = "{} {} {} {} {}".format(b, r, algo, g, T)
						qsubStr = "qsub -e /homesim/nilton.gduarte/error.log -o /homesim/nilton.gduarte/output.log -V -b y -cwd -shell n -q all.q -l hostname="+node+" python sim_PROTOCOLO.py "
						#qsubStr= "python sim_PROTOCOLO.py "
						f.write(qsubStr+str(argStr))
						f.write('\n')
						f.flush()

#ICSMA - depende apenas de beta e rho
beta = [0.01]#[0.01, 0.1, 1, 10, 100]
#gamma = [2.5]#[0.01, 0.1, 1, 10, 100]
algorithms = ["ICSMA","ICSMA-UT","ICSMA-UT2"]
#algorithms = ["ICSMA-UT","ICSMA-UT2"]
if False:
	for b in beta:
		for r in rho:
			for algo in algorithms:
				for T in delayT:
					node = "node"+hostname[aux%len(hostname)]
					aux+=1
					argStr = "{} {} {} {} {}".format(b, r, algo, -1, T)
					#f.write("qsub -e /homesim/nilton.gduarte/error.log -o /homesim/nilton.gduarte/output.log -V -b y -cwd -shell n -q all.q -l hostname="+node+" python sim_PROTOCOLO.py "+str(b)+" "+str(r))
					qsubStr ="qsub -e /homesim/nilton.gduarte/error.log -o /homesim/nilton.gduarte/output.log -V -b y -cwd -shell n -q all.q -l hostname="+node+" python sim_PROTOCOLO.py " 
					#qsubStr= "python sim_PROTOCOLO.py "
					f.write(qsubStr+str(argStr))
					f.write('\n')
					f.flush()

if False:
	#No Queue - depende apenas de rho
	algorithms = ["CFv2-NoQ", "CFv2-NoQ-UT", "CFv2-NoQ-UT2"]
	if True:
		for r in rho:
			for algo in algorithms:
				for T in delayT:
					node = "node"+hostname[aux%len(hostname)]
					aux+=1
					argStr = "{} {} {} {} {}".format(-1, r, algo, -1, T)
					#f.write("qsub -e /homesim/nilton.gduarte/error.log -o /homesim/nilton.gduarte/output.log -V -b y -cwd -shell n -q all.q -l hostname="+node+" python sim_PROTOCOLO.py "+str(b)+" "+str(r))
					qsubStr ="qsub -e /homesim/nilton.gduarte/error.log -o /homesim/nilton.gduarte/output.log -V -b y -cwd -shell n -q all.q -l hostname="+node+" python sim_PROTOCOLO.py " 
					#qsubStr= "python sim_PROTOCOLO.py "
					f.write(qsubStr+str(argStr))
					f.write('\n')
					f.flush()

#Resultados mais granulares
rho = [0.92, 0.94, 0.96, 0.98]
"""
for r in rho:
	for p in params:
			node = "node"+hostname[aux%len(hostname)]
			aux+=1
			argStr = "{} {} {} {}".format(p[0], r, p[1], p[2])
			#f.write("qsub -e /homesim/nilton.gduarte/error.log -o /homesim/nilton.gduarte/output.log -V -b y -cwd -shell n -q all.q -l hostname="+node+" python sim_PROTOCOLO.py "+str(b)+" "+str(r))
			f.write("qsub -e /homesim/nilton.gduarte/error.log -o /homesim/nilton.gduarte/output.log -V -b y -cwd -shell n -q all.q -l hostname="+node+" python sim_PROTOCOLO.py "+str(argStr))
			f.write('\n')
			f.flush()

"""


#(beta, rho, algo, gamma, delay)
params = []
#RF1 e 2
rho=[0.6,0.7,0.8,0.9,1.0]
miceicsma01=(0.1, 'MICE-ICSMAPURE', 2.5)
icsma01 =(0.1, 'ICSMA',0)
esmasf = (0.0, 'CFv2-NoQ', 0)
miceesma = (1.5, 'MICEe-CFv2', 2.5)
miceesmai = (1.5, 'MICEe-CFv4', 2.5)
micegdesmai = (1.5, "MICEe-TrueCFGDv4", 2.5)
micegdesma = (1.5, "MICEe-TrueCFGDv2", 2.5)
algos = [miceicsma01, icsma01, esmasf, miceesma, miceesmai, micegdesmai, micegdesma]
for r in rho:
	for conf in algos:
		config = (conf[0], r, conf[1], conf[2], 1)
		params.append(config)

#Rf 1
rho=[0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
icsma01 =(0.1, 'ICSMA',0)
icsma001 =(0.01, 'ICSMA',0)
icsma10 =(1.0, 'ICSMA',0)
algos = [icsma01, icsma001, icsma10]
for r in rho:
	for conf in algos:
		config = (conf[0], r, conf[1], conf[2], 1)
		params.append(config)

#Rf 6
rho = [0.8, 0.9, 1.0]	
miceicsma01=(0.1, 'MICE-ICSMAPURE', 2.5)
miceicsma10=(1.0, 'MICE-ICSMAPURE', 2.5)
miceicsma15=(1.5, 'MICE-ICSMAPURE', 2.5)
algos = [miceicsma01, miceicsma10, miceicsma15]
for r in rho:
	for conf in algos:
		config = (conf[0], r, conf[1], conf[2], 1)
		params.append(config)

#Rf 7.1
rho = [0.8, 0.9, 1.0]	
gammas = [0.5, 1.0, 1.5, 2.0]
betas = [0.1, 1.0, 1.5]
algos = [('MICE-ICSMAPURE',0)]
for r in rho:
	for b in betas:
		for g in gammas:
			for conf in algos:
				config = (b, r, conf[0], g, 1)
				params.append(config)
#Rf 9.1
rho = [0.8, 0.9, 1.0]	
miceicsma01=(1.0, 'MICE-ICSMAPURE-UT', 2.5)
icsma01 =(1.0, 'ICSMA-UT',0)
esmasf = (1.0, 'CFv2-NoQ-UT', 0)
miceesma = (1.0, 'MICEe-CFv2-UT', 2.5)
miceesmai = (1.0, 'MICEe-CFv4-UT', 2.5)
micegdesmai = (1.0, "MICEe-TrueCFGDv4-UT", 2.5)
micegdesma = (1.0, "MICEe-TrueCFGDv2-UT", 2.5)
algos = [miceicsma01, icsma01, esmasf, miceesma, miceesmai, micegdesmai, micegdesma]
for r in rho:
	for conf in algos:
		config = (conf[0], r, conf[1], conf[2], 1)
		params.append(config)

#Rf 11.1
rho = [0.8, 0.9, 1.0]	
miceicsmaUT01 = (0.1, 'MICE-ICSMAPURE-UT')
gammas = [0.5, 1.0, 1.5, 2.0, 2.5]
algos = [miceicsmaUT01]
for r in rho:
	for g in gammas:
		for conf in algos:
			config = (conf[0], r, conf[1], g, 1)
			params.append(config)

#Rf 14
rho = [0.8, 0.9, 1.0]	
esma = ('MICEe-TrueCFGDv2-UT2', 2.5)
betas = [0.1, 1.0, 1.5]
algos = [esma]
for r in rho:
	for b in betas:
		for conf in algos:
			config = (b, r, conf[0], conf[1], 1)
			params.append(config)

#Rf 15
rho = [0.8, 0.9, 1.0]	
micegdesma15 = (1.5, "MICEe-TrueCFGDv2", 2.5)
micegdesma01 = (0.1, "MICEe-TrueCFGDv2", 2.5)
micegdesma10 = (1.0, "MICEe-TrueCFGDv2", 2.5)
algos = [micegdesma01, micegdesma10, micegdesma15]
for r in rho:
	for conf in algos:
		config = (conf[0], r, conf[1], conf[2], 1)
		params.append(config)

#Rf 16
rho = [0.8, 0.9, 1.0]	
micegdesma05 = (1.5, "MICEe-TrueCFGDv2", 0.5)
micegdesma10 = (1.5, "MICEe-TrueCFGDv2", 1.0)
micegdesma15 = (1.5, "MICEe-TrueCFGDv2", 1.5)
micegdesma20 = (1.5, "MICEe-TrueCFGDv2", 2.0)
micegdesma25 = (1.5, "MICEe-TrueCFGDv2", 2.5)
algos = [micegdesma05, micegdesma10, micegdesma15, micegdesma20, micegdesma25]
for r in rho:
	for conf in algos:
		config = (conf[0], r, conf[1], conf[2], 1)
		params.append(config)

#Rf 17 e 18
rho = [0.8, 0.9, 1.0]
micegdesmaUT = (1.5, "MICEe-TrueCFGDv2-UT")
micegdesmaUT2 = (1.5, "MICEe-TrueCFGDv2-UT2")
gammas = [0.5, 1.0, 1.5, 2.0, 2.5]
algos = [micegdesmaUT, micegdesmaUT2]
for r in rho:
	for g in gammas:
		for conf in algos:
				config = (conf[0], r, conf[1], g, 1)
				params.append(config)

params = set(params)

for p in params:
		node = "node"+hostname[aux%len(hostname)]
		aux+=1
		argStr = "{} {} {} {} {}".format(p[0], p[1], p[2], p[3], p[4])
		qsubStr="qsub -e /homesim/nilton.gduarte/error.log -o /homesim/nilton.gduarte/output.log -V -b y -cwd -shell n -q all.q -l hostname="+node+" python sim_PROTOCOLO.py "
		qsubStr= "python sim_PROTOCOLO.py "
		f.write(qsubStr+str(argStr))
		f.write('\n')
		f.flush()

f.close()	
print "Finished"