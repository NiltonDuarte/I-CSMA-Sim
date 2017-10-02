import hashlib
from math import *


#[[4, 7, 1, 6, 2, 0, 5, 3], [1, 6, 3, 4, 7, 2, 5, 0], [2, 6, 3, 0, 1, 7, 5, 4]]
#int(hashlib.sha1('83').hexdigest(),16)%3


class HashOrdering():
	def __init__(self,size):
		self.size = size
		self.permGroup = [[1,2,3,4,5,6,7,0],[6,7,0,1,2,3,4,5],[7,6,5,4,0,1,2,3],[1,0,3,2,5,4,7,6]]
		self.counter = 0
		self.order = [i for i in range(size)]
		self.createPermGroup()

	def getOrder(self):
		idx = int(hashlib.sha1(str(self.counter)).hexdigest(),16)%4
		self.counter += 1
		perm = self.permGroup[idx]
		newOrder = [0]*self.size
		for i in range(self.size):
			aux = self.order[perm[i]]
			newOrder[i]= aux
		self.order = newOrder
		return newOrder

	def createPermGroup(self):
		g0 = self.order[1:]+self.order[:1]
		print g0
		self.permGroup[0] = g0
		back2 = self.size-2
		g1 = self.order[back2:]+self.order[:back2]
		print g1
		self.permGroup[1] = g1
		turn = int(floor(self.size/2.))-1
		g2 = self.order[:turn:-1]+self.order[:turn+1]
		print g2
		self.permGroup[2] = g2
		slice1 = self.order[::2]
		slice2 = self.order[1::2]
		listoflist = map(list,zip(slice2,slice1))
		g3 =sum(listoflist,[])
		if len(slice1) != len(slice2):
			if len(slice1) > len(slice2):
				g3.append( slice1[-1] )
			else:
				g3.append( slice2[-1] )
		
		print g3
		self.permGroup[3] = g3




if __name__ == "__main__":
	size = 9
	ho = HashOrdering(size)
	
	hist = [[0 for x in range(size)] for y in range(size)] 
	histOrder = {}
	count = 0
	for i in range(100000000):
		order = ho.getOrder()
		num = 0
		for j in range(len(order)):
			num += order[j]*(10**j)
			hist[order[j]][j]+=1
		key = str(num)
		if key in histOrder:
			histOrder[key] += 1
		else:
			histOrder[key] = 1
			count += 1
	for row in hist:
		print row, sum(row)
	
	print count
	print len(histOrder)
	print ho.permGroup


