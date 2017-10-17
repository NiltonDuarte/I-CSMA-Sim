from math import *
from interference_graph import *
from device_graph import *
from random import *
from network_structure import *
import sys

WINNER = 1
IDLE = 0
LOSER = 2

class Schedule_Algorithm:
  def __init__(self, id, slot):
    self.number = 0
    self.state = IDLE
    self.neighbours = []
    self.id = id
    self.slot = slot
    self.round = 0
    self.scheduled = False

  def genNumber(self, min, max):
    self.number=randint(min,max)
    return self

  def genNumberSA(self,min, dc, max):
    self.round += 1
    self.state = IDLE
    if self.scheduled:
      self.number=randint(min,dc)
    else:
      self.number=randint(dc,max)
    return self

  def updateState(self):
    win = True
    if self.state != IDLE:
      return
    for nbour in self.neighbours:
      if nbour.state == WINNER:
        self.state = LOSER
        self.number = -1
        return self
      #elif nbour.state == LOSER:
      #   self.neighbours.remove(nbour)
      elif self.number < nbour.number:
        win=False
      elif self.number == nbour.number and self.id < nbour.id:
        win=False

    if win:
      self.state=WINNER
      self.scheduled = True
    return self

  def updateState2(self):
    higher = 0
    if self.state != IDLE:
      return
    for nbour in self.neighbours:
      if nbour.state == WINNER:
        self.state = LOSER
        self.number = -1
        return self
      #elif nbour.state == LOSER:
      #   self.neighbours.remove(nbour)
      elif self.number < nbour.number:
        higher+=1
      elif self.number == nbour.number and self.id < nbour.id:
        higher+=1

    if higher <= 1:
      self.state=WINNER
      self.scheduled=True
    return self

  def updateState4(self, dc):
    if self.state != IDLE:
      return
    nboursNumbers = []
    for nbour in self.neighbours:
      if nbour.state == WINNER:
        self.state = LOSER
        self.number = -1
        return self
      if self.number == nbour.number and self.id < nbour.id:
        nboursNumbers.append(nbour.number-1)
      elif self.number == nbour.number and self.id > nbour.id:
        nboursNumbers.append(nbour.number+1)
      else:
        nboursNumbers.append(nbour.number)
    if self.number>dc:
      higher_numbers = filter(lambda x: x> self.number, nboursNumbers)
      #print "n>dc higher", self.id, higher_numbers
      if len(higher_numbers) <= 1:
        self.state=WINNER
        self.scheduled = True
    else:
      dcIn_numbers = filter(lambda x: x> dc, nboursNumbers)
      #print "n<dc dcin ", self.id, dcIn_numbers
      if len(dcIn_numbers) >  0:
        return self
      higher_numbers = filter(lambda x: x> self.number, nboursNumbers)
      #print "n<dc higher ", self.id, higher_numbers
      if len(higher_numbers) <= 1:
        self.state=WINNER
        self.scheduled = True
    return self

#>>> perm
#[[4, 7, 1, 6, 2, 0, 5, 3], [1, 6, 3, 4, 7, 2, 5, 0], [2, 6, 3, 0, 1, 7, 5, 4]]     
#int(hashlib.sha1('83').hexdigest(),16)%3

if __name__ == "__main__":
  
  LattInterfDist = 80.
  LattDistance = 70.
  LattSize = 4
  LattPairDist = 40.
  maxSteps = 0
  numIt = 60000
  dc = 50000
  dmax=100000
  dmin= 0
  #lattice = Lattice(LattSize,LattDistance,LattPairDist)
  #interfGraphLattice = InterferenceGraph(lattice, LattInterfDist, True, LattDistance*(LattSize), LattDistance*(LattSize))
  n = 16
  totalCountFreq=[0]*n
  filePath = "./randomGraphs/savedGraphs/"
  saveFilePath = "../resultados/"
  fileNames = ["DevGraph16AllRandWR", "DevGraph16NPV","DevGraph16NPV_MD3_"]

  print "Starting"
  minSchedFile = open(saveFilePath+"Results_MinScheds.csv",'w')
  for name in fileNames:
    resultsSaveFile = open(saveFilePath+"Results_"+name+sys.argv[1]+".csv",'w')
    for nameIdx in range(40):
      stepsFreq=[0]*25
      countFreq=[0]*n
      notSched = [k for k in range(n)]
      sched = []
      allSchedFreq = []
      bestScheds = [0]*(n+1)
      currntScheds = []
      for i in range(numIt):
        sched.sort()
        if len(sched) > 0:
          currntScheds.append(sched)
        for s in sched:
          if s in notSched:
            notSched.remove(s)
        #print "still left ", notSched

        sched = []
        if len(notSched) == 0:
          notSched = [k for k in range(n)]
          allSchedFreq.append(i)
          if len(currntScheds) < len(bestScheds):
            print "new best sched", currntScheds
            bestScheds = currntScheds[:]
            currntScheds = []
        rt = RandomTopology()
        rt.load(filePath+name+str(nameIdx)+".csv")
        interfGraphLattice = InterferenceGraph(rt, LattInterfDist, False)
        interfGraphLattice.nodes.sort(key=lambda node: node.id)
        
        for node in interfGraphLattice.nodes:
          node.sched_algo=Schedule_Algorithm(node.id,0)
          if sys.argv[1] == 'v4':
            prio = notSched
            if node.id in prio:
              node.sched_algo.genNumber(dc,dmax)
            else:
              node.sched_algo.genNumber(dmin,dc)
          else:
            node.sched_algo.genNumber(0,10000)

        for node in interfGraphLattice.nodes:
          node.sched_algo.neighbours=[obj.sched_algo for obj in interfGraphLattice.getNeighbours(node)]


        #print [node.sched_algo.number for node in interfGraphLattice.nodes]

        completed = False
        
        steps = 0
        count = 0
        while not completed:
          steps+=1
          shuffle(interfGraphLattice.nodes)
          for node in interfGraphLattice.nodes:
            if sys.argv[1] == 'v1':
              node.sched_algo.updateState()
            if sys.argv[1] == 'v2' or sys.argv[1] == 'v3':
              node.sched_algo.updateState2()
            if sys.argv[1] == 'v4':
              node.sched_algo.updateState4(dc)
            
          completed=True
          for node in interfGraphLattice.nodes:
            if node.sched_algo.state == IDLE:
              completed = False
          if steps>10: 
            print '=SCHED='
            for node in interfGraphLattice.nodes:
              print node.sched_algo.state,
              print node.sched_algo.number,
              if node.id%LattSize==(LattSize-1):
                print

        for node in interfGraphLattice.nodes:
          if node.sched_algo.state == WINNER:
            for neigh in node.sched_algo.neighbours:
              if neigh.state == WINNER:
                print "ERROR 2,1".i , node.id, neigh.id                     
        #v3
        if sys.argv[1] == 'v3': 
          for node in interfGraphLattice.nodes:
            if node.sched_algo.state==WINNER:
              neighboursCandidateList=[]
              for neigh in node.sched_algo.neighbours:
                nneighsOns=0
                for nneigh in neigh.neighbours:
                  if nneigh.state==WINNER:
                    nneighsOns +=1
                if nneighsOns == 0:
                  print "Error 1"
                if nneighsOns == 1:
                  neighboursCandidateList.append(neigh)
              if len(neighboursCandidateList)>1: 
                #print "search ",node.id, [obj.id for obj in neighboursCandidateList]
                node.sched_algo.state=LOSER
                for nodeschedalgo in neighboursCandidateList:
                  allnneighOFF = True
                  for nneigh in nodeschedalgo.neighbours:
                    if nneigh.state==WINNER:
                      allnneighOFF = False
                  if allnneighOFF:
                    nodeschedalgo.state=WINNER


        for node in interfGraphLattice.nodes:
          if node.sched_algo.state == WINNER:
            for neigh in node.sched_algo.neighbours:
              if neigh.state == WINNER:
                print "ERROR 2",i, node.id, neigh.id
            count += 1
            sched.append(node.id)
        if count > n/2:
          print '=SCHED2='
          print steps
          print [node.id for node in sched]

          for node in interfGraphLattice.nodes:
            print node.sched_algo.number,
            #if node.id%LattSize==(LattSize-1):
          print
        #print "==SCHED=="
        #for node in interfGraphLattice.nodes:
        #   print node.sched_algo.state,
        #   if node.id%4==3:
        #       print                   
          #print [node.sched_algo.state for node in interfGraphLattice.nodes]
          #print [node.sched_algo.number for node in interfGraphLattice.nodes]
          #i=0
          #for node in interfGraphLattice.nodes:
          #   print node.sched_algo.state,
          #   i+=1
          #   if i%4==0: print
          #print "======================"
        if i%10000==0:
          print i
          print name, nameIdx
          print stepsFreq
          print countFreq
        stepsFreq[steps]+=1
        countFreq[count]+=1
        totalCountFreq[count]+=1
      print stepsFreq
      print countFreq
      mean = 0.
      for aux in range(len(countFreq)):
        mean += aux*countFreq[aux]
      mean = mean/float(numIt)
      resultsSaveFile.write(sys.argv[1]+","+str(nameIdx)+","+str(mean)+"\n")
      resultsSaveFile.flush()
      minSchedFile.write(name+str(nameIdx)+", "+str(bestScheds)+"\n")
      minSchedFile.flush()
    resultsSaveFile.close()
  mean = 0.


if __name__ == "false__main__":
  LattInterfDist = 80.
  LattDistance = 70.
  LattSize = 4
  LattPairDist = 40.
  maxSteps = 0
  numIt = 10000   
  dc = 50000
  dmax=100000
  dmin= 0
  lattice = Lattice(LattSize,LattDistance,LattPairDist)
  interfGraphLattice = InterferenceGraph(lattice, LattInterfDist, True, LattDistance*(LattSize), LattDistance*(LattSize))
  n = 16
  totalCountFreq=[0]*n
  print "Starting"
  #resultsSaveFile = open("Results_"+name+sys.argv[1]+".csv",'w')
  stepsFreq=[0]*25
  countFreq=[0]*n
  notSched = []
  sched = []
  allSchedFreq = []
  for i in range(numIt):
    for s in sched:
      if s in notSched:
        notSched.remove(s)
    #print "still left ", notSched
    sched = []
    if len(notSched) == 0:
      notSched = [k for k in range(n)]
      #print "all sched'ed ", i
      allSchedFreq.append(i)
    lattice = Lattice(LattSize,LattDistance,LattPairDist)
    interfGraphLattice = InterferenceGraph(lattice, LattInterfDist, False, LattDistance*(LattSize), LattDistance*(LattSize))
    interfGraphLattice.nodes.sort(key=lambda node: node.id)
    
    for node in interfGraphLattice.nodes:
      node.sched_algo=Schedule_Algorithm(node.id,0)
      #prio = [0,2,5,7,8,10,13,15]
      prio = notSched
      if node.id in prio:
        node.sched_algo.genNumber(dc,dmax)
      else:
        node.sched_algo.genNumber(dmin,dc)

    for node in interfGraphLattice.nodes:
      node.sched_algo.neighbours=[obj.sched_algo for obj in interfGraphLattice.getNeighbours(node)]
    
    """
    print [node.id for node in interfGraphLattice.nodes]
    print [node.sched_algo.state for node in interfGraphLattice.nodes]
    print [node.sched_algo.number for node in interfGraphLattice.nodes]
    """
    completed = False
        
    steps = 0
    count = 0
    while not completed:
      steps+=1
      shuffle(interfGraphLattice.nodes)
      for node in interfGraphLattice.nodes:
        if sys.argv[1] == 'v1':
          node.sched_algo.updateState()
        if sys.argv[1] == 'v2' or sys.argv[1] == 'v3':
          node.sched_algo.updateState2()
        if sys.argv[1] == 'v4':
          node.sched_algo.updateState4(dc)
        
      completed=True
      for node in interfGraphLattice.nodes:
        if node.sched_algo.state == IDLE:
          completed = False
      if steps>10: 
        print '=SCHED='
        for node in interfGraphLattice.nodes:
          print node.sched_algo.state,
          print node.sched_algo.number,
          if node.id%LattSize==(LattSize-1):
            print
    interfGraphLattice.nodes.sort(key=lambda node: node.id)
    for node in interfGraphLattice.nodes:
      if node.sched_algo.state == WINNER:
        for neigh in node.sched_algo.neighbours:
          if neigh.state == WINNER:
            print "ERROR 1 invalid schedule.  asrkt",i, node.id, neigh.id
        count += 1
        sched.append(node.id)
    """ 
    print [node.sched_algo.state for node in interfGraphLattice.nodes]
    print [node.sched_algo.number for node in interfGraphLattice.nodes]
    
    i=0
    for node in interfGraphLattice.nodes:
      print node.sched_algo.state,
      i+=1
      if i%4==0: print
    print [nID for nID in sched]
    print "======================"
    """
    if i%10000==0:
      print i
      print stepsFreq
      print countFreq
    stepsFreq[steps]+=1
    countFreq[count]+=1
    totalCountFreq[count]+=1
    #a = raw_input("press p/ continuar")
  print "steps freq ",stepsFreq
  print "count freq ",countFreq
  mean = 0.
  for h in range(len(countFreq)):
    mean+=countFreq[h]*h
  print "count mean ", mean/numIt
  #print allSchedFreq
  allSchedHisto = [0]*100
  for v in range(len(allSchedFreq))[1:]:
    time = allSchedFreq[v]-allSchedFreq[v-1]
    allSchedHisto[time]+=1
  
  print "all sched mean ",float(allSchedFreq[-1])/(len(allSchedFreq)-1)
  print "all sched histo ",allSchedHisto

