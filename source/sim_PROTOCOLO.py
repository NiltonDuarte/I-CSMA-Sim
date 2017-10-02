from device_graph import *
from interference_graph import *
from interference_SINR_graph import *
from n_csma import *
from network_structure import *
import sys
print "Initializing sim"

algorithm = "N"

LattDistance = 70.
LattSize = 4
LattPairDist = 40.
print "Lattice Graph size "+str(LattSize)+" distance "+ str(LattDistance)+" pair distance " + str(LattPairDist)


windowP1 = 20
windowP2 = 8
#rho = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
rho = map(float, sys.argv[2:])
arrivalMean = 0.5
beta = float(sys.argv[1])
testesIt = 1000000
rounds = 30
LattInterfDist = 80.
alpha=2.5
sinrbeta=4.0
noiseBG=9.88211768803e-05/12.
print "Using rho = "+str(rho) + " and beta = "+str(beta)
strRho = ",".join(str(int(10*x)) for x in rho)
f = open('results_proto_'+algorithm+'_beta'+sys.argv[1]+'_r'+strRho+'.csv', 'w')
lattice = Lattice(LattSize,LattDistance,LattPairDist)
interfGraphLattice = InterferenceGraph(lattice, LattInterfDist)
n = len(interfGraphLattice.nodes)
header = "Rho, Beta, QMean"
#queue size
for i in range(n):
	header += ",q"+str(i+1)+" "
#sched size freq
for i in range(n+1):
	header += ",s"+str(i)+" "

header+='\n'
f.write(str(header))
f.flush()

for i in range(rounds):
	for r in rho:
		lattice = Lattice(LattSize,LattDistance,LattPairDist)
		interfGraphLattice = InterferenceGraph(lattice, LattInterfDist)
		sinrGraph = None
		if algorithm =="N":
			xcsma = N_CSMA(interfGraphLattice, beta, windowP1, windowP2, 252+16, r, arrivalMean, sinrGraph)	
			schedule = xcsma.runCollisionFree(testesIt,3,"v1")
		elif algorithm == "I":
			xcsma = I_CSMA(interfGraphLattice, beta, windowP1, windowP2, 280,r, arrivalMean, sinrGraph)	
			schedule = xcsma.run(testesIt)
		print algorithm+"-CSMA Window = ", (windowP1, windowP2), " Rho = ",r, " beta = ", beta, " it = ", i
		
		queue=0
		queuesList = []
		xcsma.interfGraph.nodes.sort(key=lambda node: node.id)
		for node in xcsma.interfGraph.nodes:
			queuesList.append(node.queueSize)
			queue += node.queueSize
		results=", ".join(str(x) for x in ([r , beta, round(queue/n,2)] + queuesList + xcsma.schedSizeFrequency))
		print results
		f.write(str(results))
		f.write('\n')
		f.flush()