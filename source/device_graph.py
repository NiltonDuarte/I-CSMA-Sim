# -*- coding: utf-8 -*-
import math
from network_structure import *

class Lattice:
	#each point in the lattice will have one device linked with itself 
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
	#each point in the ring is a device and are connected to the neighbours
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
	def __init__(self):
		pass