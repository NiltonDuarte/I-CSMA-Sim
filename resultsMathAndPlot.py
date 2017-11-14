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


QueueMean = collections.namedtuple("QueueMean", "meanL, rho, beta, algo, graph, resultsL")
queueMeanL = []
for graph in graphL:
  for rho in rhoL:
    for beta in betaL:
      for algo in algoL:
        queue = QueueMean([], rho, beta, algo, graph, [])
        queueMeanL.append(queue)

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

"""
#getidx func test
for graph in graphL:
  for rho in rhoL:
    for beta in betaL:
      for algo in algoL:
        t = queueMeanL[getIdx(rho=rho, beta=beta, algo=algo, graph=graph)]
        if t.rho != rho or t.beta != beta or t.algo != algo or t.graph != graph:
          print "Error"
"""



for resultRow in doc:
  param = resultRow.rho, resultRow.beta, resultRow.algo, resultRow.graph
  qMean = queueMeanL[getIdx(*param)]
  mean = resultRow.mean
  if len(qMean.meanL) < 5:
    qMean.meanL.append(mean)
  qMean.resultsL.append(resultRow)

#checks for wrong duplicate dealing
for q in queueMeanL:
  if len(q.resultsL) > 5:
    #print len(q.meanL), q.rho, q.beta, q.algo, "   \t" if q.algo in ["CFv2", "CFv4"] else "\t", q.graph
    for result in q.resultsL:
      if not result.mean in q.meanL:
        print "Error",result.mean, q.resultsL, q.meanL

#checks for forgot sims
sum = 0
for q in queueMeanL:
  
  if len(q.meanL) != 5:# and q.rho==0.5:
    print len(q.meanL), q.rho, q.beta, q.algo, "   \t" if q.algo in ["CFv2", "CFv4"] else "\t", q.graph
    sum += 1
print sum
