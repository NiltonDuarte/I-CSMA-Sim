# -*- coding: utf-8 -*-

from interference_graph import *
from math import *
from random import *
from network_structure import *
from schedule_algorithm import *

class MultipleAccessAlgorithm:
  def __init__(self, interferenceGraph, beta, totalMiniSlots, rho, trafficMean, maxMeanQueue, safeCheck = False):
    self.b = beta
    self.g = 1 #gamma
    self.interfGraph = interferenceGraph
    self.numNodes = len(interferenceGraph.nodes)
    self.maxD = interferenceGraph.getMaxDegree()
    self.rho = rho
    self.it = None
    self.slot = 0
    #STORE VALUES
    self.maxMeanQueue = maxMeanQueue
    self.OFF = -1
    self.CP2W=8
    #CONTROL VARIABLES
    self.useHeuristic = False
    self.useCollisionFree = False
    self.newQueueFunc = False
    self.newSFunc = False
    self.newQProb = False
    self.newCP2 = False
    self.useQueueInfo = True
    self.safeCheck = safeCheck
    #====================
    #STATISTICS VARIABLES
    self.totalCollisionCount = 0
    self.slotCollisionCount = 0
    self.onNodesCount = 0
    self.slotCollisionFrequency = [0]*(self.numNodes+2)
    self.schedSizeFrequency = [0]*(self.numNodes+1) 
    self.onNodesFrequency = [0]*(self.numNodes+1)
    #====================
    
    for node in self.interfGraph.nodes:
      nodeTraffic = trafficMean[str(node.id)]
      #print node.id, nodeTraffic
      node.set_traffic(rho*nodeTraffic, totalMiniSlots) 


  def _run(self, iterations):
    self.it = 0
    while self.it < iterations:
      self.slotCollisionCount=0
      self.onNodesCount=0
      if self.queueLimit():
        return slotSchedule
      if self.useHeuristic or self.useCollisionFree:
        self.heuristicControlPhase1()
      else:
        self.controlPhase1()
      if self.useCollisionFree:
        slotSchedule = self._collisionFreePhase2()
        self.slot+=1
      else:
        slotSchedule = self.controlPhase2()
      self.totalCollisionCount+=self.slotCollisionCount
      if self.slotCollisionCount > self.numNodes:
        self.slotCollisionCount = self.numNodes+1  
      self.slotCollisionFrequency[int(self.slotCollisionCount)]+=1
      self.schedSizeFrequency[len(slotSchedule)]+=1   
      self.onNodesFrequency[self.onNodesCount]+=1
      
      self.it += 1
      if self.safeCheck:
        #slotSchedule.append(self.interfGraph.nodes[0])
        if not self.safetyCheck(slotSchedule):
          print "SAFETY CHECK ERROR", slotSchedule
          return "SAFETY CHECK ERROR"
    return slotSchedule

  def runCollisionFree(self, iterations, version, steps, maxSchedRounds=None):
    #tdma slot assignment max rounds (colors)
    self.maxSchedRounds = maxSchedRounds
    self.versionCollisionFree = version
    self.parallelSchedAlgos = steps
    self.useCollisionFree = True
    if self.slot == 0:
      self.initCtrlPhaseCF(steps)
    return self._run(iterations)
    
  def runICSMA(self, iterations, W1, W2):
    self.W1 = W1
    self.W2 = W2
    return self._run(iterations)

  def runHeuristicICSMA(self, iterations, W2):
    self.W2 = W2
    self.useHeuristic=True
    return self._run(iterations)   
    
  def _collisionFreePhase2(self):
    shuffle(self.interfGraph.nodes)
    if self.versionCollisionFree == 'v2':
      return self.collisionFreePhase2v2()
    if self.versionCollisionFree == 'v4':
      return self.collisionFreePhase2v4()

  #returns true if the current queue mean is greater than the queue limit
  def queueLimit(self):
    meanQ = reduce(lambda parcialSum,node: parcialSum+node.getQueueSize(),self.interfGraph.nodes,0)
    meanQ /= self.numNodes
    if self.maxMeanQueue and meanQ > self.maxMeanQueue:
      return True
    return False

  def turnOnFunctions(self, newQF, newSF, newQP, newCP2, useQueueInfo=True):
    self.newQueueFunc = newQF
    self.newSFunc = newSF
    self.newQProb = newQP
    self.newCP2 = newCP2
    self.useQueueInfo = useQueueInfo


  def safetyCheck(self, sched):
    for schedNode in sched:
      for neig in self.interfGraph.getNeighbours(schedNode):
        if neig in sched:
          print "ERROR impossible sched"
          return False
    return True

  def S(self, node):
    #sum of the node neighbours state(spins). desc after eq 5
    neighbours = self.interfGraph.getNeighbours(node)
    S = 0.0
    for neighbour in neighbours:
      S += neighbour.state
    #print node.id, S
    if self.newSFunc:
      return S/len(neighbours)
    return S

  def q(self, node):
    #eq 5
    Av=self.queueFunction(node.getQueueSize())
    S = self.S(node)
    try:
      if self.newQProb == "tanhdif":
        x = self.b*(Av-self.S(node))
        ret= 0.5*(1+tanh(x))
      elif self.newQProb == "sech":
        ret = 1-(1/cosh((Av+1)*self.b*self.S(node)/2))
      elif self.newQProb == "placeholder":
        expo = self.b*((self.g+S)-Av*(Av*self.g-S))
        ret = 1./(1.+exp(expo))
      else:
        ret = 0.5*(1-tanh((Av+1)*self.b*self.S(node)/2))
    except OverflowError as e:
      print "(Av+1)*self.b*self.S(node)/2 = ", (Av+1)*self.b*self.S(node)/2
    #print ret
    return ret

  def silenceNeighbours(self, node):
    #avoid bouncing
    if node.visited: return
    node.visited = True
    for neighbour in self.interfGraph.getNeighbours(node):
      #collision
      if neighbour.setSilenced(True).backoff == node.backoff:
        self.slotCollisionCount+=0.5
        node.setSilenced(True)
        self.silenceNeighbours(neighbour)

  #Av
  def queueFunction(self, queue):
    if self.newQueueFunc:
      return log(queue+1)
    return 2*(self.maxD-1)+log(queue+1)

  def updateState(self, node):
    if random() < node.get_q():
      Av = self.queueFunction(node.getQueueSize())
      node.setState(Av)
      #print node.id, Av
    else:
      node.setState(self.OFF)  
      
  def dumpNodesQueues(self, sched):
    map(lambda node: node.dumpQueue(), sched)  

  def fillNodesQueues(self):
    #fill queues
    map(lambda node: node.fillQueue(), self.interfGraph.nodes)

  def calculateNodes_q(self):
    map(lambda node: node.set_q(self.q(node)), self.interfGraph.nodes)

  def setsortNodesRandomBackoffs(self, maxVal):
    map(lambda node: node.setBackoff(randint(0,maxVal)), self.interfGraph.nodes)
    self.interfGraph.nodes.sort(key=lambda node: node.backoff)
    

  def resetNodesCtrlVars(self):
    map(lambda node: node.resetCtrlVars(), self.interfGraph.nodes)

  def controlPhase1(self):
    self.calculateNodes_q() #calc S and q based on prev time slot
    self.fillNodesQueues()
    self.resetNodesCtrlVars() #reset visited, silenced and collided control variable
    self.setsortNodesRandomBackoffs(self.W1) #set and sort random backoff

    #send INTENT
    for node in self.interfGraph.nodes:
      if not node.silenced:
        self.silenceNeighbours(node)
        #if ack collided, this node is silenced now
        if not node.silenced:
          self.updateState(node)

  def heuristicControlPhase1(self):
    self.calculateNodes_q()    #calc S and q based on prev time slot
    self.fillNodesQueues() 
    for node in self.interfGraph.nodes:
      self.updateState(node)

  def controlPhase2(self):
    self.resetNodesCtrlVars()  #reset visited, silenced and collided control variable
    self.setsortNodesRandomBackoffs(self.W2)  #set ans sort random backoff

    slotSchedule = []
    #send RESERVE
    for node in self.interfGraph.nodes:
      if node.state != self.OFF:
        self.onNodesCount+=1
        if not node.silenced:
          self.silenceNeighbours(node)
          #if ack collided, this node is silenced now
          if not node.silenced:
            slotSchedule.append(node)

    if self.newCP2:
      self.setsortNodesRandomBackoffs(self.newCP2)  #set and sort random backoff     
      for node in self.interfGraph.nodes:
        if (not node.silenced and node.state == self.OFF) or node.collided:
          self.silenceNeighbours(node)
          #if ack collided, this node is silenced now
          if not node.silenced:
            slotSchedule.append(node)
    #dump schedules queues
    self.dumpNodesQueues(slotSchedule)
    return slotSchedule

  def initCtrlPhaseCF(self, steps):  
    for i in range(steps):
      for node in self.interfGraph.nodes:
        algo = Schedule_Algorithm(node.id, self.slot)
        algo.genNumber(0,4000)
        node.sched_algo.append(algo)
      for node in self.interfGraph.nodes:
        node.sched_algo[-1].neighbours = [obj.sched_algo[-1] for obj in self.interfGraph.getNeighbours(node)]
      self.slot += 1

  def collisionFreePhase2v2(self):
    min = 0
    dc = 4000
    max = 10000
    slotSchedule = []
    #print "====================="
    for node in self.interfGraph.nodes:
      #print node.sched_algo[0].number
      schedState = node.sched_algo.pop(0).state
      #print self.slot, node.id, schedState
      for obj in self.interfGraph.getNeighbours(node):
        error = True
        for algo in obj.sched_algo[-2:]:
          if algo.slot == node.sched_algo[-1].slot:
            error = False
            node.sched_algo[-1].neighbours.append(algo)
        if error: print "ERROR"

      for algo in node.sched_algo:
        algo.updateState2()

      newAlgo = Schedule_Algorithm(node.id, self.slot)
      if node.state == self.OFF and self.useQueueInfo:
        newAlgo.genNumber(min, dc)
      else:
        newAlgo.genNumber(dc, max)
      node.sched_algo.append(newAlgo)

      if schedState == 1:
        slotSchedule.append(node)
    self.dumpNodesQueues(slotSchedule)
    #print [node.id for node in slotSchedule]
    return slotSchedule

  def collisionFreePhase2v4(self):
    min = 0
    dc = 10000
    max = 20000
    slotSchedule = []
    algoIdx = self.it % self.parallelSchedAlgos
    startingNewAlgo = False
    #print "====================="
    for node in self.interfGraph.nodes:
      
      nodeAlgo = node.sched_algo[algoIdx]
      #print nodeAlgo.number
      schedState = nodeAlgo.state
      if schedState == 1:
        slotSchedule.append(node)
      for algo in node.sched_algo:
        algo.updateState4(dc)

      if nodeAlgo.round == self.maxSchedRounds:
        startingNewAlgo = True
        newAlgo = Schedule_Algorithm(node.id, self.slot)
        if node.state == self.OFF and self.useQueueInfo:
          newAlgo.scheduled=True
        newAlgo.genNumberSA(min,dc, max)
        node.sched_algo[algoIdx]=newAlgo
      else:
        nodeAlgo.genNumberSA(min,dc,max)
      #print self.slot, node.id, schedState

    if startingNewAlgo:
      for node in self.interfGraph.nodes:  
        for neig in self.interfGraph.getNeighbours(node):
          error = True
          neigAlgo = neig.sched_algo[algoIdx]
          nodeAlgo = node.sched_algo[algoIdx]
          if neigAlgo.slot == nodeAlgo.slot:
            error = False
            nodeAlgo.neighbours.append(neigAlgo)
          if error: print "ERROR 1"

    self.dumpNodesQueues(slotSchedule)
    #print [node.id for node in slotSchedule]
    return slotSchedule

if __name__ == '__main__':
  from device_graph import *
  from interference_graph import *
  LattDistance = 70.
  LattSize = 4
  LattPairDist = 40.

  windowP1 = 20
  windowP2 = 8
  heuristicWindowP2 = 28
  graphFilePath = "./randomGraphs/savedGraphs/"
  maxSchedPath = "./randomGraphs/maximalScheds/"
  maxSchedFileName = "MaximalScheds_"
  fileNames = ["DevGraph16AllRandWR", "DevGraph16NPV","DevGraph16NPV_MD3_"]
  name = fileNames[2]
  nameIdx=22
  #rho = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
  r = 0.5#map(float, sys.argv[2:])
  #arrivalMean = {'0':0.10, '1':0.1, '2':0.2,  '3':0.3,  '4':0.4,  '5':0.5,  '6':0.06,  '7':0.07,
  #         '8':0.08, '9':0.09, '10':0.10, '11':0.11, '12':0.12, '13':0.13, '14':0.14, '15':0.15}
  arrivalMean = {'0':0.50, '1':0.5, '2':0.5,  '3':0.5,  '4':0.5,  '5':0.5,  '6':0.5,  '7':0.5,
           '8':0.5, '9':0.5, '10':0.50, '11':0.5, '12':0.5, '13':0.5, '14':0.5, '15':0.5}
  beta = 1#float(sys.argv[1])
  testesIt = 1000
  LattInterfDist = 80.
  getArrivalVectorDict(maxSchedPath+maxSchedFileName+name+str(nameIdx)+".csv")
  print "Initializing"
  for beta in [0.1, 0.03, 1]:
    
    for r in [0.4, 0.5, 0.7]:
      for i in [2]:
        
        lattice = Lattice(LattSize,LattDistance,LattPairDist)
        interfGraphLattice = InterferenceGraph(lattice, LattInterfDist, False)
        
        #turnOnFunctions(self, newQF, newSF, newQP, newCP2):
        #runCollisionFree(self, iterations, version, steps, maxSchedRounds=None):
        if i == 0:
          #beta = 0.01
          maa = MultipleAccessAlgorithm(interfGraphLattice, beta, 252+28,r, arrivalMean, False, True) 
          maa.turnOnFunctions(False,False,False,False)
          schedule = maa.runICSMA(testesIt, windowP1, windowP2) 

          #schedule = maa.runHeuristicCSMA(testesIt, heuristicWindowP2) 
        elif i == 1:
          beta = 1
          maa = MultipleAccessAlgorithm(interfGraphLattice, beta, 252+28,r, arrivalMean, True)
          maa.turnOnFunctions(False,False,'sech',False)
          schedule = maa.runHeuristicICSMA(testesIt, heuristicWindowP2) 
        elif i == 2:
          beta = 1
          maa = MultipleAccessAlgorithm(interfGraphLattice, beta, 252+16,r, arrivalMean, True)      
          maa.turnOnFunctions(True,True,'sech',False,True)
          schedule = maa.runCollisionFree(testesIt, 'v2', 4, 4)
        elif i == 3:
          beta = 1
          maa = MultipleAccessAlgorithm(interfGraphLattice, beta, 252+16,r, arrivalMean, True)      
          maa.turnOnFunctions(False,True,'sech',False, False)
          schedule = maa.runCollisionFree(testesIt, 'v4', 4, 4)
        

        n=16.
        queue=0
        queuesList = []
        maa.interfGraph.nodes.sort(key=lambda node: node.id)
        for node in maa.interfGraph.nodes:
          queuesList.append(node.queueSize)
          queue += node.queueSize
        results=", ".join(str(x) for x in ([r , beta, maa.it, round(queue/n,2)] + queuesList + maa.schedSizeFrequency))
        print i, results