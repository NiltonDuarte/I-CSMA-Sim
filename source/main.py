from device_graph import *
from interference_graph import *
from i_csma import *
import sys
print "Initializing"

print "Lattice Graph 5x5 distance 5"

distance = 5
size = 4
lattice = Lattice(size,distance)

for j in range(size):
 for i in range(size):
 	print lattice.latticeGraph[i][j].position,
 print



radius = 5
numNodes = 8
print "Ring Graph "+str(numNodes)+" nodes radius "+str(radius)
ring = Ring(numNodes, radius)
for i in range(numNodes):
	print ring.ringGraph[i].id,
	print ring.ringGraph[i].position

print "Interference Graph for Lattice 4x4 distance 5, interference distance 5.1"

interfGraphLattice = InterferenceGraph(lattice, 5.1)
#for i in interfGraphLattice.edges:
#	print i.id,
#print
"""
print "Interference Graph for Ring 8 nodes Radius 5, interference distance 0.1"

interfGraphRing = InterferenceGraph(ring, 7.0)
#for i in interfGraphRing.edges:
#	print i.id, i.nodes[0].id, i.nodes[1].id

print "I-CSMA ring size 8"
icsma = I_CSMA(interfGraphRing, 1, 20,20, 0.5)
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
rho = 0.4
print "I-CSMA lattice 4x4 Windows = ", windowSize, " Rho = ",rho
icsma = I_CSMA(interfGraphLattice, 1, windowSize,windowSize, rho)
testesIt = 100000
it = 0
node0 = icsma.interfGraph.nodes[6]
frequency = [0]*25
schedSizeFrequency = [0]*14
maxSched = 0
while it < testesIt:
	it += 1
	if it%100000 == 0: 
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
print schedSizeFrequency
print queue/16.0

print "Finished"
"""

testesItTimes = 3
results = []
beta = float(sys.argv[1])
windowSize = 200
f = open('results'+sys.argv[1], 'w')
#0.01, 0.1, 1
#for beta in [0.01,0.03,0.1,0.3,1,3]:
for rho in [0.2,0.5,0.7]:
	for i in range(3):
		interfGraphLattice = InterferenceGraph(lattice, 5.1)
		windowSize = 50
		icsma = I_CSMA(interfGraphLattice, beta, windowSize,windowSize, rho)
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



