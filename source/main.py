from device_graph import *
from interference_graph import *
from interference_hypergraph import *
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

print "Ring Graph 4 nodes radius 5"
radius = 5
numNodes = 4
ring = Ring(numNodes, radius)
for i in range(numNodes):
	print ring.ringGraph[i].id,
	print ring.ringGraph[i].position

print "Interference Graph for Lattice 5x5 distance 5, interference distance 5.1"

interfGraph = InterferenceGraph(lattice, 5.1)
for i in interfGraph.edges:
	print i.id

print "Interference Graph for Ring 8 nodes Radius 5, interference distance 0.1"

interfGraph = InterferenceGraph(ring, 7.0)
for i in interfGraph.edges:
	print i.id, i.nodes[0].id, i.nodes[1].id

print "I-CSMA"
icsma = I_CSMA(interfGraph, 1, 20,3)

createSets([1,2,3,4])

print "Finished"