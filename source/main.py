from device_graph import *
from interference_graph import *
from i_csma import *
print "Initializing"

print "Lattice Graph 5x5 distance 5"

distance = 5
size = 5
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

print "Interference Graph for Lattice 5x5 distance 5, interference distance 5.1"

interfGraphLattice = InterferenceGraph(lattice, 5.1)
for i in interfGraphLattice.edges:
	print i.id,
print

print "Interference Graph for Ring 8 nodes Radius 5, interference distance 0.1"

interfGraphRing = InterferenceGraph(ring, 7.0)
for i in interfGraphRing.edges:
	print i.id, i.nodes[0].id, i.nodes[1].id

print "I-CSMA ring size 8"
icsma = I_CSMA(interfGraphRing, 1, 20,20)
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

print "I-CSMA lattice 5x5"
icsma = I_CSMA(interfGraphLattice, 1, 20,20)
testesIt = 200000
it = 0
node0 = icsma.interfGraph.nodes[6]
frequency = [0]*25
schedSizeFrequency = [0]*14
maxSched = 0
while it < testesIt:
	it += 1
	if it%100000 == 0: print it
	schedule = icsma.run(1)
	schedule.sort(key=lambda node: node.id)
	maxSched = len(schedule) if len(schedule) > maxSched else maxSched
	schedSizeFrequency[len(schedule)]+=1
	#print "len",len(schedule), "nodes:",
	for node in schedule:
		frequency[node.id] +=1
	#	print node.id,
	#print
	#schedule.append(node0)
	for node in schedule:
		for neighbour in icsma.interfGraph.getNeighbours(node):
			if neighbour in schedule:
				print "ERRO", node.id, neighbour.id
print frequency
print maxSched
print schedSizeFrequency

print "Finished"