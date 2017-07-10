from device_graph import *
from interference_graph import *
from interference_SINR_graph import *
from i_csma import *
from network_structure import *
import sys
print "Initializing"

distance = 5
size = 4
lattice = Lattice(size,distance)

interfGraphLattice = InterferenceGraph(lattice, 5.1)


windowSize = 20
rho = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
beta = float(sys.argv[1])
testesIt = 1000000
rounds = 30
f = open('results'+sys.argv[1], 'w')

for i in range(30):
	for r in rho:
		interfGraphLattice = InterferenceGraph(lattice, 5.1)
		icsma = I_CSMA(interfGraphLattice, beta, windowSize, windowSize, r, 0.5)	
		print "I-CSMA Window = ", windowSize, " Rho = ",r, " beta = ", beta, " it = ", i
		schedule = icsma.run(testesIt)
		queue=0
		queuesList = []
		icsma.interfGraph.nodes.sort(key=lambda node: node.id)
		for node in icsma.interfGraph.nodes:
			queuesList.append(node.queueSize)
			queue += node.queueSize
		results=[r , beta, round(queue/16.0,2), queuesList]
		f.write(str(results))
		f.write('\n')
		f.flush()