import subprocess
from interference_graph import *
from device_graph import *


interfDistance = 70.

randNetGraphPath = "./randomGraphs/savedGraphs/"
randInterGraphPath = "./randomGraphs/savedInterfGraphs/"
saveResultsFilePath = "../resultados/"
feasibleSchedPath = "../resultados/feasible scheds/"
maximalSchedPath = "./randomGraphs/maximalScheds/"
fileNames = ["DevGraph16AllRandWR", "DevGraph16NPV","DevGraph16NPV_MD3_"]
print "Starting"


for name in fileNames:
  for nameIdx in range(40):
    #resultsSaveFile = open(maximalSchedPath+"MaximalScheds_"+name+str(nameIdx)+".csv",'w')
    
    saveInterGraphPath = randInterGraphPath+name+str(nameIdx)+".interfgraph"
    if False: #already saved
      rt = RandomTopology()
      rt.load(randNetGraphPath+name+str(nameIdx)+".csv")
      interfGraph = InterferenceGraph(rt, interfDistance, False)
      interfGraph.save(saveInterGraphPath)

    if True:
      saveFeasibleSchedPath = feasibleSchedPath+"feasibleSched_"+name+str(nameIdx)+".fsched"
      subprocess.call(['../enumerator iecker/main', saveInterGraphPath, saveFeasibleSchedPath])