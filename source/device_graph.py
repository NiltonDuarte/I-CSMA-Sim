# -*- coding: utf-8 -*-
import math
from random import *
from network_structure import *

class Lattice:
	#each point in the lattice will have one device linked with its pair
	def __init__(self, size, distance, pairDist):
		self.latticeGraph = [[0 for x in range(size)] for y in range(size)]
		#list of nodes(devices)
		self.devices = []
		#list of links
		self.links = []
		for i in range(size):
			for j in range(size):
				#device position
				pos=[i*distance,j*distance, 0]
				#create device
				device1 = Device(j*size+i, pos, Queue())
				#device position
				pos=[i*distance,j*distance, pairDist]
				#create device
				device2 = Device(0.2+j*size+i, pos, Queue())
				#create a link to itself
				link = Link(j*size+i, device1, device2)
				device1.addLink(link)
				device2.addLink(link)

				self.latticeGraph[i][j]= (device1, device2)
				self.devices.append(device1)
				self.devices.append(device2)
				self.links.append(link)

class Ring:
	#each point in the ring is a device and are connected its pair
	def __init__(self, numNodes, radius, pairDist):
		self.ringGraph = [0 for x in range(numNodes)]
		angularDistance = 2*math.pi/numNodes
		#list of nodes(devices)
		self.devices = []
		#list of links
		self.links = []
		for i in range(numNodes):
			#device position
			pos=[round(math.cos(i*angularDistance)*radius,10), round(math.sin(i*angularDistance)*radius,10), 0]
			#create device
			device1 = Device(i, pos, Queue())
			self.devices.append(device1)
			pos=[round(math.cos(i*angularDistance)*radius,10), round(math.sin(i*angularDistance)*radius,10), pairDist]
			#create device
			device2 = Device(0.2+i, pos, Queue())
			self.ringGraph[i]=(device1, device2)
			self.devices.append(device2)
			link = Link(i, device1, device2)
			device1.addLink(link)
			device2.addLink(link)
			self.links.append(link)


class RandomTopology:
	#each point is a device and is connected to every near(by distance) device
	def __init__(self, numNodes, xSize, ySize, pairDist):
		self.xSize = xSize
		self.ySize = ySize
		self.pairDist=pairDist
		self.numNodes = numNodes
		#list of nodes(devices)
		self.devices = []
		#list of links
		self.links = []


	def allRandom(self):
		for i in range(self.numNodes):
			pos = [uniform(0,self.xSize), uniform(0,self.ySize),0]
			self.addDevice(i,pos)		

	def nearPrevNode(self, radius):
		pos = [self.xSize/2., self.ySize/2.,0]
		self.addDevice(0,pos) 
		for i in range(1,self.numNodes):
			prevNode = choice(self.devices)
			print math.floor(prevNode.id), "->", i
			X = prevNode.position[0]
			Y = prevNode.position[1]
			ang = 2*math.pi*random()
			r = uniform(0, radius**2)
			r = math.sqrt(r)
			pos = [X+r*math.cos(ang),Y+ r*math.sin(ang),0]
			self.addDevice(i, pos)

	def addDevice(self, idt, pos):
			device1 = Device(idt, pos, Queue())
			self.devices.append(device1)
			pos2 = [pos[0], pos[1], self.pairDist]
			device2 = Device(0.2+idt, pos2, Queue())
			
			self.devices.append(device2)
			link = Link(idt, device1, device2)
			device1.addLink(link)
			device2.addLink(link)
			self.links.append(link)	


if __name__ == "__main__":
	rt = RandomTopology(20,100,100,30)
	rt.nearPrevNode(30)
	for node in rt.devices:
		if node.position[2] == 0:
			print node.position

