# -*- coding: utf-8 -*-

#directed interference hypergraph#directed interference hypergraph

def createSets(list):
	list.sort()
	sets = []
	workingSet =[]
	for i in list:
		workingSetAux = workingSet[:]
		for subset in workingSetAux:
			workingSet.append(subset+[i])
		workingSet.append([i])
		print workingSet
		print len(workingSet)
