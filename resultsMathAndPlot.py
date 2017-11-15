import csv
import collections
n=16
namedTuple = "mean, rho, algo, graph, beta, ArrSum, NumEdges, MaxScheds, Iter"
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
floatIdxs = range(42)[:2] + range(42)[4:]
print floatIdxs
with open('./resultados/gitignoreR_All.csv', 'r') as csvFile:
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
    r = ResultRow(*row)
    if not r.graph in graphL:
      graphL.append(r.graph)
    if not r.beta in betaL:
      betaL.append(r.beta)
    if not r.rho in rhoL:
      rhoL.append(r.rho)
    if not r.algo in algoL:
      algoL.append(r.algo)
    #print r
    #floatList = map(float, row)
    doc.append(r)
iters = len(doc)/3./6./12./30.

print iters
betaL.sort()
rhoL.sort()
algoL.sort()
graphL.sort()
print betaL
print rhoL
print algoL
print graphL
#beta [0.01, 0.1, 1.0]
#rho  [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
#algo ['CFv2', 'CFv2-NoQ', 'CFv2NQF', 'CFv4', 'CFv4-NoQ', 'CFv4NQF', 'HICSMA', 'HICSMA-NCP2', 'HICSMASEC', 'HICSMASEC-NCP2', 'HICSMASECNQF', 'ICSMA']


QueueInfo = collections.namedtuple("QueueInfo", "mean, queueML, rho, beta, algo, graph, resultsL")
queueMeanGraphL = []
for graph in graphL:
  for rho in rhoL:
    for beta in betaL:
      for algo in algoL:
        queue = QueueInfo([-1], [], rho, beta, algo, graph, [])
        queueMeanGraphL.append(queue)

lenGraph = len(graphL)
lenRho = len(rhoL)
lenBeta = len(betaL)
lenAlgo = len(algoL)


def getIdx(rho, beta, algo, graph):
  gIdx = graphL.index(graph)
  rIdx = rhoL.index(rho)
  bIdx = betaL.index(beta)
  algoIdx = algoL.index(algo)
  return gIdx*lenRho*lenBeta*lenAlgo + rIdx*lenBeta*lenAlgo + bIdx*lenAlgo + algoIdx

print "Test 1"
for graph in graphL:
  for rho in rhoL:
    for beta in betaL:
      for algo in algoL:
        t = queueMeanGraphL[getIdx(rho=rho, beta=beta, algo=algo, graph=graph)]
        if t.rho != rho or t.beta != beta or t.algo != algo or t.graph != graph:
          print "Error"
print "Done\n"          


for resultRow in doc:
  param = resultRow.rho, resultRow.beta, resultRow.algo, resultRow.graph
  qMean = queueMeanGraphL[getIdx(*param)]
  mean = resultRow.mean
  if len(qMean.queueML) < 5:
    qMean.queueML.append(mean)
  qMean.resultsL.append(resultRow)


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

print "Calculating Means"
for q in queueMeanGraphL:
  print ".\r",
  summ = sum(q.queueML)
  if summ>0:
    mean = summ/len(q.queueML)
    q.mean[0] = mean
print "\nDone\n"

#data structure
queueMeanL = []
for rho in rhoL:
  for beta in betaL:
    for algo in algoL:
      queue = QueueInfo([-1], [], rho, beta, algo, None, None)
      queueMeanL.append(queue)

print "Test 2"
for rho in rhoL:
  for beta in betaL:
    for algo in algoL:
      t = queueMeanL[getIdx(rho=rho, beta=beta, algo=algo, graph=graphL[0])]
      if t.rho != rho or t.beta != beta or t.algo != algo:
        print "Error"
print "Done\n"

#mean over all graphs of a given rho, beta and algo
for qm in queueMeanL:
  for graph in graphL:
    param = qm.rho, qm.beta, qm.algo, graph
    qMean = queueMeanGraphL[getIdx(*param)]
    qm.queueML.append(qMean.mean[0])

print "Calculating Means"
for q in queueMeanL:
  print ".\r",
  summ = sum(q.queueML)
  if summ>0:
    mean = summ/len(q.queueML)
    q.mean[0] = mean
print "\nDone\n"


#getting the best beta fit for each algo
queueMeanL.sort(key=lambda obj: obj.mean[0])
bestBetaQueues = []
for qm in queueMeanL:
  inBB = False
  for bb in bestBetaQueues:
    if qm.algo == bb.algo and qm.rho == bb.rho:
      if bb.mean > qm.mean:
        print "Error"
      inBB = True
      break
  if not inBB:
    bestBetaQueues.append(qm)


bestBetaQueues.sort(key=lambda obj: obj.rho)
for q in bestBetaQueues:
  #if q.rho == 0.8:
  print "{}\t{}\t{}\t{}".format(q.rho, q.beta, q.algo, round(q.mean[0],3))
