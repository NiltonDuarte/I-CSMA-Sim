from math import *
from interference_graph import *
from device_graph import *
from random import *
from network_structure import *
import sys

WINNER = 1
IDLE = 0
LOSER = 2

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
				self.state = LOSER
				self.number = -1
				return self
			#elif nbour.state == LOSER:
			#	self.neighbours.remove(nbour)
			elif self.number < nbour.number:
				win=False
			elif self.number == nbour.number and self.id < nbour.id:
				win=False

		if win:
			self.state=WINNER
		return self

	def updateState2(self):
		higher = 0
		if self.state != IDLE:
			return
		for nbour in self.neighbours:
			if nbour.state == WINNER:
				self.state = LOSER
				self.number = -1
				return self
			#elif nbour.state == LOSER:
			#	self.neighbours.remove(nbour)
			elif self.number < nbour.number:
				higher+=1
			elif self.number == nbour.number and self.id < nbour.id:
				higher+=1

		if higher <= 1:
			self.state=WINNER
		return self

#>>> perm
#[[4, 7, 1, 6, 2, 0, 5, 3], [1, 6, 3, 4, 7, 2, 5, 0], [2, 6, 3, 0, 1, 7, 5, 4]]		
#int(hashlib.sha1('83').hexdigest(),16)%3

if __name__ == "__main__":
	
	LattInterfDist = 80.
	LattDistance = 70.
	LattSize = 4
	LattPairDist = 40.
	maxSteps = 0
	lattice = Lattice(LattSize,LattDistance,LattPairDist)
	interfGraphLattice = InterferenceGraph(lattice, LattInterfDist, True, LattDistance*(LattSize), LattDistance*(LattSize))
	for node in interfGraphLattice.nodes:
		print node.id, interfGraphLattice.getNeighbours(node)
	n = len(interfGraphLattice.nodes)
	stepsFreq=[0]*25
	countFreq=[0]*n

	for i in range(1000000):
		sched = []
		lattice = Lattice(LattSize,LattDistance,LattPairDist)
		interfGraphLattice = InterferenceGraph(lattice, LattInterfDist, True, LattDistance*(LattSize), LattDistance*(LattSize))
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
			shuffle(interfGraphLattice.nodes)
			for node in interfGraphLattice.nodes:
				if sys.argv[1] == 'v1':
					node.sched_algo.updateState()
				if sys.argv[1] == 'v2':
					node.sched_algo.updateState2()
			completed=True
			for node in interfGraphLattice.nodes:
				if node.sched_algo.state == IDLE:
					completed = False
			if steps>10: 
				print '=SCHED='
				for node in interfGraphLattice.nodes:
					print node.sched_algo.state,
					print node.sched_algo.number,
					if node.id%LattSize==(LattSize-1):
						print
		#v3
		if False:	
			for node in interfGraphLattice.nodes:
				if node.sched_algo.state==WINNER:
					neighboursCandidateList=[]
					for neigh in node.sched_algo.neighbours:
						neighsOns=0
						for nneigh in neigh.neighbours:
							if nneigh.state==WINNER:
								neighsOns +=1
						if neighsOns == 0:
							print "Error 1"
						if neighsOns == 1:
							neighboursCandidateList.append(neigh)
					if len(neighboursCandidateList)>1:
						node.sched_algo.state=LOSER
						for nodeschedalgo in neighboursCandidateList:
							nodeschedalgo.state=WINNER

		for node in interfGraphLattice.nodes:
			if node.sched_algo.state == WINNER:
				for neigh in node.sched_algo.neighbours:
					if neigh.state == WINNER:
						print "ERROR 2"
				count += 1
				sched.append(node)
		if count > n/2:
			print '=SCHED2='
			print steps
			print [node.id for node in sched]

			for node in interfGraphLattice.nodes:
				print node.sched_algo.number,
			 	if node.id%LattSize==(LattSize-1):
			 		print
		#print "==SCHED=="
		#for node in interfGraphLattice.nodes:
		#	print node.sched_algo.state,
		#	if node.id%4==3:
		#		print			 		
			#print [node.sched_algo.state for node in interfGraphLattice.nodes]
			#print [node.sched_algo.number for node in interfGraphLattice.nodes]
			#i=0
			#for node in interfGraphLattice.nodes:
			#	print node.sched_algo.state,
			#	i+=1
			#	if i%4==0: print
			#print "======================"
		if i%10000==0:
			print i
			print stepsFreq
			print countFreq
		stepsFreq[steps]+=1
		countFreq[count]+=1
	print stepsFreq
	print countFreq

