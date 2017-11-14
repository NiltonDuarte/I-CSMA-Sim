from device_graph import *
from interference_graph import *
from access_algorithm import *
from network_structure import *
import sys
import time
print "Initializing sim"
print sys.argv
start_time = time.time()

#LattDistance = 70.
#LattSize = 4
#LattPairDist = 40.
randNetGraphPath = "./randomGraphs/savedGraphs/"
saveResultsFilePath = "../resultados/"
maxSchedPath = "./randomGraphs/maximalScheds/"
maxSchedFileName = "MaximalScheds_"
fileNames = ["DevGraph16AllRandWR", "DevGraph16NPV","DevGraph16NPV_MD3_"] #
fileNamesIdx = 10

windowP1 = 20
windowP2 = 8
heuristicWindowP2 = windowP1 + windowP2

#rho = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
rho = [float(sys.argv[2])]

betaList = [float(sys.argv[1])] #[0.01,0.1,1]
testesIt = 100000
rounds = 5
InterfDist = 80.
algorithms = [sys.argv[3]]#["ICSMA", "HICSMA", "HICSMASEC", "CFv4", "CFv2"]#"HICSMA-NCP2", "HICSMASEC-NCP2", "CFv2-NoQ", "CFv4-NoQ"]# "HICSMASECNQF", "CFv4NQF", "CFv2NQF"]#"ICSMA", "HICSMA", "HICSMASEC", "CFv4", "CFv2"
#print "Using rho = "+str(rho) + " and beta = "+str(betaList)

n = 16

resultsSaveFile = saveResultsFilePath+"gitignoreR_"+".csv"
for name in fileNames:
  for nameIdx in range(fileNamesIdx):
    netGraphName = randNetGraphPath+name+str(nameIdx)
    #print netGraphName
    arrivalMean, numMaxSched, arrivalSum = getArrivalVectorDict(maxSchedPath+maxSchedFileName+name+str(nameIdx)+".csv")

    #print arrivalMean

    netGraphName = randNetGraphPath+name+str(nameIdx)
    netGraph = RandomTopology()
    netGraph.load(netGraphName+".csv")
    interfGraph = InterferenceGraph(netGraph, InterfDist, False)
    numEdges = len(interfGraph.edges)
    #print "Arrival Sum: {} N. Max Sched: {} N.Edges: {}".format(arrivalSum, numMaxSched, numEdges)
    for algorithm in algorithms:
      for i in range(rounds):
        for beta in betaList:
          for r in rho:
            
            netGraphName = randNetGraphPath+name+str(nameIdx)
            netGraph = RandomTopology()
            netGraph.load(netGraphName+".csv")
            interfGraph = InterferenceGraph(netGraph, InterfDist, False)

            #turnOnFunctions(self, newQF, newSF, newQP, newCP2):
            if algorithm == "ICSMA":
              maa = MultipleAccessAlgorithm(interfGraph, beta, 252+28,r, arrivalMean, False, True) 
              maa.turnOnFunctions(False,False,False,False)
              schedule = maa.runICSMA(testesIt, windowP1, windowP2) 

            elif algorithm == "HICSMA":
              maa = MultipleAccessAlgorithm(interfGraph, beta, 252+28,r, arrivalMean, False, True) 
              maa.turnOnFunctions(False,False,False,False)
              schedule = maa.runHeuristicICSMA(testesIt, heuristicWindowP2)

            elif algorithm == "HICSMA-NCP2":
              maa = MultipleAccessAlgorithm(interfGraph, beta, 252+28,r, arrivalMean, False, True) 
              maa.turnOnFunctions(False,False,False,False)
              schedule = maa.runHeuristicICSMA(testesIt, heuristicWindowP2)

            elif algorithm == "HICSMASEC":
              maa = MultipleAccessAlgorithm(interfGraph, beta, 252+28,r, arrivalMean, False, True) 
              maa.turnOnFunctions(False,True,'sech',True)
              schedule = maa.runHeuristicICSMA(testesIt, heuristicWindowP2) 

            elif algorithm == "HICSMASEC-NCP2":
              maa = MultipleAccessAlgorithm(interfGraph, beta, 252+28,r, arrivalMean, False, True) 
              maa.turnOnFunctions(False,True,'sech',True)
              schedule = maa.runHeuristicICSMA(testesIt, heuristicWindowP2)           

            elif algorithm == "CFv2":
              maa = MultipleAccessAlgorithm(interfGraph, beta, 252+16,r, arrivalMean, False, True)     
              maa.turnOnFunctions(False,True,'sech',False)
              schedule = maa.runCollisionFree(testesIt, 'v2', 4, 4)

            elif algorithm == "CFv4":
              maa = MultipleAccessAlgorithm(interfGraph, beta, 252+16,r, arrivalMean, False, True) 
              maa.turnOnFunctions(False,True,'sech',False)
              schedule = maa.runCollisionFree(testesIt, 'v4', 4, 4)

            elif algorithm == "HICSMASECNQF":
              maa = MultipleAccessAlgorithm(interfGraph, beta, 252+28,r, arrivalMean, False, True) 
              maa.turnOnFunctions(True,True,'sech',False)
              schedule = maa.runHeuristicICSMA(testesIt, heuristicWindowP2) 

            elif algorithm == "CFv2NQF":
              maa = MultipleAccessAlgorithm(interfGraph, beta, 252+16,r, arrivalMean, False, True)     
              maa.turnOnFunctions(True,True,'sech',False)
              schedule = maa.runCollisionFree(testesIt, 'v2', 4, 4)

            elif algorithm == "CFv4NQF":
              maa = MultipleAccessAlgorithm(interfGraph, beta, 252+16,r, arrivalMean, False, True) 
              maa.turnOnFunctions(True,True,'sech',False)
              schedule = maa.runCollisionFree(testesIt, 'v4', 4, 4)

            elif algorithm == "CFv2-NoQ":
              maa = MultipleAccessAlgorithm(interfGraph, beta, 252+16,r, arrivalMean, False, True) 
              maa.turnOnFunctions(True,True,'sech',False, False)
              schedule = maa.runCollisionFree(testesIt, 'v4', 4, 4)

            elif algorithm == "CFv4-NoQ":
              maa = MultipleAccessAlgorithm(interfGraph, beta, 252+16,r, arrivalMean, False, True) 
              maa.turnOnFunctions(True,True,'sech',False, False)
              schedule = maa.runCollisionFree(testesIt, 'v4', 4, 4)              

            queue=0
            queuesList = []
            maa.interfGraph.nodes.sort(key=lambda node: node.id)
            for node in maa.interfGraph.nodes:
              queuesList.append(node.queueSize)
              queue += node.queueSize
            results=", ".join(str(x) for x in ([round(queue/n,2), r, algorithm, name+str(nameIdx), beta, arrivalSum, numEdges, numMaxSched, testesIt] + queuesList + maa.schedSizeFrequency))
            #print algorithm, beta, r, round(queue/n,2)
            with open(resultsSaveFile,"a") as rsf:
              rsf.write(str(results))
              rsf.write('\n')
              rsf.flush()
        #print " "

print("--- %s seconds ---" % (time.time() - start_time))