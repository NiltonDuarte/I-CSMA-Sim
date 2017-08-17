from math import *
from interference_graph import *
from device_graph import *
from random import *
from network_structure import *

WINNER = 1
IDLE = 0
LOOSER = 2

class Schedule_Algorithm:
	def __init__(self, id, slot):
		self.number = 0
		self.state = IDLE
		self.neighbours = []
		self.id = id
		self.slot = slot

	def genNumber(self, min, max):
		self.number=randint(min,max)
		return self

	def updateState(self):
		win = True
		if self.state != IDLE:
			return
		for nbour in self.neighbours:
			if nbour.state == WINNER:
				self.state = LOOSER
				self.number = 0
				return self
			#elif nbour.state == LOOSER:
			#	self.neighbours.remove(nbour)
			elif self.number < nbour.number:
				win=False
			elif self.number == nbour.number and self.id < nbour.id:
				win=False

		if win:
			self.state=WINNER
		return self

if __name__ == "__main__":
	LattInterfDist = 80.
	LattDistance = 70.
	LattSize = 4
	LattPairDist = 40.
	maxSteps = 0
	stepsFreq=[0]*15
	countFreq=[0]*10

	for i in range(1000000):
		sched = []
		lattice = Lattice(LattSize,LattDistance,LattPairDist)
		interfGraphLattice = InterferenceGraph(lattice, LattInterfDist)
		interfGraphLattice.nodes.sort(key=lambda node: node.id)
		for node in interfGraphLattice.nodes:
			node.sched_algo=Schedule_Algorithm(node.id,0)
			node.sched_algo.genNumber(0,10000)

		for node in interfGraphLattice.nodes:
			node.sched_algo.neighbours=[obj.sched_algo for obj in interfGraphLattice.getNeighbours(node)]


		#print [node.sched_algo.number for node in interfGraphLattice.nodes]

		completed = False
		
		steps = 0
		count = 0
		while not completed:
			steps+=1
			for node in interfGraphLattice.nodes:
				node.sched_algo.updateState()
			completed=True
			for node in interfGraphLattice.nodes:
				if node.sched_algo.state == IDLE:
					completed = False

		for node in interfGraphLattice.nodes:
			if node.sched_algo.state == WINNER:
				count += 1
				sched.append(node)
		if count > 8:
			print steps
			print [node.id for node in sched]

			for node in interfGraphLattice.nodes:
				print node.sched_algo.number,
			 	if node.id%4==3:
			 		print
		print "==SCHED=="
		for node in interfGraphLattice.nodes:
			print node.sched_algo.state,
			if node.id%4==3:
				print			 		
			#print [node.sched_algo.state for node in interfGraphLattice.nodes]
			#print [node.sched_algo.number for node in interfGraphLattice.nodes]
			#i=0
			#for node in interfGraphLattice.nodes:
			#	print node.sched_algo.state,
			#	i+=1
			#	if i%4==0: print
			#print "======================"
		if i%100==0:
			print i
			print stepsFreq
			print countFreq
		stepsFreq[steps]+=1
		countFreq[count]+=1
	print stepsFreq
	print countFreq

