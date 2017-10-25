import subprocess
from interference_graph import *
from device_graph import *
import numpy as np
import sympy as sp


interfDistance = 80.

randNetGraphPath = "./randomGraphs/savedGraphs/"
randInterGraphPath = "./randomGraphs/savedInterfGraphs/"
saveResultsFilePath = "../resultados/"
feasibleSchedPath = "../resultados/feasible scheds/"
maximalSchedPath = "./randomGraphs/maximalScheds/"
fileNames = ["DevGraph16AllRandWR", "DevGraph16NPV","DevGraph16NPV_MD3_"]
print "Starting"


for name in fileNames:
  for nameIdx in range(40):

    
    saveInterGraphPath = randInterGraphPath+name+str(nameIdx)+".interfgraph"
    if False: #already saved
      rt = RandomTopology()
      rt.load(randNetGraphPath+name+str(nameIdx)+".csv")
      interfGraph = InterferenceGraph(rt, interfDistance, False)
      interfGraph.save(saveInterGraphPath)

    saveFeasibleSchedPath = feasibleSchedPath+"feasibleSched_"+name+str(nameIdx)+".fsched"
    if False: #done
      subprocess.call(['../enumerator iecker/main', saveInterGraphPath, saveFeasibleSchedPath])

    
    fsched = []
    i = 0
    with open(saveFeasibleSchedPath) as feasibleSchedsFile:
      for line in feasibleSchedsFile:
        i += 1
        line = set(map(int,line.split()))
        fsched.append(line)
        #if i == 20:
          #break
      #print fsched

    maximalScheds = []
    for outterSched in range(len(fsched)):
      isMaximal = True
      for innerSched in range(outterSched+1, len(fsched)):
        if fsched[outterSched].issubset(fsched[innerSched]):
          isMaximal = False
          break
      if isMaximal:
        maximalScheds.append(fsched[outterSched])
    maximalScheds = map(list,maximalScheds)
    #print len(maximalScheds), saveFeasibleSchedPath
    listoflist = []

    for sched in maximalScheds:
      sched = sorted(sched)
      aux = [0]*16
      for pos in sched:
        aux[pos]=1
      listoflist.append(aux)

    p0 = listoflist[0]
    listoflist = listoflist[1:]
    ums = [1]*16

    for p in listoflist:
      for i in range(len(p)):
        p[i] -= p0[i]
    #listoflist.append(ums)
    if True:
      matrix = np.array([np.array(vec) for vec in listoflist])
      rank = np.linalg.matrix_rank(matrix)
      spVecMatrix = sp.Matrix(listoflist)
      nullSpace = spVecMatrix.nullspace()

    
    if True: #rank == 16:

      if rank > 15: 
        print "======== WTFFF RANK ========"
        print len(maximalScheds), saveFeasibleSchedPath
        print rank
      if False:
        allZero = True
        for val in nullSpace[0]:
          if val != 0:
            allZero = False
        if allZero:
          print "======== WTFFF ========"
          print nullSpace[0]
      #print nullSpace
      #print spVecMatrix*nullSpace[0]
    
    #print matrix[lambdas == 0,:]
    if False:
      with open(maximalSchedPath+"MaximalScheds_"+name+str(nameIdx)+".csv",'w') as resultsSaveFile:
        for l in maximalScheds:
          resultsSaveFile.write(str(l)+'\n')




    #print map(list,maximalScheds)

        #print fsched[outterSched], fsched[innerSched]

print "Finished"