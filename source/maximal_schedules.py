import subprocess
from interference_graph import *
from device_graph import *


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
    if True: #already saved
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
    with open(maximalSchedPath+"MaximalScheds_"+name+str(nameIdx)+".csv",'w') as resultsSaveFile:
      for l in maximalScheds:
        resultsSaveFile.write(str(l)+'\n')




    #print map(list,maximalScheds)

        #print fsched[outterSched], fsched[innerSched]