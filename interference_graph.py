# -*- coding: utf-8 -*-

from network_structure import *

#undirected interference graph

class InterferenceGraph:
	def __init__(self, deviceGraph, interferenceDistance):
		self.deviceGraph = deviceGraph
		self.interferenceDistance = interferenceDistance
		self.nodes = []
		self.edges = []
		self.createGraph()

	def createGraph(self):
		for link in self.deviceGraph.links:
			node = Node(link.id)
			self.nodes.append(node)
		outterIdx= 0
		innerIdx= 0
		edgeID= 1
		for sourceLink in self.deviceGraph.links:
			innerIdx= 0	
			for link in self.deviceGraph.links[outterIdx+1:]:
				if (self.distance(sourceLink.devices[0],link.devices[0]) <= self.interferenceDistance) or (self.distance(sourceLink.devices[0],link.devices[1]) <= self.interferenceDistance) or (self.distance(sourceLink.devices[1],link.devices[0]) <= self.interferenceDistance) or (self.distance(sourceLink.devices[1],link.devices[1]) <= self.interferenceDistance):
					sourceNode = self.nodes[outterIdx]
					destNode = self.nodes[outterIdx+1+innerIdx]
					edge = Edge(edgeID, sourceNode,  destNode)
					sourceNode.addEdge(edge)
					destNode.addEdge(edge)
					self.edges.append(edge)
					edgeID+= 1
				innerIdx+= 1
			outterIdx+= 1

	def distance(self, deviceA, deviceB):
		sqSum = (deviceA.position[0]-deviceB.position[0])**2+(deviceA.position[1]-deviceB.position[1])**2
		dist = sqSum**0.5
		return dist
