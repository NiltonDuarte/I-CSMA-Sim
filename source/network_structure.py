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
	pass	

class TrafficDistribution:
	def __init__(self):
		self.L=None

	def getNewValue(self):
		L=self.L
		H=1000
		U=random()
		g=1.5
		x=(-(U*(H**g)-U*(L**g)-H**g)/(H*L)**g)**(-1/g)
		#x = 1/((1-random()*(1-(L/H)**g))/L**g)**(1/g)
		#mean=((L**g)/(1-(L/H)**g))*(g/(g-1))*((1/(L**(g-1)))-(1/H**(g-1)))
		#print mean
		return x
		#return paretovariate(1)
	
	def calc_L(self, targetMean):
		H=1000
		g=1.5
		meanDelta = 0.001
		L_step = 0.02
		L=0.16
		direction=1
		currMean=((L**g)/(1-(L/H)**g))*(g/(g-1))*((1/(L**(g-1)))-(1/H**(g-1)))
		while abs(targetMean-currMean)>meanDelta:
			if targetMean > currMean:
				if direction==-1: L_step/=2
				L+=L_step
				direction = 1
			else: 
				if direction==1: L_step/=2
				L-=L_step
				direction = -1
			currMean=((L**g)/(1-(L/H)**g))*(g/(g-1))*((1/(L**(g-1)))-(1/H**(g-1)))
		self.L = L
		return L

class Node:
	def __init__(self, obj, idf):
		self.id = idf
		self.edges=[]
		#I-CSMA state {-1,Av} ou {-1,+1}(Ising)
		self.state = -1
		self.backoff = None
		self.silenced = False
		self.visited = False
		self.collided = False
		self.queueSize = 0
		self.S = None
		self.q = None
		self.sourceObj = obj
		
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

	def setCollided(self, st):
		self.collided=st
		return self

	def resetVisit(self):
		self.visited = False

	def resetSilence(self):
		self.silenced = False

	def resetCollided(self):
		self.collided = False

	def resetCtrlVars(self):
		self.visited = False
		self.silenced = False
		self.collided = False

	def getQueueSize(self):
		return self.queueSize

	def fillQueue(self,val):
		self.queueSize+= val

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
	def __init__(self, idf, nodeA, nodeB, weight=None):
		self.id = idf
		self.nodes = [nodeA, nodeB]
		self.weight = weight

	def setWeight(self, value):
		self.weight = value
		return self

	def getWeight(self):
		return self.weight

	def destiny(self,source):
		if source == self.nodes[0]:
			return self.nodes[1]
		if source == self.nodes[1]:
			return self.nodes[0]
		raise NameError("Edge has no destiny")

