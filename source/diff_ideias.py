from device_graph import *
from interference_graph import *
from interference_SINR_graph import *
from i_csma import *
from n_csma import *
from network_structure import *
from mod_csma import *
import sys
print "Initializing"

#COLETAR OS RESULTADOS SEPARADAMENTE A MUDANcA DA FUNcAO DE ATIVAcAO E DO MECANIMOS DE DUAS FASES DE DISPUTA
#TESTAR COM OUTRAS TOPOLOGIAS
#INDICE DO REUSO - MEDIA NOS ESCALONADOS/MAX DE NOS ESCALONAVEIS
print "X-CSMA lattice size 4"
#(self, interferenceGraph, beta, W1, W2, rho, trafficMean, interferenceSINRGraph=None)
betaL=[10]
beta = float(sys.argv[1])
alfa = 2.5
W1 = 0
W2 = 20
rhoL = [0.5, 0.6, 0.7, 0.8, 0.9]
rho = 0.7
mean = 0.5
#alpha=2.5
sinrbeta=4.0
noiseBG=9.88211768803e-05/12.
numExps = 3
numIt = 1000000
file = open('results_diff_ideias_beta'+str(beta)+'_rho'+str(rho)+'.csv', 'w')

LattInterfDist = 80.
LattDistance = 70.
LattSize = 4
LattPairDist = 40.

lattice = Lattice(LattSize,LattDistance,LattPairDist)
interfGraphLattice = InterferenceGraph(lattice, LattInterfDist)
n = len(interfGraphLattice.nodes)
header = "Rho, Beta, NewQF, NewSF, NewQP, NewCP2, Queue Mean, Tot Collision"
#queue size
for i in range(n):
	header += ",q"+str(i+1)+" "
#sched size freq
for i in range(n+1):
	header += ",s"+str(i)+" "
#n. collisions freq
for i in range(n+1):
	header += ",c"+str(i)+" "
#n. on nodes freq
for i in range(n+1):
	header += ",o"+str(i)+" "
file.write(str(header))
file.write('\n')
file.flush()

# builds all possible params argument newQF, newSF, newQP, newCP2
param1 = [False, True]
param2 = [False, True]
if beta < 10:
	param3 = [False, "tanhdif", "sech"]
else:
	param3 = [False, "tanhdif"]
param4 = [False, True]
params = [[a, b, c, d] for a in param1 for b in param2 for c in param3 for d in param4]
for exps in range(numExps):
	#for beta in betaL:
	for newIdeiasParam in params:
		lattice = Lattice(LattSize,LattDistance,LattPairDist)
		interfGraphLattice = InterferenceGraph(lattice, LattInterfDist)
		#sinrGraph = InterferenceSINRGraph(lattice, alpha, sinrbeta, noiseBG)
		modcsma = MOD_CSMA(interfGraphLattice, beta, W1, W2, rho, mean)
		modcsma.turnNewIdeias(*newIdeiasParam)
		sched = modcsma.runHeuristic(numIt)
		queue=0
		queuesList = []	
		modcsma.interfGraph.nodes.sort(key=lambda node: node.id)
		for node in modcsma.interfGraph.nodes:
			queuesList.append(node.queueSize)
			queue += node.queueSize
		results=", ".join(str(x) for x in ([rho, beta]+ newIdeiasParam + [round(queue/n,2), modcsma.totalCollisionCount] + queuesList + modcsma.schedSizeFrequency + modcsma.slotCollisionFrequency + modcsma.onNodesFrequency))
		print "MOD-CSMA",results
		file.write(str(results))
		file.write('\n')
		file.flush()