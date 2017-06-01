# -*- coding: utf-8 -*-
import math
from network_structure import *

class Lattice:
	#each point in the lattice will have one device linked with itself 
	def __init__(self, size, distance):
		self.latticeGraph = [[0 for x in range(size)] for y in range(size)]
		#list of nodes(devices)
		self.devices = []
		#list of links
		self.links = []
		for i in range(size):
			for j in range(size):
				#device position
				pos=[i*distance,j*distance]
				#create device
				device = Device(j*size+i, pos, Queue())
				#create a link to itself
				link = Link(j*size+i, device, device)
				device.addLink(link)

				self.latticeGraph[i][j]= device		
				self.devices.append(device)
				self.links.append(link)

class Ring:
	#each point in the ring is a device and are connected to the neighbours
	def __init__(self, numNodes, radius):
		self.ringGraph = [0 for x in range(numNodes)]
		angularDistance = 2*math.pi/numNodes
		#list of nodes(devices)
		self.devices = []
		#list of links
		self.links = []
		for i in range(numNodes):
			#device position
			pos=[round(math.cos(i*angularDistance)*radius,10), round(math.sin(i*angularDistance)*radius,10)]
			#create device
			device = Device(i, pos,Queue())
			self.ringGraph[i]=device
			self.devices.append(device)
		for i in range(numNodes):
			#create a link with the previous device and add the link to both devices
			link = Link(i, self.ringGraph[i], self.ringGraph[i-1])
			self.ringGraph[i].addLink(link)
			self.ringGraph[i-1].addLink(link)
			self.links.append(link)

class RandomTopology:
	#each point is a device and is connected to every near(by distance) device
	def __init__(self):
		pass