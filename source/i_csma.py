# -*- coding: utf-8 -*-

from interference_graph import *
from math import *
from random import *
from network_structure import *

class I_CSMA:
  def __init__(self, interferenceGraph, beta, W1, W2, totalMiniSlots, rho, trafficMean, interferenceSINRGraph=None):
    self.b = beta
    self.interfGraph = interferenceGraph
    self.W1 = W1
    self.W2 = W2
    self.maxD = interferenceGraph.getMaxDegree()
    self.rho = rho
    #self.traffic = TrafficDistribution(totalMiniSlots)
    #self.traffic.calc_L(rho*trafficMean)
    self.interfSINRGraph = interferenceSINRGraph
    self.useSINR = False
    self.schedSizeFrequency = [0]*(len(interferenceGraph.nodes)+1)
    self.numNodes = len(interferenceGraph.nodes)
    self.maxMeanQueue = 600
    self.it = None
    for node in self.interfGraph.nodes:
      nodeTraffic = trafficMean[str(node.id)]
      print node.id, nodeTraffic
      node.set_traffic(rho*nodeTraffic, totalMiniSlots)

  def _run(self, iterations):
    it = 0
    while it < iterations:
      if self.controlPhase1():
        slotSchedule = self.controlPhase2()
      else:
        self.it=it
        return slotSchedule
      self.schedSizeFrequency[len(slotSchedule)]+=1
      it += 1
    self.it=it
    return slotSchedule

  def run(self, iterations):
    self.useSINR=False
    return self._run(iterations)

  def runWithSINR(self, iterations):
    if self.interfSINRGraph == None:
      return False
    self.useSINR=True
    return self._run(iterations)

  def runHeuristic(self, iterations):
    it = 0
    while it < iterations:
      self.heuristicControlPhase1()
      schedule = self.controlPhase2()
      it += 1
    return schedule   

  def S(self, node):
    #sum of the node neighbours state(spins). desc after eq 5
    neighbours = self.interfGraph.getNeighbours(node)
    S = 0
    for neighbour in neighbours:
      S += neighbour.state
    #print node.id, S
    return S

  def q(self, node):
    #eq 5
    Av=self.queueFunction(node.getQueueSize())
    #ret = 0.5*(1-tanh((node.state+1)*self.b*self.S(node)/2))
    ret = 0.5*(1-tanh((Av+1)*self.b*self.S(node)/2))
    #print ret
    return ret

  def silenceNeighbours(self, node):
    #avoid bouncing
    if node.visited: return
    node.visited = True
    for neighbour in self.interfGraph.getNeighbours(node):
      #collision
      if neighbour.setSilenced(True).backoff == node.backoff:
        node.setSilenced(True)
        self.silenceNeighbours(neighbour)

  #Av
  def queueFunction(self, queue):
    return 2*(self.maxD-1)+log(queue+1)

  def updateState(self, node):
    if random() < node.get_q():
      Av = self.queueFunction(node.getQueueSize())
      node.setState(Av)
      #print node.id, Av
    else:
      node.setState(-1)
  def dumpQueue(self, sched):
    if self.useSINR:
      sched = self.interfSINRGraph.successfulTransmissions(sched)
    map(lambda node: node.dumpQueue(), sched)

  def controlPhase1(self):
    #check if the queues are too large and stop the algorithm
    meanQ = reduce(lambda parcialSum,node: parcialSum+node.getQueueSize(),self.interfGraph.nodes,0)
    meanQ /= self.numNodes
    if meanQ > self.maxMeanQueue:
      return False

    #calc S and q based on prev time slot
    #map(lambda node: node.setS(self.S(node)), self.interfGraph.nodes)
    map(lambda node: node.set_q(self.q(node)), self.interfGraph.nodes)
    #fill queues
    map(lambda node: node.fillQueue(), self.interfGraph.nodes)

    #reset visited control variable
    map(lambda node: node.resetVisit(), self.interfGraph.nodes)
    map(lambda node: node.resetSilence(), self.interfGraph.nodes)
    #set random backoff
    map(lambda node: node.setBackoff(randint(0,self.W1)), self.interfGraph.nodes)
    #sort
    self.interfGraph.nodes.sort(key=lambda node: node.backoff)
    #send INTENT
    for node in self.interfGraph.nodes:
      if not node.silenced:
        self.silenceNeighbours(node)
        #if ack collided, this node is silenced now
        if not node.silenced:
          self.updateState(node)
    #for node in self.interfGraph.nodes: print node.backoff, node.state

    return True

  def controlPhase2(self):
    #reset visited and silenced control variable
    map(lambda node: node.resetVisit(), self.interfGraph.nodes)
    map(lambda node: node.resetSilence(), self.interfGraph.nodes)
    #set random backoff
    map(lambda node: node.setBackoff(randint(0,self.W2)), self.interfGraph.nodes)
    #sort
    self.interfGraph.nodes.sort(key=lambda node: node.backoff)
    slotSchedule = []
    #send RESERVE
    for node in self.interfGraph.nodes:
      #if node.state != -1:
      # self.silenceNeighbours(node)
      if not node.silenced and node.state != -1:
        self.silenceNeighbours(node)
        #if ack collided or any neighbours reserved before, this node is silenced now
        if not node.silenced:
          slotSchedule.append(node)
    #dump schedules queues
    self.dumpQueue(slotSchedule)
    return slotSchedule

  def heuristicControlPhase1(self):
    #calc S and q based on prev time slot
    map(lambda node: node.set_q(self.q(node)), self.interfGraph.nodes)
    #fill queues
    map(lambda node: node.fillQueue(), self.interfGraph.nodes)
    for node in self.interfGraph.nodes:
      self.updateState(node)


if __name__ == '__main__':
  from device_graph import *
  from interference_graph import *
  LattDistance = 70.
  LattSize = 4
  LattPairDist = 40.

  windowP1 = 20
  windowP2 = 8
  #rho = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
  r = 0.9#map(float, sys.argv[2:])
  arrivalMean = {'0':0.10, '1':0.1, '2':0.2,  '3':0.3,  '4':0.4,  '5':0.5,  '6':0.06,  '7':0.07,
           '8':0.08, '9':0.09, '10':0.10, '11':0.11, '12':0.12, '13':0.13, '14':0.14, '15':0.15}
  beta = 0.01#float(sys.argv[1])
  testesIt = 10000

  LattInterfDist = 80.
  lattice = Lattice(LattSize,LattDistance,LattPairDist)
  interfGraphLattice = InterferenceGraph(lattice, LattInterfDist)
  xcsma = I_CSMA(interfGraphLattice, beta, windowP1, windowP2, 252+28,r, arrivalMean, None) 
  schedule = xcsma.run(testesIt)  
  n=16.
  queue=0
  queuesList = []
  xcsma.interfGraph.nodes.sort(key=lambda node: node.id)
  for node in xcsma.interfGraph.nodes:
    queuesList.append(node.queueSize)
    queue += node.queueSize
  results=", ".join(str(x) for x in ([r , beta, xcsma.it, round(queue/n,2)] + queuesList + xcsma.schedSizeFrequency))
  print results
