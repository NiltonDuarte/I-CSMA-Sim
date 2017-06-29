# -*- coding: utf-8 -*-

from interference_graph import *
from math import *
from random import *

class I_CSMA:
	def __init__(self, interferenceGraph, beta, W1, W2, rho):
		self.b = beta
		self.interfGraph = interferenceGraph
		self.W1 = W1
		self.W2 = W2
		self.maxD = interferenceGraph.getMaxDegree()
		self.rho = rho

	def run(self, iterations):
		it = 0
		while it < iterations:
			self.controlPhase1()
			schedule = self.controlPhase2()
			it += 1
		return schedule

	def S(self, node):
		#sum of the node neighbours state(spins). desc after eq 5
		neighbours = self.interfGraph.getNeighbours(node)
		S = 0
		for neighbour in neighbours:
			S += neighbour.state
		return S

	def q(self, node):
	 	#eq 5
	 	#Av=self.queueFunction(node.getQueueSize())
	 	ret = 0.5*(1-tanh((node.state+1)*self.b*self.S(node)/2))
	 	#ret = 0.5*(1-tanh((Av+1)*self.b*self.S(node)/2))
	 	return ret

	def silenceNeighbours(self, node):
		#avoid bouncing
		if node.visited: return
		node.visited = True
		for neighbour in self.interfGraph.getNeighbours(node):
					#collision
		 			if neighbour.setSilenced(True).backoff == node.backoff:
		 				node.setSilenced(True)
		 				self.silenceNeighbours(neighbour)
	def queueFunction(self, queue):
		return 2*(self.maxD-1)+log(queue+1)

	def updateState(self, node):
		if random() < node.get_q():
			node.setState(self.queueFunction(node.getQueueSize()))
		else:
			node.setState(-1)

	def controlPhase1(self):
		#calc S and q based on prev time slot
		#map(lambda node: node.setS(self.S(node)), self.interfGraph.nodes)
		map(lambda node: node.set_q(self.q(node)), self.interfGraph.nodes)
		#fill queues
		map(lambda node: node.fillQueue(self.rho), self.interfGraph.nodes)
		#reset visited control variable
		map(lambda node: node.resetVisit(), self.interfGraph.nodes)
		map(lambda node: node.resetSilence(), self.interfGraph.nodes)
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
		#reset visited and silenced control variable
		map(lambda node: node.resetVisit(), self.interfGraph.nodes)
		map(lambda node: node.resetSilence(), self.interfGraph.nodes)
		#set random backoff
	 	map(lambda node: node.setBackoff(randint(0,self.W2)), self.interfGraph.nodes)
	 	#sort
	 	self.interfGraph.nodes.sort(key=lambda node: node.backoff)
	 	slotSchedule = []
	 	#send RESERVE
	 	for node in self.interfGraph.nodes:
	 		if node.state != -1:
	 			self.silenceNeighbours(node)
	 		#if not node.silenced and node.state != -1:
	 		#	self.silenceNeighbours(node)
	 			#if ack collided, this node is silenced now
	 			if not node.silenced:
	 				slotSchedule.append(node)
	 	#dump schedules queues
		map(lambda node: node.dumpQueue(), slotSchedule)
	 	return slotSchedule