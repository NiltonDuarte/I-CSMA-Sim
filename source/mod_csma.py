# -*- coding: utf-8 -*-

from interference_graph import *
from math import *
from random import *
from network_structure import *

class MOD_CSMA:
	def __init__(self, interferenceGraph, beta, W1, W2, rho, trafficMean, interferenceSINRGraph=None):
		self.b = beta
		self.interfGraph = interferenceGraph
		self.W1 = W1
		self.W2 = W2
		self.CP2W=8
		self.maxD = interferenceGraph.getMaxDegree()
		self.rho = rho
		self.traffic = TrafficDistribution()
		self.traffic.calc_L(rho*trafficMean)
		self.interfSINRGraph = interferenceSINRGraph
		self.numNodes = len(interferenceGraph.nodes)
		self.useSINR = False
		self.useHeuristic = False
		self.OFF = -1
		self.totalCollisionCount = 0
		self.slotCollisionCount = 0
		self.slotCollisionFrequency = [0]*(self.numNodes+2)
		self.schedSizeFrequency = [0]*(self.numNodes+1)
		self.onNodesCount = 0
		self.onNodesFrequency = [0]*(self.numNodes+1)

		self.newQueueFunc = False
		self.newSFunc = False
		self.newQProb = False
		self.newCP2 = False

	def turnNewIdeias(self, newQF, newSF, newQP, newCP2):
		self.newQueueFunc = newQF
		self.newSFunc = newSF
		self.newQProb = newQP
		self.newCP2 = newCP2
		if not newCP2:
			self.W2 += self.CP2W

	def _run(self, iterations):
		it = 0
		while it < iterations:
			self.slotCollisionCount=0
			self.onNodesCount=0
			if self.useHeuristic:
				self.heuristicControlPhase1()
			else:
				self.controlPhase1()
			slotSchedule = self.controlPhase2()
			self.schedSizeFrequency[len(slotSchedule)]+=1
			self.totalCollisionCount+=self.slotCollisionCount
			if self.slotCollisionCount > self.numNodes:
				self.slotCollisionCount = self.numNodes+1
			self.slotCollisionFrequency[int(self.slotCollisionCount)]+=1
			self.onNodesFrequency[self.onNodesCount]+=1		
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

	def S(self, node):
		#sum of the node neighbours state(spins). desc after eq 5
		neighbours = self.interfGraph.getNeighbours(node)
		S = 0.0
		for neighbour in neighbours:
			S += neighbour.state
		#print node.id, S
		if self.newSFunc:
			return S/len(neighbours)
		return S

	def q(self, node):
	 	#eq 5
	 	Av=self.queueFunction(node.getQueueSize())
	 	if self.newQProb == "tanhdif":
	 		x = self.b*(Av-self.S(node))
	 		ret= 0.5*(1+tanh(x))
	 	elif self.newQProb == "sech":
	 		ret = 1-(1/cosh((Av+1)*self.b*self.S(node)/2))
	 	else:
	 		ret = 0.5*(1-tanh((Av+1)*self.b*self.S(node)/2))
	 	#print ret
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
		if self.newQueueFunc:
			return self.newQFunc(queue)
		return self.origQFunc(queue)

	def newQFunc(self,queue):
		return log(queue+1)

	def origQFunc(self,queue):
		return 2*(self.maxD-1)+log(queue+1)

	def updateState(self, node):
		if random() < node.get_q():
			Av = self.queueFunction(node.getQueueSize())
			node.setState(Av)
			#print node.id, Av
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

	 	if self.newCP2:
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


