# -*- coding: utf-8 -*-
from random import *


def calc_L(targetMean):
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
	return L

def getNewValue(L,rho):
	H=1000
	U=random()
	g=1.5
	x=(-(U*(H**g)-U*(L**g)-H**g)/(H*L)**g)**(-1/g)
	#x = 1/((1-random()*(1-(L/H)**g))/L**g)**(1/g)
	#mean=((L**g)/(1-(L/H)**g))*(g/(g-1))*((1/(L**(g-1)))-(1/H**(g-1)))
	#print mean
	return rho*x


summ=0
size = 10
#0.5
for i in range(size):
 summ+= getNewValue(calc_L(0.5),1)
print summ/size

summ=0
#0.5
for i in range(size):
 summ+= getNewValue(calc_L(0.1),1)
print summ/size

summ=0
#0.5
for i in range(size):
 summ+= getNewValue(calc_L(0.5),1./5.)
print summ/size

v1=[0, 0, 0, 0, 7762, 0, 567732, 175043, 249463, 0, 0, 0, 0, 0, 0, 0]
v2=[0, 0, 0, 0, 6241, 0, 565826, 197558, 230375, 0, 0, 0, 0, 0, 0, 0]
v12=[0, 0, 0, 0, 0, 0, 191774, 90519, 717707, 0, 0, 0, 0, 0, 0, 0]
v22=[0, 0, 0, 0, 0, 0, 180308, 99939, 719753, 0, 0, 0, 0, 0, 0, 0]
algos = [v1, v2, v12, v22]
print"===Reutilizacao espacial==="
for algo in algos:
	reutilSum = 0.
	maxNodesSChed = 0.
	for i in range(len(algo)):
		if algo[i] > 0: maxNodesSChed = i
		reutilSum+= algo[i]*i
	reutil = reutilSum/(sum(algo)*maxNodesSChed)
	print reutil


t1=[0, 2204, 351828, 511818, 113125, 19018, 1836, 164, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
t2=[0, 63578, 916657, 19759, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
t12=[0, 2240, 351437, 511627, 113828, 18936, 1769, 149, 13, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
t22=[0, 63573, 916720, 19704, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
v2 = [0, 34545, 897215, 68198, 42, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
v1 = [0, 2020, 309910, 516468, 139195, 29348, 2707, 347, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
algos=[v1,v2]
print "===Tempo de convergencia==="
for j in range(len(algos)):
	summ=0.
	for i in range(len(algos[j])):
		if j > 1:
			summ+=algos[j][i]*(i+3)
		else:
			summ+=algos[j][i]*(i)
	meanTime = summ/sum(algo)
	print meanTime


#toroidal
#v2 [0, 0, 0, 0, 164789, 387583, 0, 0, 447628, 0, 0, 0, 0, 0, 0, 0]
#v1 [0, 0, 0, 0, 166477, 388432, 0, 0, 445091, 0, 0, 0, 0, 0, 0, 0]
#v2 = [0, 34545, 897215, 68198, 42, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#v1 = [0, 2020, 309910, 516468, 139195, 29348, 2707, 347, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#nao toroidal
#v2
#[0, 34762, 896323, 68876, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#[0, 0, 0, 0, 165473, 387622, 0, 0, 446905, 0, 0, 0, 0, 0, 0, 0]
#v1
#[0, 1994, 311296, 515471, 138657, 29601, 2583, 392, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#[0, 0, 0, 0, 165766, 388364, 0, 0, 445870, 0, 0, 0, 0, 0, 0, 0]
