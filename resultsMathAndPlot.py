import csv
import collections
n=16
namedTuple = "mean, rho, algo, graph, beta, gamma, ArrSum, NumEdges, MaxScheds, Iter"
#queue size
for i in range(n):
  namedTuple += ", q"+str(i+1)+" "
#sched size freq
for i in range(n+1):
  namedTuple += ", s"+str(i)+" "

ResultRow = collections.namedtuple("ResultRow", namedTuple)

doc = []

betaL=[]
rhoL = []
algoL = []
graphL = []
gammaL=[]
floatIdxs = range(42)[:2] + range(42)[4:]
#([round(queue/n,2), r, algorithm, name+str(nameIdx), beta, gamma, arrivalSum, numEdges, numMaxSched, testesIt] + queuesList + maa.schedSizeFrequency))
print floatIdxs
resultFileIdx = ['All', '3', '4', '5', '6','7.parcial.copy']
for rfi in resultFileIdx:
  with open('./resultados/gitignoreR_{}.csv'.format(rfi), 'r') as csvFile:
    #skip header
    #next(csvFile)
    reader = csv.reader(csvFile, delimiter=',')
    for row in reader:
      #convert string to float
      for i in floatIdxs:
        row[i] = float(row[i])
      #trimming string
      row[2] = row[2].strip()
      row[3] = row[3].strip()
      if not 'MICE' in row[2]:
        row = row[:5]+[0]+row[5:]
        #print row
      r = ResultRow(*row)
      if not r.graph in graphL:
        graphL.append(r.graph)
      if not r.beta in betaL:
        betaL.append(r.beta)
      if not r.rho in rhoL:
        rhoL.append(r.rho)
      if not r.algo in algoL:
        algoL.append(r.algo)
      if not r.gamma in gammaL:
        gammaL.append(r.gamma)
      #print r
      #floatList = map(float, row)
      doc.append(r)
#iters = len(doc)/3./6./12./30.

print "N. results rows {}".format(len(doc))
betaL.sort()
rhoL.sort()
algoL.sort()
graphL.sort()
print "betaL",betaL
print "rhoL",rhoL
print "algoL",algoL
print "graphL",graphL
print "gammaL",gammaL
#beta [0.01, 0.1, 1.0]
#rho  [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
#algo ['CFv2', 'CFv2-NoQ', 'CFv2NQF', 'CFv4', 'CFv4-NoQ', 'CFv4NQF', 'HICSMA', 'HICSMA-NCP2', 'HICSMASEC', 'HICSMASEC-NCP2', 'HICSMASECNQF', 'ICSMA']


QueueInfo = collections.namedtuple("QueueInfo", "mean, queueML, meanFI, FIL, rho, beta, gamma, algo, graph, resultsL")
queueMeanGraphL = []
for graph in graphL:
  for rho in rhoL:
    for beta in betaL:
      for gamma in gammaL:
        for algo in algoL:
          queue = QueueInfo([-1], [], [-1], [], rho, beta, gamma, algo, graph, [])
          queueMeanGraphL.append(queue)

lenGraph = len(graphL)
lenRho = len(rhoL)
lenBeta = len(betaL)
lenAlgo = len(algoL)
lenGamma = len(gammaL)

def getIdx(rho, beta, gamma, algo, graph):
  gIdx = graphL.index(graph)
  rIdx = rhoL.index(rho)
  bIdx = betaL.index(beta)
  gammaIdx = gammaL.index(gamma)
  algoIdx = algoL.index(algo)
  
  return gIdx*lenRho*lenBeta*lenAlgo*lenGamma + rIdx*lenBeta*lenAlgo*lenGamma + bIdx*lenAlgo*lenGamma + gammaIdx*lenAlgo + algoIdx

print "Test 1"
for graph in graphL:
  for rho in rhoL:
    for beta in betaL:
      for algo in algoL:
        for gamma in gammaL:
          t = queueMeanGraphL[getIdx(rho=rho, beta=beta, gamma=gamma, algo=algo, graph=graph)]
          if t.rho != rho or t.beta != beta or t.algo != algo or t.graph != graph or t.gamma!=gamma:
            print "Error"
print "Done\n"          


for resultRow in doc:
  param = resultRow.rho, resultRow.beta, resultRow.gamma, resultRow.algo, resultRow.graph
  qMean = queueMeanGraphL[getIdx(*param)]
  mean = resultRow.mean
  #do not append more than 5 results rows, removing duplicates and some sims
  if len(qMean.queueML) < 5:
    qMean.queueML.append(mean)
  qMean.resultsL.append(resultRow)

"""
print "Checking for wrong duplicates dealing"
for q in queueMeanGraphL:
  print ".\r",
  if len(q.resultsL) > 5:
    #print len(q.queueML), q.rho, q.beta, q.algo, "   \t" if q.algo in ["CFv2", "CFv4"] else "\t", q.graph
    for result in q.resultsL:
      if not result.mean in q.queueML:
        print "Error",result.mean, q.resultsL, q.queueML
print "\nDone\n"

removeList = []
print "Checks for forgotten sims"
for q in queueMeanGraphL:
  if len(q.queueML) != 5:# and q.rho==0.5:
    print "Error",
    print len(q.queueML), q.rho, q.beta, q.algo, "   \t" if q.algo in ["CFv2", "CFv4"] else "\t", q.graph, "\r",
    removeList.append(q)
#for q in removeList:
#  queueMeanGraphL.remove(q)
print "\nDone\n"
"""
auxrho = [0.7, 0.8, 0.9, 1.0]
auxbeta =[0.01, 0.1, 1, 1.5]
auxgamma = [0.8, 1, 1.2, 1.4, 1.5]
auxalgorithms = ["MICE10-ICSMA", "MICEe-ICSMA", "MICE10-CFv2", "MICEe-CFv2", "MICE10-CFv4", "MICEe-CFv4", "MICE10-CFGDv2", "MICEe-CFGDv2", "MICE10-CFGDv4", "MICEe-CFGDv4" ]
leftSims = []
#search for leftover sims
for q in queueMeanGraphL:
  if len(q.queueML) != 5:
    if q.rho in auxrho and q.beta in auxbeta and q.gamma in auxgamma and q.algo in auxalgorithms:
      params = q.rho, q.beta, q.gamma, q.algo
      if not params in leftSims:
        leftSims.append(params)
for i in leftSims:
  print i
sortedleftsims = sorted(leftSims, lambda x,y: x[1] > y[1])  
print len(sortedleftsims)




print "Calculating Means"
for q in queueMeanGraphL:
  print ".\r",
  summ = sum(q.queueML)
  if summ>0:
    mean = summ/len(q.queueML)
    q.mean[0] = mean
print "\nDone\n"


print "Calculating Fairness Index"
for q in queueMeanGraphL:
  print ".\r",
  for r in q.resultsL:
    fiSum = 0
    fiSqSum = 0
    for nodeIdx in ["q{}".format(i+1) for i in range(n)]:
      qVal = eval("r."+nodeIdx)
      fiSum+=qVal
      fiSqSum += qVal**2
    fi = (fiSum**2)/(n*fiSqSum)
    q.FIL.append(fi)
  if len(q.FIL) > 0:
    q.meanFI[0]=sum(q.FIL)/float(len(q.FIL))
  else:
    q.meanFI[0]=-1

print "\nDone\n"


#data structure
queueMeanL = []
for rho in rhoL:
  for beta in betaL:
    for gamma in gammaL:
      for algo in algoL:
        queue = QueueInfo([-1], [],[-1], [], rho, beta, gamma, algo, None, None)
        queueMeanL.append(queue)

print "Test 2"
for rho in rhoL:
  for beta in betaL:
    for gamma in gammaL:
      for algo in algoL:
        t = queueMeanL[getIdx(rho=rho, beta=beta, gamma=gamma, algo=algo, graph=graphL[0])]
        if t.rho != rho or t.beta != beta or t.algo != algo or t.gamma != gamma:
          print "Error"
print "Done\n"

#mean over all graphs of a given rho, beta and algo
for qm in queueMeanL:
  for graph in graphL:
    param = qm.rho, qm.beta, qm.gamma, qm.algo, graph
    qMean = queueMeanGraphL[getIdx(*param)]
    qm.queueML.append(qMean.mean[0])
    qm.FIL.append(qMean.meanFI[0])

print "Calculating QMeans and FIMeans"
for q in queueMeanL:
  print ".\r",
  summ = sum(q.queueML)
  fiSumm = sum(q.FIL)
  if summ>0:
    mean = summ/len(q.queueML)
    fimean = fiSumm/len(q.FIL)
    q.mean[0] = mean
    q.meanFI[0] = fimean
print "\nDone\n"


#getting the best beta fit for each algo
queueMeanL.sort(key=lambda obj: obj.mean[0])
bestBetaQueues = []
for qm in queueMeanL:
  inBB = False
  for bb in bestBetaQueues:
    if qm.algo == bb.algo and qm.rho == bb.rho:
      if bb.mean[0] > qm.mean[0]:
        print "Error"
      inBB = True
      break
  if not inBB and qm.mean[0]>0:
    bestBetaQueues.append(qm)


bestBetaQueues.sort(key=lambda obj: obj.rho)
print ""
print "============================================"
print "===============  EVEN TRAFFIC =============="
print "============================================"
saveFile = "processedResults.csv"
prf = open(saveFile,'w')
prf.write("rho, beta, gamma, FI, algo, mean\n")
rhoMem = 0
for q in bestBetaQueues:
  if "UT" in q.algo:
    continue
  if rhoMem != q.rho:
    print "\n-Rho-\t-Beta-\t-Gamma-\t-FI-\t-Algo-\t\t\t-QMean-"
    rhoMem=q.rho
  #if q.rho == 0.8:
  if True:
    if len(q.algo) > 7 and len(q.algo) < 16:
      algoSpcs = q.algo+"\t\t"
    elif len(q.algo) > 14:
      algoSpcs = q.algo + "\t"
    elif len(q.algo)<8:
      algoSpcs = q.algo+"\t\t\t"
        #algoSpcs = q.algo if len(q.algo) > 7 else q.algo+"\t"
    print "{}\t{}\t{}\t{}\t{}{}".format(q.rho, q.beta, q.gamma, round(q.meanFI[0],2), algoSpcs, round(q.mean[0],3))
    line = "{},{},{},{},{},{}\n".format(q.rho, q.beta, q.gamma, round(q.meanFI[0],2), q.algo, round(q.mean[0],3))
    prf.write(line)
print ""
print "============================================"
print "==============  UNEVEN TRAFFIC ============="
print "============================================"
rhoMem = 0
for q in bestBetaQueues:
  if not "UT" in q.algo:
    continue
  if rhoMem != q.rho:
    print "\n-Rho-\t-Beta-\t-Gamma-\t-FI-\t-Algo-\t\t\t-QMean-"
    rhoMem=q.rho
  #if q.rho == 0.8:
  if True:
    if len(q.algo) > 7 and len(q.algo) < 16:
      algoSpcs = q.algo+"\t\t"
    elif len(q.algo) > 14:
      algoSpcs = q.algo + "\t"
    elif len(q.algo)<8:
      algoSpcs = q.algo+"\t\t\t"
        #algoSpcs = q.algo if len(q.algo) > 7 else q.algo+"\t"
    print "{}\t{}\t{}\t{}\t{}{}".format(q.rho, q.beta, q.gamma, round(q.meanFI[0],2), algoSpcs, round(q.mean[0],3))
    line = "{},{},{},{},{},{}\n".format(q.rho, q.beta, q.gamma, round(q.meanFI[0],2), q.algo, round(q.mean[0],3))
    prf.write(line)
prf.flush()
#collections.namedtuple("BetaFit", "algo, 0.01, 0.1, 1.0")
algoBetaFit = [(algo,[0,0,0]) for algo in algoL]

for algo in algoBetaFit:
  for bestQ in bestBetaQueues:
    if bestQ.algo == algo[0] and bestQ.rho > 0.6:
      if bestQ.beta == 0.01:
        algo[1][0] += 1
      if bestQ.beta == 0.1:
        algo[1][1] += 1
      if bestQ.beta == 1.0:
        algo[1][2] += 1
print algoBetaFit

