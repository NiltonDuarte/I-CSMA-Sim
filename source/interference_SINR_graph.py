# -*- coding: utf-8 -*-

from network_structure import *

#undirected interference graph

class InterferenceSINRGraph:
	def __init__(self, deviceGraph, alpha, beta, noiseBG):
		self.deviceGraph = deviceGraph
		self.nodes = []
		self.edges = []
		self.alpha = alpha
		self.beta = beta
		self.noiseBG = noiseBG
		self.createGraph()

	def createGraph(self):
		for device in self.deviceGraph.devices:
			node = Node(device, device.id)
			self.nodes.append(node)	
		edgeID=0
		for sourceNode in self.nodes:
			for interfNode in self.nodes:
				if sourceNode.id < interfNode.id:
					weight = self.calcInterference(sourceNode, interfNode)
					edge = Edge(edgeID,sourceNode,interfNode, weight=weight)
					edgeID+=1
					sourceNode.addEdge(edge)
					interfNode.addEdge(edge)
					self.edges.append(edge)

	def calcInterference(self, node, interfNode):
		alpha = self.alpha
		for device in self.deviceGraph.devices:
			if device.id == node.id:
				nodePos=device.position
			if device.id == interfNode.id:
				interfNodePos=device.position
		dist = self.distance(nodePos, interfNodePos)

		return 1/(dist**alpha)

	def distance(self, posA, posB):
		sqSum = (posA[0]-posB[0])**2+(posA[1]-posB[1])**2+(posA[2]-posB[2])**2
		dist = sqSum**0.5
		return dist

	def isFeasible(self, linkSched):
		successLinks = self.successfulTransmissions(linkSched)
		if len(linkSched) == len(successLinks):
			return True
		return False

	def successfulTransmissions(self, linkSched):
		beta = self.beta
		noiseBG = self.noiseBG
		successLinks = []
		schedNode = []
		map(lambda node: node.setState(0), self.nodes)
		for schedLink in linkSched:
			for node in self.nodes:
				if schedLink.sourceObj.devices[0].id == node.id:
					node.setState(1)
					schedNode.append(node)
		for schedLink in linkSched:
			accuInterf=0
			transID = schedLink.sourceObj.devices[0].id
			#print transID,
			recvID = schedLink.sourceObj.devices[1].id
			#print recvID
			linkDist = self.distance(schedLink.sourceObj.devices[0].position, schedLink.sourceObj.devices[1].position)
			for node in self.nodes:
				if recvID == node.id:
					for edge in node.edges:
						dest = edge.destiny(node)
						if dest.id != transID:
							accuInterf+=edge.weight*dest.state
							
			sinr = (1/((linkDist)**self.alpha))/(accuInterf+noiseBG)
			#print sinr
			if sinr > beta:
				successLinks.append(schedLink)

		return successLinks

