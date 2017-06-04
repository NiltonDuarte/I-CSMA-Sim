# -*- coding: utf-8 -*-

from interference_graph import *
from math import *
from random import *

class I_CSMA:
	def __init__(self, interferenceGraph, beta, W1, W2):
		self.b = beta
		self.interfGraph = interferenceGraph
		self.W1 = W1
		self.W2 = W2
		self.initSystem()
		self.controlPhase1()

	def S(self, node):
		#sum of the node neighbours state(spins). desc after eq 5
		neighbours = self.interfGraph.getNeighbours(node)
		S = 0
		for neighbour in neighbours:
			S += neighbour.state
		return S

	def q(self, node):
	 	#eq 5
	 	return 0.5*(1-tanh((node.state+1)*self.b*self.S(node)/2))

	def silenceNeighbours(self, node):
		#avoid bouncing
		if node.visited: return
		node.visited = True
		for neighbour in self.interfGraph.getNeighbours(node):
					#collision
		 			if neighbour.setSilenced(True).backoff == node.backoff:
		 				node.setSilenced(True)
		 				self.silenceNeighbours(neighbour)

	def updateState(self, node):
		if random() < self.q(node):
			node.setState(node.getQueue())
		else:
			node.setState(-1)

	def initSystem(self):
		#map(lambda node: node.state=randint(0,1)*node.getQueue(), self.interfGraph.nodes)
		#init system with random states
		for node in self.interfGraph.nodes:
			if randint(0,1):
				node.setState(node.getQueue())
			else:
				node.setState(-1)
		#for node in self.interfGraph.nodes: print(node.state)
		#print "system initiated"

	def controlPhase1(self):
		#set random backoff
	 	backoffs = [node.setBackoff(randint(0,self.W1)) for node in self.interfGraph.nodes]
	 	#sort
	 	backoffs.sort(key=lambda node: node.backoff)
	 	#send INTENT
	 	for node in backoffs:
	 		if not node.silenced:
	 			self.silenceNeighbours(node)
	 			#if ack collided, this node is silenced now
	 			if not node.silenced:
	 				self.updateState(node)
	 	#for node in self.interfGraph.nodes: print node.backoff, node.state
		 		