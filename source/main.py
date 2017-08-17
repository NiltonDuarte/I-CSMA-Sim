from device_graph import *
from interference_graph import *
from interference_SINR_graph import *
from i_csma import *
from n_csma import *
from network_structure import *
import sys
print "Initializing"



distance = 70.
size = 4
pairDist = 40.
print "Lattice Graph size "+str(size)+" distance "+ str(distance)
lattice = Lattice(size,distance,pairDist)
if False:
	for j in range(size):
 		for i in range(size):
 			print lattice.latticeGraph[i][j][0].position,
 			print lattice.latticeGraph[i][j][1].position,
 		print


#distancia entre os nos de um link 50m

radius = 10.0
numNodes = 8
print "Ring Graph "+str(numNodes)+" nodes radius "+str(radius)
ring = Ring(numNodes, radius, pairDist)
#for i in range(numNodes):
#	print ring.ringGraph[i][0].id,
#	print ring.ringGraph[i][0].position
#	print ring.ringGraph[i][1].id,
#	print ring.ringGraph[i][1].position


interfDist = 80.0
print "Interference Graph for Lattice size "+str(size)+" distance "+ str(distance)+", interference distance "+str(interfDist)

interfGraphLattice = InterferenceGraph(lattice, interfDist)
#for i in interfGraphLattice.edges:
#	print i.id,
#print

interfDist = 8.0
#print "Interference Graph for Ring 8 nodes Radius "+str(radius)+", interference distance "+str(interfDist)

interfGraphRing = InterferenceGraph(ring, interfDist)
#for i in interfGraphRing.edges:
#	print i.id, i.nodes[0].id, i.nodes[1].id
"""
print "I-CSMA ring size 8"
icsma = I_CSMA(interfGraphRing, 1, 20,20, 0.5, 0.5)
sched = iscma.run(100000)

testesIt = 200000
it = testesIt
node0 = icsma.interfGraph.nodes[0]
while it < testesIt:
	it += 1
	if it%100000 == 0: print it
	schedule = icsma.run(1)
	#schedule.append(node0)
	for node in schedule:
		for neighbour in icsma.interfGraph.getNeighbours(node):
			if neighbour in schedule:
				print "ERRO"
print "I-CSMA ring size 8 test FINISHED"
"""
"""
windowSize = 2000
rho = 0.5
print "I-CSMA lattice 4x4 Windows = ", windowSize, " Rho = ",rho
icsma = I_CSMA(interfGraphLattice, 0.1, windowSize,windowSize, rho, 0.5)
testesIt = 50000
it = 0
node0 = icsma.interfGraph.nodes[6]
frequency = [0]*16
schedSizeFrequency = [0]*9
maxSched = 0
while it < testesIt:
	it += 1
	if it%1000 == 0: 
		print it
		queue=0
		for node in icsma.interfGraph.nodes:
			queue+=node.queueSize
		print queue/16.0
	schedule = icsma.run(1)
	schedule.sort(key=lambda node: node.id)
	#maxSched = len(schedule) if len(schedule) > maxSched else maxSched
	schedSizeFrequency[len(schedule)]+=1
	#print "len",len(schedule), "nodes:",
	for node in schedule:
		frequency[node.id] +=1
	#	print node.id,
	#print
	#schedule.append(node0)
	#for node in schedule:
	#	for neighbour in icsma.interfGraph.getNeighbours(node):
	#		if neighbour in schedule:
	#			print "ERRO", node.id, neighbour.id
print "===== RESULTS ====="
queue=0
for node in icsma.interfGraph.nodes:
	queue+=node.queueSize
print frequency
for i in range(4):
	for j in range(4):
		print frequency[4*i+j], "\t",
	print
print schedSizeFrequency
print queue/16.0

print "Finished"
"""
"""
testesItTimes = 2
results = []
beta = float(sys.argv[1])
windowSize = 500
f = open('results'+sys.argv[1], 'w')
#0.01, 0.1, 1
#for beta in [0.01,0.03,0.1,0.3,1,3]:
for rho in [0.5,0.7]:
	for i in range(3):
		interfGraphLattice = InterferenceGraph(lattice, 5.1)
		icsma = I_CSMA(interfGraphLattice, beta, windowSize,windowSize, rho, 0.5)
		for j in range(testesItTimes):
			schedule = icsma.run(100000)
			queue=0
			for node in icsma.interfGraph.nodes:
				queue+=node.queueSize
			results.append([i,j,beta,rho,round(queue/16,2)])
			print i,j
		f.write(str(results))
		f.write('\n')
		print results

"""
#testar no i-csma se o escalonamento e factivel, e transferir apenas caso seja.
#
#
def distance(posA, posB):
	sqSum = (posA[0]-posB[0])**2+(posA[1]-posB[1])**2+(posA[2]-posB[2])**2
	dist = sqSum**0.5
	if dist == 0: return 1
	return dist
if False:
	print "Calculo sinr Beta e BG Noise"
	alfa = 2.5
	noise = 9.88211768803e-05/12.
	print "sinr links"
	print lattice.devices[10].id
	aux = 1/distance(lattice.devices[0].position, lattice.devices[10].position)**alpha
	print lattice.devices[4].id
	aux += 1/distance(lattice.devices[0].position, lattice.devices[4].position)**alpha
	print lattice.devices[16].id
	aux += 1/distance(lattice.devices[0].position, lattice.devices[16].position)**alpha
	sinR = (1/distance(lattice.devices[0].position, lattice.devices[1].position)**alpha)/(aux+noise)
	print sinR
	print "device 0 e 0.2 dist"
	sinR = (1/distance(lattice.devices[0].position, lattice.devices[1].position)**alpha)/(1)
	print sinR
	print "device 0 e 1 dist"
	sinR = (1/distance(lattice.devices[0].position, lattice.devices[2].position)**alpha)/(1)
	print sinR
	for i in lattice.devices:
		print str(i.id) + "\t",
		sinR = (1/distance(lattice.devices[0].position, lattice.devices[1].position)**alpha)/(1/distance(lattice.devices[0].position, i.position)**alpha+noise)
		print sinR
	for i in lattice.devices:
		print str(i.id)+ "\t",
		sinR = (1/distance(lattice.devices[0].position, i.position)**alpha)/(noise)
		print sinR

#COLETAR OS RESULTADOS SEPARADAMENTE A MUDANcA DA FUNcAO DE ATIVAcAO E DO MECANIMOS DE DUAS FASES DE DISPUTA
#TESTAR COM OUTRAS TOPOLOGIAS
#INDICE DO REUSO - MEDIA NOS ESCALONADOS/MAX DE NOS ESCALONAVEIS
print "X-CSMA lattice size 4"
#(self, interferenceGraph, beta, W1, W2, rho, trafficMean, interferenceSINRGraph=None)
betaL=[ 0.01, 0.1, 1, 10]
beta=20
alfa = 2.5
W1 = 20
W2 = 8
rhoL = [0.5, 0.6, 0.7, 0.8, 0.9]
rho = 0.7
mean = 0.5
#alpha=2.5
sinrbeta=4.0
noiseBG=9.88211768803e-05/12.
numExps = 3
numIt = 1000000
#f = open('results_sinr_beta'+str(beta), 'w')

interfDist = 80.
for beta in betaL:
	for exps in range(numExps):
		if False:
			interfGraphLattice = InterferenceGraph(lattice, interfDist)
			#sinrGraph = InterferenceSINRGraph(lattice, alpha, sinrbeta, noiseBG)
			icsma = I_CSMA(interfGraphLattice, beta, W1, W2, rho, mean)#, sinrGraph)
			sched = icsma.run(numIt)
			queue=0
			queuesList = []
			n = len(icsma.interfGraph.nodes)
			for node in icsma.interfGraph.nodes:
				queuesList.append(node.queueSize)
				queue += node.queueSize
			results=", ".join(str(x) for x in ([rho , beta, round(queue/n,2)] + queuesList))
			print "I-CSMA",results
		if True:
			interfGraphLattice = InterferenceGraph(lattice, interfDist)
			#sinrGraph = InterferenceSINRGraph(lattice, alpha, sinrbeta, noiseBG)
			ncsma = N_CSMA(interfGraphLattice, beta, W1, W2, rho, mean)#, sinrGraph)
			#for runs in range(numIt):
			sched = ncsma.runCollisionFree(numIt,5)
				#if runs % 10000 == 0: print runs
			queue=0
			queuesList = []
			n = len(ncsma.interfGraph.nodes)
			ncsma.interfGraph.nodes.sort(key=lambda node: node.id)
			for node in ncsma.interfGraph.nodes:
				queuesList.append(round(node.queueSize,4))
				queue += node.queueSize
				if node.id % 4 == 3:
					queuesList.append("\n")
			results=", ".join(str(x) for x in ([rho , beta, round(queue/n,2), "\n"] + queuesList))
			print "N-CSMA",results
			#print "Total Colisions",ncsma.totalCollisionCount
			print "Sched Frequency",ncsma.schedSizeFrequency
			#print "Collision Frequency",ncsma.slotCollisionFrequency
			print "On Nodes Frequency",ncsma.onNodesFrequency
		#f.write(str(results))
		#f.write('\n')
		#f.flush()

