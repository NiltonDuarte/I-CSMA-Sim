from device_graph import *
from interference_graph import *
from interference_SINR_graph import *
from i_csma import *
from network_structure import *
import sys
print "Initializing sim"



distance = 70.
size = 4
pairDist = 40.
print "Lattice Graph size "+str(size)+" distance "+ str(distance)+" pair distance " + str(pairDist)
lattice = Lattice(size,distance,pairDist)

windowP1 = 20
windowP2 = 8
#rho = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
rho = map(float, sys.argv[2:])
arrivalMean = 0.5
beta = float(sys.argv[1])
testesIt = 1000000
rounds = 30
interfDist = 80.
alpha=2.5
sinrbeta=4.0
noiseBG=9.88211768803e-05/12.
print "Using rho = "+str(rho) + " and beta = "+str(beta)
strRho = ",".join(str(int(10*x)) for x in rho)
f = open('results_beta'+sys.argv[1]+'_r'+strRho+'.csv', 'w')
header = "Rho, Beta, QMean, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16\n"
f.write(str(header))
f.flush()

for i in range(rounds):
	for r in rho:
		interfGraphLattice = InterferenceGraph(lattice, interfDist)
		sinrGraph = InterferenceSINRGraph(lattice, alpha, sinrbeta, noiseBG)
		icsma = I_CSMA(interfGraphLattice, beta, windowP1, windowP2, r, arrivalMean, sinrGraph)	
		print "I-CSMA Window = ", (windowP1, windowP2), " Rho = ",r, " beta = ", beta, " it = ", i
		schedule = icsma.runWithSINR(testesIt)
		queue=0
		queuesList = []
		icsma.interfGraph.nodes.sort(key=lambda node: node.id)
		for node in icsma.interfGraph.nodes:
			queuesList.append(node.queueSize)
			queue += node.queueSize
		results=", ".join(str(x) for x in ([r , beta, round(queue/16.0,2)] + queuesList))
		print results
		f.write(str(results))
		f.write('\n')
		f.flush()