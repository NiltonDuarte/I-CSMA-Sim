# -*- coding: utf-8 -*-
import math
from random import *
from network_structure import *
import csv

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
	def __init__(self, numPairs=None, pairDist=None, xSize=None, ySize=None):
		self.xSize = xSize
		self.ySize = ySize
		self.pairDist=pairDist
		self.numNodes = numPairs
		#list of nodes(devices)
		self.devices = []
		#list of links
		self.links = []


	def allRandom(self):
		for i in range(self.numNodes):
			pos = [uniform(0,self.xSize), uniform(0,self.ySize),0]
			self.addDevice(i,pos)		

	def nearPrevNode(self, radiusRange, useMaxDegree=False, maxDegree = None):
		degrees = [0]*self.numNodes
		pos = [self.xSize/2., self.ySize/2.,0]
		self.addDevice(0,pos)
		degrees[0] += 1
		for i in range(1,self.numNodes):
			idx = randint(0,i-1)
			#print idx
			prevNode = self.devices[2*idx]
			if useMaxDegree:
				while degrees[idx] >= maxDegree:
					idx = randint(0,i-1)
			degrees[idx] += 1
			degrees[i] += 1
			#print math.floor(prevNode.id), "->", i
			ang = 2*math.pi*random()
			r = uniform(0, radiusRange**2)
			r = math.sqrt(r)
			X=prevNode.position[0] + r*math.cos(ang)
			Y=prevNode.position[1] + r*math.sin(ang)
			pos = [X,Y,0]
			self.addDevice(i, pos)
		#print degrees

	def allRandomWithReplacement(self, radiusRange):
		self.allRandom()
		self.replacement(radiusRange)

	def replacement(self,radiusRange):
		for source in range(self.numNodes):
			minDist = self.getMinDist(source)
			while minDist > radiusRange:
				#print "replaced"
				pos = [uniform(0,self.xSize), uniform(0,self.ySize),0]
				pos2 = [pos[0], pos[1], self.pairDist]
				self.devices[2*source].position = pos
				self.devices[(2*source)+1].position = pos2
				minDist = self.getMinDist(source)
				

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

	def save(self, file):
		with open(file, 'w') as f:
			for dev in self.devices:
				line = "dev,{},{},{},{}\n".format(dev.id,dev.position[0], dev.position[1], dev.position[2])
				f.write(line)
			for link in self.links:
				line = "link,{},{},{}\n".format(link.id, link.devices[0].id, link.devices[1].id)
				f.write(line)

	def saveDevices(self, file):
		with open(file, 'w') as f:
			for dev in self.devices:
				line = "{},{},{},{}\n".format(dev.id,dev.position[0], dev.position[1], dev.position[2])
				f.write(line)

	def load(self,file):
		with open(file, 'r') as f:
			csvFile = csv.reader(f, delimiter=',')
			for row in csvFile:
				#print row
				if row[0]=='dev':
					devID=float(row[1])
					pos=[float(row[2]),float(row[3]),float(row[4])]
					devc = Device(devID, pos, Queue())
					self.devices.append(devc)
				elif row[0]=='link':
					linkID=float(row[1])
					dev1ID=float(row[2])
					dev2ID=float(row[3])
					for device in self.devices:
						if device.id == dev1ID:
							device1 = device
						if device.id == dev2ID:
							device2 = device
					link = Link(linkID, device1, device2)
					device1.addLink(link)
					device2.addLink(link)
					self.links.append(link)

				else:
					print "ERROR loading file"
			self.numNodes = len(self.devices)/2


	def distance(self, deviceA, deviceB):
		if self.useToroidalSpace:
			sqSum=min(abs(deviceA.position[0]-deviceB.position[0]), self.sizeX - abs(deviceA.position[0]-deviceB.position[0]))**2 + min(abs(deviceA.position[1]-deviceB.position[1]), self.sizeY - abs(deviceA.position[1]-deviceB.position[1]))**2+(deviceA.position[2]-deviceB.position[2])**2
		else:
			sqSum = (deviceA.position[0]-deviceB.position[0])**2+(deviceA.position[1]-deviceB.position[1])**2+(deviceA.position[2]-deviceB.position[2])**2
		dist = sqSum**0.5
		return dist

	def getMinDist(self, source):
		sourceDev = self.devices[2*source]
		minDist = deviceDistance(sourceDev,self.devices[2*(source-1)])
		for target in range(self.numNodes):
			if source == target:
				continue
			dist = deviceDistance(sourceDev,self.devices[2*target])
			minDist = dist if dist < minDist else minDist
		return minDist




if __name__ == "__main__":
	for i in range(40):
		rt = RandomTopology(16,40,70*4,70*4)
		rt.allRandomWithReplacement(80)
		rt.save("./randomGraphs/savedGraphs/DevGraph16AllRandWR"+str(i)+".csv")
		rt.saveDevices("./randomGraphs/savedDevPoints/DevGraph16AllRandWRDevs"+str(i)+".csv")

	for i in range(40):
		rt = RandomTopology(16,40,70*4,70*4)
		rt.nearPrevNode(80)
		rt.save("./randomGraphs/savedGraphs/DevGraph16NPV"+str(i)+".csv")
		rt.saveDevices("./randomGraphs/savedDevPoints/DevGraph16NPVDevs"+str(i)+".csv")

	for i in range(40):
		rt = RandomTopology(16,40,70*4,70*4)
		rt.nearPrevNode(80, True, 4)
		rt.save("./randomGraphs/savedGraphs/DevGraph16NPV_MD3_"+str(i)+".csv")
		rt.saveDevices("./randomGraphs/savedDevPoints/DevGraph16NPV_MD3_Devs"+str(i)+".csv")		