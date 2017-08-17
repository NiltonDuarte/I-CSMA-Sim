# -*- coding: utf-8 -*-

from interference_graph import *
from math import *
from random import *
from network_structure import *
from schedule_algorithm import *

class N_CSMA:
	def __init__(self, interferenceGraph, beta, W1, W2, rho, trafficMean, interferenceSINRGraph=None):
		self.b = beta
		self.interfGraph = interferenceGraph
		self.W1 = W1
		self.W2 = W2
		self.maxD = interferenceGraph.getMaxDegree()
		self.rho = rho
		self.traffic = TrafficDistribution()
		self.traffic.calc_L(rho*trafficMean)
		self.interfSINRGraph = interferenceSINRGraph
		self.useSINR = False
		self.useHeuristic = False
		self.useCollisionFree = False
		self.OFF = -1
		self.totalCollisionCount = 0
		self.slotCollisionCount = 0
		self.slotCollisionFrequency = [0]*(len(interferenceGraph.nodes)+1)
		self.schedSizeFrequency = [0]*(len(interferenceGraph.nodes)+1)
		self.onNodesCount = 0
		self.onNodesFrequency = [0]*(len(interferenceGraph.nodes)+1)
		self.newCP2=8
		self.slot = 0

	def _run(self, iterations):
		it = 0
		while it < iterations:
			self.slotCollisionCount=0
			self.onNodesCount=0
			if self.useHeuristic or self.useCollisionFree:
				self.heuristicControlPhase1()
			else:
				self.controlPhase1()
			if self.useCollisionFree:
				slotSchedule = self.collisionFreePhase2()
				if len(slotSchedule) > 8:
					print [node.id for node in slotSchedule]
				self.slot+=1
			else:
				slotSchedule = self.controlPhase2()
			self.schedSizeFrequency[len(slotSchedule)]+=1			
			self.slotCollisionFrequency[int(self.slotCollisionCount)]+=1
			self.onNodesFrequency[self.onNodesCount]+=1
			self.totalCollisionCount+=self.slotCollisionCount
			it += 1
		return slotSchedule

	def run(self, iterations):
		self.useSINR=False
		return self._run(iterations)

	def runWithSINR(self, iterations):
		if self.interfSINRGraph == None:
			return False
		self.useSINR=True
		return self._run(iterations)

	def runHeuristic(self, iterations):
		self.useHeuristic=True
		return self._run(iterations)

	def runCollisionFree(self, iterations, steps):
		self.interfGraph.nodes.sort(key=lambda node: node.id)
		self.useCollisionFree = True
		if self.slot == 0:
			self.initCtrlPhase(steps)
		return self._run(iterations)

	def S(self, node):
		#sum of the node neighbours state(spins). desc after eq 5
		neighbours = self.interfGraph.getNeighbours(node)
		S = 0.0
		for neighbour in neighbours:
			S += neighbour.state
		#print node.id, S
		return S/len(neighbours)

	def q(self, node):
	 	#eq 5
	 	Av=self.queueFunction(node.getQueueSize())
	 	#ret = 0.5*(1-tanh((node.state+1)*self.b*self.S(node)/2))
	 	x = self.b*(Av-self.S(node))

	 	ret= 0.5*(1+tanh(x))
	 	#ret=1
	 	return ret

	def silenceNeighbours(self, node):
		#avoid bouncing
		if node.visited: return
		node.visited = True
		for neighbour in self.interfGraph.getNeighbours(node):
					#collision
		 			if neighbour.setSilenced(True).backoff == node.backoff:
		 				self.slotCollisionCount+=0.5
		 				node.setSilenced(True)
		 				self.silenceNeighbours(neighbour)

	#Av
	def queueFunction(self, queue):
		return log(queue+1)

	def updateState(self, node):
		if random() < node.get_q():
			Av = self.queueFunction(node.getQueueSize())
			node.setState(Av)
			if self.useCollisionFree:
				self.onNodesCount+=1
		else:
			node.setState(self.OFF)

	def dumpQueue(self, sched):
		if self.useSINR:
			sched = self.interfSINRGraph.successfulTransmissions(sched)
		map(lambda node: node.dumpQueue(), sched)

	def controlPhase1(self):
		#calc S and q based on prev time slot
		#map(lambda node: node.setS(self.S(node)), self.interfGraph.nodes)
		map(lambda node: node.set_q(self.q(node)), self.interfGraph.nodes)
		#fill queues
		map(lambda node: node.fillQueue(self.traffic.getNewValue()), self.interfGraph.nodes)
		#reset visited, silenced and collided control variable
		map(lambda node: node.resetCtrlVars(), self.interfGraph.nodes)
		#set random backoff
	 	map(lambda node: node.setBackoff(randint(0,self.W1)), self.interfGraph.nodes)
	 	#sort
	 	self.interfGraph.nodes.sort(key=lambda node: node.backoff)
	 	#send INTENT
	 	for node in self.interfGraph.nodes:
	 		if not node.silenced:
	 			self.silenceNeighbours(node)
	 			#if ack collided, this node is silenced now
	 			if not node.silenced:
	 				self.updateState(node)
	 	#for node in self.interfGraph.nodes: print node.backoff, node.state

	def controlPhase2(self):
		#reset visited, silenced and collided control variable
		map(lambda node: node.resetCtrlVars(), self.interfGraph.nodes)
		#set random backoff
	 	map(lambda node: node.setBackoff(randint(0,self.W2)), self.interfGraph.nodes)
	 	#sort
	 	self.interfGraph.nodes.sort(key=lambda node: node.backoff)
	 	slotSchedule = []
	 	#send RESERVE
	 	for node in self.interfGraph.nodes:
	 		if node.state != self.OFF:
	 			self.onNodesCount+=1
		 		if not node.silenced:
		 			self.silenceNeighbours(node)
		 			#if ack collided, this node is silenced now
		 			if not node.silenced:
		 				slotSchedule.append(node)

	 	map(lambda node: node.setBackoff(randint(0,self.newCP2)), self.interfGraph.nodes)
	 	#sort
	 	self.interfGraph.nodes.sort(key=lambda node: node.backoff)	 				
	 	for node in self.interfGraph.nodes:
	 		if (not node.silenced and node.state == self.OFF) or node.collided:
	 			self.silenceNeighbours(node)
	 			#if ack collided, this node is silenced now
	 			if not node.silenced:
	 				slotSchedule.append(node)
	 	#dump schedules queues
		self.dumpQueue(slotSchedule)
	 	return slotSchedule

	def heuristicControlPhase1(self):
		#calc S and q based on prev time slot
		map(lambda node: node.set_q(self.q(node)), self.interfGraph.nodes)
		#fill queues
		map(lambda node: node.fillQueue(self.traffic.getNewValue()), self.interfGraph.nodes)	 	
	 	for node in self.interfGraph.nodes:
	 		self.updateState(node)

	def initCtrlPhase(self, steps):
		for i in range(steps):
			for node in self.interfGraph.nodes:
				algo = Schedule_Algorithm(node.id, self.slot)
				algo.genNumber(0,10000)
				node.sched_algo.append(algo)
			for node in self.interfGraph.nodes:
				node.sched_algo[-1].neighbours = [obj.sched_algo[-1] for obj in self.interfGraph.getNeighbours(node)]
			self.slot += 1



	def collisionFreePhase2(self):
		onMinMax = [4001,10000]
		offMinMax=[0,4000]
		slotSchedule = []
		for node in self.interfGraph.nodes:
			schedState = node.sched_algo.pop(0).state
			#print self.slot, node.id, schedState
			for obj in self.interfGraph.getNeighbours(node):
				error = True
				for algo in obj.sched_algo[-2:]:
					if algo.slot == node.sched_algo[-1].slot:
						error = False
						node.sched_algo[-1].neighbours.append(algo)
				if error: print "ERROR"

			for algo in node.sched_algo:
				algo.updateState()

			newAlgo = Schedule_Algorithm(node.id, self.slot)
			if node.state == self.OFF:
				newAlgo.genNumber(*offMinMax)
			else:
				newAlgo.genNumber(*onMinMax)
			node.sched_algo.append(newAlgo)

			if schedState == 1:
				slotSchedule.append(node)
		self.dumpQueue(slotSchedule)
		#print [node.id for node in slotSchedule]
	 	return slotSchedule

