# -*- coding: utf-8 -*-
from random import *

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

	def getValue(self,rho):
		L=0.168
		H=1000
		U=random()
		g=1.5
		x=(-(U*(H**g)-U*(L**g)-H**g)/(H*L)**g)**(-1/g)
		#x = 1/((1-random()*(1-(L/H)**g))/L**g)**(1/g)
		mean=((L**g)/(1-(L/H)**g))*(g/(g-1))*((1/(L**(g-1)))-(1/H**(g-1)))
		#print mean
		return rho*x
		#return paretovariate(1)


class Node:
	def __init__(self, idf):
		self.id = idf
		self.edges=[]
		#I-CSMA state {-1,Av} ou {-1,+1}(Ising)
		self.state = -1
		self.backoff = None
		self.silenced = False
		self.visited = False
		self.queueSize = 0
		self.S = None
		self.q = None
		
	def addEdge(self, e):
		self.edges.append(e)
		return self

	def setBackoff(self,time):
		self.backoff=time
		return self

	def setState(self,st):
		self.state = st
		return self

	def setSilenced(self, st):
		self.silenced = st
		return self

	def resetVisit(self):
		self.visited = False

	def resetSilence(self):
		self.silenced = False

	def getQueueSize(self):
		return self.queueSize

	def fillQueue(self,rho):
		self.queueSize+= Queue().getValue(rho)

	def dumpQueue(self):
		if self.queueSize < 1: self.queueSize = 0 
		else: self.queueSize -= 1

	def setS(self,value):
		self.S = value

	def set_q(self,value):
		self.q = value

	def get_q(self):
		return self.q

class Edge:
	def __init__(self, idf, nodeA, nodeB):
		self.id = idf
		self.nodes = [nodeA, nodeB]

	def destiny(self,source):
		if source == self.nodes[0]:
			return self.nodes[1]
		if source == self.nodes[1]:
			return self.nodes[0]
		raise NameError("Edge has no destiny")

