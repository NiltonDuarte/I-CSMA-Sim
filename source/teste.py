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
rho = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
beta=[0.01, 0.03, 0.1, 0.3, 1, 3]
hostname=['01', '02', '03', '04']
aux = 0
f = open('gridQsub.sh', 'w')
for r in rho:
	for b in beta:
		node = "node"+hostname[aux%4]
		aux+=1
		f.write("qsub -e /homesim/nilton.gduarte/error.log -o /homesim/nilton.gduarte/output.log -V -b y -cwd -shell n -q all.q -l hostname="+node+" python sim.py "+str(b)+" "+str(r))
		f.write('\n')
		f.flush()
f.close()		

print "Finished"