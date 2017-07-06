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
size = 100000
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