# -*- coding: utf-8 -*-

from network_structure import *

#undirected interference graph

class InterferenceSINRGraph:
	def __init__(self, deviceGraph, alpha, F):
		self.deviceGraph = deviceGraph
		self.nodes = []
		self.edges = []
		self.alpha = alpha
		self.F = F
		self.createGraph()

	def createGraph(self):
		for device in self.deviceGraph.devices:
			node = Node(device, device.id)
			self.nodes.append(node)	
		edgeID=0
		for sourceNode in self.nodes:
			for interfNode in self.nodes:
				if sourceNode.id < interfNode.id:
					weight = self.CalcInterference(sourceNode, interfNode)
					edge = Edge(edgeID,sourceNode,interfNode, weight=weight)
					edgeID+=1
					sourceNode.addEdge(edge)
					interfNode.addEdge(edge)
					self.edges.append(edge)

	def CalcInterference(self, node, interfNode):
		F=self.F
		alpha = self.alpha
		for device in self.deviceGraph.devices:
			if device.id == node.id:
				nodePos=device.position
			if device.id == interfNode.id:
				interfNodePos=device.position
		dist = self.distance(nodePos, interfNodePos)

		return F/(dist**alpha)

	def distance(self, posA, posB):
		sqSum = (posA[0]-posB[0])**2+(posA[1]-posB[1])**2
		dist = sqSum**0.5
		return dist

	def isFeasible(self, beta, noiseBG, linkSched):
		map(lambda node: node.setState(0), self.nodes)
		for schedLink in linkSched:
			for node in self.nodes:
				if schedLink.sourceObj.devices[0].id == node.id:
					node.setState(1)
		
		for schedLink in linkSched:
			accuInterf=0
			transID = schedLink.sourceObj.devices[0].id
			recvID = schedLink.sourceObj.devices[1].id
			linkDist = self.distance(schedLink.sourceObj.devices[0].position, schedLink.sourceObj.devices[1].position)
			for node in self.nodes:
				if recvID == node.id:
					for edge in node.edges:
						dest = edge.destiny(node)
						if dest.id != transID:
							accuInterf+=edge.weight*dest.state
							
			sinr = (self.F/((linkDist)**self.alpha))/(accuInterf+noiseBG)
			if sinr < beta:
				return False
		return True
