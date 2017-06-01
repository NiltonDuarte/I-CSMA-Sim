# -*- coding: utf-8 -*-


class Device:
	def __init__(self, idf, pos, queue):
		self.id = idf
		self.links=[]
		self.queue=queue
		self.position=pos

	def addLink(self, link):
		self.links.append(link)

	def getLinks(self):
		return self.links


class Link:
	def __init__(self, idf, deviceA, deviceB):
		self.id = idf
		self.devices = [deviceA, deviceB]
		

class Queue:
	def __init__(self):
		pass
	def getSize(self):
		return 9


class Node:
	def __init__(self, idf):
		self.id = idf
		self.edges=[]
		#I-CSMA state {-1,Av} ou {-1,+1}(Ising)
		self.state = None
		
	def addEdge(self, e):
		self.edges.append(e)

	def getNeighbours(self):
		ret = []
		for edge in self.edges:
			ret.append(edge.destiny(self))

class Edge:
	def __init__(self, idf, nodeA, nodeB):
		self.id = idf
		self.nodes = [nodeA, nodeB]

	def destiny(self,source):
		if source == self.nodes[0]:
			return self.nodes[1]
		if source == self.nodes[1]:
			return self.nodes[0]
		return None

