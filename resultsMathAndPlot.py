# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import csv
import collections
#import plotly
#import plotly.plotly as py
#from plotly.graph_objs import *
import matplotlib.pyplot as plt
import operator
import scipy.stats as st
import numpy as np

n=16
namedTuple = "mean, rho, algo, graph, beta, gamma, delayT, ArrSum, NumEdges, MaxScheds, Iter"
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
delayTL= []
floatIdxs = range(44)[:2] + range(44)[4:]
#([round(queue/n,2), r, algorithm, name+str(nameIdx), beta, gamma, delayT, arrivalSum, numEdges, numMaxSched, testesIt] + queuesList + maa.schedSizeFrequency))
print floatIdxs
#files , resultFileIdx= "Rfiles", ['R2_','R_All', 'R_3', 'R_4', 'R_5', 'R_6','R_7']
#files , resultFileIdx = "RFfiles", ['RF_','RF_1']
files , resultFileIdx= "RDelayed", ["RDelayed_"]
for rfi in resultFileIdx:
  with open('./resultados/gitignore{}.csv'.format(rfi), 'r') as csvFile:
    #skip header
    #next(csvFile)
    reader = csv.reader(csvFile, delimiter=',')
    rowCount = 0
    for row in reader:
      rowCount += 1
      #convert string to float
      #print rowCount, len(row), row

      for i in floatIdxs:
        row[i] = float(row[i])
      #trimming string
      row[2] = row[2].strip()
      row[3] = row[3].strip()
      #if files!= "RFfiles" and not 'MICE' in row[2]:
      #  row = row[:5]+[0]+row[5:]
        #print row
      r = ResultRow(*row)
      if r.rho > 1.0: continue
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
      if not r.delayT in delayTL:
        delayTL.append(r.delayT)
      #print r
      #floatList = map(float, row)
      doc.append(r)
#iters = len(doc)/3./6./12./30.

print "N. results rows {}".format(len(doc))
betaL.sort()
rhoL.sort()
algoL.sort()
graphL.sort()
gammaL.sort()
delayTL.sort()
print "betaL",betaL
print "rhoL",rhoL
print "algoL",algoL
print "graphL",graphL
print "gammaL",gammaL
print "delayTL",delayTL
#beta [0.01, 0.1, 1.0]
#rho  [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
#algo ['CFv2', 'CFv2-NoQ', 'CFv2NQF', 'CFv4', 'CFv4-NoQ', 'CFv4NQF', 'HICSMA', 'HICSMA-NCP2', 'HICSMASEC', 'HICSMASEC-NCP2', 'HICSMASECNQF', 'ICSMA']


QueueInfo = collections.namedtuple("QueueInfo", "mean, queueML, meanFI, FIL, rho, beta, gamma, delayT, algo, graph, resultsL")
queueMeanGraphL = []
for graph in graphL:
  for rho in rhoL:
    for beta in betaL:
      for gamma in gammaL:
        for delayT in delayTL:
          for algo in algoL:
            queue = QueueInfo([-1], [], [-1], [], rho, beta, gamma, delayT, algo, graph, [])
            queueMeanGraphL.append(queue)

lenGraph = len(graphL)
lenRho = len(rhoL)
lenBeta = len(betaL)
lenGamma = len(gammaL)
lenDelayT = len(delayTL)
lenAlgo = len(algoL)


def getIdx(rho, beta, gamma, delayT, algo, graph):
  gIdx = graphL.index(graph)
  rIdx = rhoL.index(rho)
  bIdx = betaL.index(beta)
  gammaIdx = gammaL.index(gamma)
  tIdx = delayTL.index(delayT)
  algoIdx = algoL.index(algo)
  
  return gIdx*lenRho*lenBeta*lenAlgo*lenGamma*lenDelayT + rIdx*lenBeta*lenAlgo*lenGamma*lenDelayT + bIdx*lenAlgo*lenGamma*lenDelayT + gammaIdx*lenDelayT*lenAlgo + tIdx*lenAlgo + algoIdx

print "Test 1"
for graph in graphL:
  for rho in rhoL:
    for beta in betaL:
      for algo in algoL:
        for gamma in gammaL:
          for dT in delayTL:
            t = queueMeanGraphL[getIdx(rho=rho, beta=beta, gamma=gamma, delayT=dT ,algo=algo, graph=graph)]
            if t.rho != rho or t.beta != beta or t.algo != algo or t.graph != graph or t.gamma!=gamma or t.delayT!=dT:
              print "Error"
print "Done\n"          


for resultRow in doc:
  param = resultRow.rho, resultRow.beta, resultRow.gamma, resultRow.delayT, resultRow.algo, resultRow.graph
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

"""
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
"""

#data structure
queueMeanL = []
for rho in rhoL:
  for beta in betaL:
    for gamma in gammaL:
      for dT in delayTL:
        for algo in algoL:
          queue = QueueInfo([-1], [],[-1], [], rho, beta, gamma, dT, algo, None, None)
          queueMeanL.append(queue)

print "Test 2"
for rho in rhoL:
  for beta in betaL:
    for gamma in gammaL:
      for dT in delayTL:
        for algo in algoL:
          t = queueMeanL[getIdx(rho=rho, beta=beta, gamma=gamma, delayT=dT, algo=algo, graph=graphL[0])]
          if t.rho != rho or t.beta != beta or t.algo != algo or t.gamma != gamma or t.delayT!= dT:
            print "Error"
print "Done\n"

#mean over all graphs of a given rho, beta, delayT and algo
#getIdx(rho, beta, gamma, T, algo, graph):
for qm in queueMeanL:
  for graph in graphL:
    param = qm.rho, qm.beta, qm.gamma, qm.delayT, qm.algo, graph
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
prf.write("rho, beta, gamma, dT, FI, algo, mean\n")
rhoMem = 0
for q in bestBetaQueues:
  if "UT" in q.algo:
    continue
  if rhoMem != q.rho:
    print "\n-Rho-\t-Beta-\t-Gamma-\t-dT-\t-FI-\t-Algo-\t\t\t-QMean-"
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
    print "{}\t{}\t{}\t{}\t{}\t{}{}".format(q.rho, q.beta, q.gamma, q.delayT, round(q.meanFI[0],2), algoSpcs, round(q.mean[0],3))
    line = "{},{},{},{},{},{},{}\n".format(q.rho, q.beta, q.gamma, q.delayT, round(q.meanFI[0],2), q.algo, round(q.mean[0],3))
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
    print "{}\t{}\t{}\t{}\t{}\t{}{}".format(q.rho, q.beta, q.gamma, q.delayT, round(q.meanFI[0],2), algoSpcs, round(q.mean[0],3))
    line = "{},{},{},{},{},{},{}\n".format(q.rho, q.beta, q.gamma, q.delayT, round(q.meanFI[0],2), q.algo, round(q.mean[0],3))
    prf.write(line)
prf.flush()
#collections.namedtuple("BetaFit", "algo, 0.01, 0.1, 1.0")
algoBetaFit = [(algo,[0,0,0,0]) for algo in algoL]

for algo in algoBetaFit:
  for bestQ in bestBetaQueues:
    if bestQ.algo == algo[0] and bestQ.rho > 0.6:
      if bestQ.beta == 0.01:
        algo[1][0] += 1
      if bestQ.beta == 0.1:
        algo[1][1] += 1
      if bestQ.beta == 1.0:
        algo[1][2] += 1
      if bestQ.beta == 1.5:
        algo[1][3] += 1
print algoBetaFit


def multiLinePlot(figname, aliasLegDict, data, variationParam, ordenationParam, restrictionParam="", restrictionValueList=[""], restrictionParam2="", 
                                               restrictionValueList2=[""], variationRestrictionList="Todos", ordenationRestricionList = "Todos", yAxisTicks=None,
                                               varFileNameAlias = None):
  dataInfo = collections.namedtuple("TraceInfo", "valuePairs, varParam, originalData")
  mData = data[:]
  varParam = variationParam
  oParam = ordenationParam
  dataD = {}
  printList = []
  for d in mData:
    if d.mean[0] > -1:
      if (variationRestrictionList == "Todos" or getattr(d,varParam) in variationRestrictionList) and (ordenationRestricionList == "Todos" or getattr(d,oParam) in ordenationRestricionList):
        #printList.append((round(d.mean[0]), "beta=",d.beta, "rho=",d.rho, "gamma=",d.gamma))
        #print "===========", round(d.mean[0],3), "beta=",d.beta, "rho=",d.rho, "gamma=",d.gamma
        #print "============================================"
        if getattr(d,restrictionParam,"") in restrictionValueList and getattr(d,restrictionParam2,"") in restrictionValueList2:
          varParamVal = getattr(d, varParam)
          oParamVal = getattr(d, oParam)
        
          #print "===========", round(d.mean[0],3), "beta=",d.beta, "rho=",d.rho, "gamma=",d.gamma
          if not varParamVal in dataD.keys():
            dataD[varParamVal] = dataInfo([(oParamVal, d.mean[0])], varParamVal, 0)
          else:
            dataD[varParamVal].valuePairs.append((oParamVal, d.mean[0]))
  printList.sort(key=lambda t: t[6])
  printList.sort(key=lambda t: t[4])
  printList.sort(key=lambda t: t[2])
  #for t in printList:
    #print t
  for i in dataD.keys():
    dataDVal = dataD[i]   
    #print "1",i,dataDVal   
    ordes=set(map(lambda pair: pair[0], dataDVal.valuePairs))
    newpairs = [(orde,[pair[1] for pair in dataDVal.valuePairs if pair[0]==orde]) for orde in ordes]
    y = [pair[1] for pair in dataDVal.valuePairs if pair[0]==orde]*20
    print "Y=",y
    erroy = st.t.interval(0.95, len(y)-1, loc=np.mean(y), scale=st.sem(y))
    print "ERRO Y",erroy
    meanvaluePairs = []
    for pairs in newpairs:
      mean = sum(pairs[1])/len(pairs[1])
      err = abs(erroy[0]-mean)
      pair = (pairs[0],mean, err)
      meanvaluePairs.append(pair)
    del dataDVal.valuePairs[:]
    for pair in meanvaluePairs:
      dataDVal.valuePairs.append(pair)


  traces = []
  markerList = ["o", "^", "s", "*", "D", "x", "+","v", "H","o", "^", "s", "*", "D", "x", "+","v", "H","o", "^", "s", "*", "D", "x", "+","v", "H"]
  mLIdx = 0
  legendHandler = []
  xMaxLen = []
  plt.rc('font', size=17) 
  for i in dataD.keys():
    dataDVal = dataD[i]
    #print "2",i,dataDVal
    dataDVal.valuePairs.sort(key=lambda valPair: valPair[0])
    x, y, erroy = zip(*dataDVal.valuePairs)
    if len(x) > len(xMaxLen): xMaxLen=x[:]
    legString = i
    if i in aliasLegDict.keys():
      legString=aliasLegDict[i]
    print y
    plt.errorbar(x,y,yerr=erroy)
    plt.plot(x,y, markerList[mLIdx]+'-', label='{}={}'.format(variationParam,legString), color='black', linewidth=1)
    #legendHandler.append(leg)
    mLIdx += 1

  handles, labels = plt.axes().get_legend_handles_labels()
  hl = sorted(zip(handles, labels),
            key=operator.itemgetter(1))
  handles2, labels2 = zip(*hl)
  plt.legend(handles2, labels2)
  plt.yscale('log')  
  plt.ylabel(u'Média do tamanho das filas')
  plt.xticks(xMaxLen)
  if yAxisTicks!= None:  plt.yticks(yAxisTicks)
  plt.xlabel(ordenationParam)
  #plt.title(restrictionValueList)
  varfilename = variationRestrictionList
  if varFileNameAlias != None: varfilename = varFileNameAlias
  figName = "{}-var={}={}-ord={}={}-{}={}-{}={}.png".format(figname, variationParam,varfilename, ordenationParam,ordenationRestricionList, restrictionParam, restrictionValueList, restrictionParam2, restrictionValueList2)
  plt.savefig(figName)
  #plt.show()
  plt.clf()
  plt.cla()
#[(1.0, 2906.7745333333337), (0.9, 3175.8592333333336), (0.8, 2218.7504)]
  return
#data, variationParam, ordenationParam, restrictionParam="", restrictionValue=""
figName = files
rho01=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
rho02=[0.9, 0.92, 0.94, 0.96, 0.98, 1.0] 
rho03=[0.8, 0.9, 1.0]
yaxis1 = [10**3, 10**4]
yaxis2 = [1, 10, 10**2, 10**3, 10**4]
yaxis3 = [7*10**3, 10**4, 1.5*10**4]
yaxis4 = [10**3, 10**4, 10**5]
yaxis5 = [1, 10, 10**2, 10**3]
yaxis6 = [10**3, 7*10**3]
yaxis7 = [1, 10, 10**2]
aliasDict = {"MICE-ICSMAPURE":"MICE-ICSMA",
             "MICEe-TrueCFGDv4": "MICE-GD-EsMAI",
             "MICEe-TrueCFGDv2": "MICE-GD-EsMa",
             "MICEe-CFv4": "MICE-EsMAI",
             "MICEe-CFv2": "MICE-EsMa",
             "CFv2-NoQ": "EsMa-S/F",
             "MICE-ICSMAPURE-UT":"MICE-ICSMA",
             "MICEe-TrueCFGDv4-UT": "MICE-GD-EsMAI",
             "MICEe-TrueCFGDv2-UT": "MICE-GD-EsMa",
             "MICEe-CFv4-UT": "MICE-EsMAI",
             "MICEe-CFv2-UT": "MICE-EsMa",
             "CFv2-NoQ-UT": "EsMa-S/F",
             "MICE-ICSMAPURE-UT2":"MICE-ICSMA",
             "MICEe-TrueCFGDv4-UT2": "MICE-GD-EsMAI",
             "MICEe-TrueCFGDv2-UT2": "MICE-GD-EsMa",
             "MICEe-CFv4-UT2": "MICE-EsMAI",
             "MICEe-CFv2-UT2": "MICE-EsMa",
             "CFv2-NoQ-UT2": "EsMa-S/F",
             "ICSMA-UT" : "ICSMA",
             "ICSMA-UT2" : "ICSMA",
}
#for q in queueMeanL:
#  print q
#  print "------" 
if False and figName == "Rfiles":
  if True:
  #ICSMA variando beta
    multiLinePlot(figName+"01-", aliasDict, queueMeanL,variationParam="beta",
                             ordenationParam="rho",
                             restrictionParam="algo",
                             restrictionValueList=["ICSMA"],
                             yAxisTicks=yaxis1)
                                                       
    #MICE-ICSMA variando beta, todos gamma
    multiLinePlot(figName+"06-", aliasDict, queueMeanL,variationParam="beta",
                             ordenationParam="rho",
                             restrictionParam="algo",
                             restrictionValueList=["MICE-ICSMAPURE"],
                             yAxisTicks=yaxis1)

    #MICE-ICSMA variando gamma, fixo beta = 1.0
    multiLinePlot(figName+"07.0-", aliasDict, queueMeanL,variationParam="gamma",
                             ordenationParam="rho",
                             restrictionParam="algo",
                             restrictionValueList=["MICE-ICSMAPURE"],
                             restrictionParam2="beta", 
                             restrictionValueList2=[1.0],
                             yAxisTicks=yaxis1)
    #MICE-ICSMA variando gamma, fixo beta = 0.1
    multiLinePlot(figName+"07.1-", aliasDict, queueMeanL,variationParam="gamma",
                             ordenationParam="rho",
                             restrictionParam="algo",
                             restrictionValueList=["MICE-ICSMAPURE"],
                             restrictionParam2="beta", 
                             restrictionValueList2=[0.1],
                             yAxisTicks=yaxis1)
    #MICE-ICSMA variando gamma, fixo beta = 1.5
    multiLinePlot(figName+"07.2-", aliasDict, queueMeanL,variationParam="gamma",
                             ordenationParam="rho",
                             restrictionParam="algo",
                             restrictionValueList=["MICE-ICSMAPURE"],
                             restrictionParam2="beta", 
                             restrictionValueList2=[1.5],
                             yAxisTicks=yaxis1)

    #MICE-ICSMA variando gamma, todos beta
    multiLinePlot(figName+"08-", aliasDict, queueMeanL,variationParam="gamma",
                             ordenationParam="rho",
                             restrictionParam="algo",
                             restrictionValueList=["MICE-ICSMAPURE"],
                             yAxisTicks=yaxis1)

    multiLinePlot(figName+"09.0-UT-", aliasDict, queueMeanL,variationParam="algo",
                           ordenationParam="rho",
                           restrictionParam="beta",
                           restrictionValueList=[0.1],
                           restrictionParam2="gamma", 
                           restrictionValueList2=[0, 2.5], 
                           variationRestrictionList=["MICE-ICSMAPURE-UT", "MICEe-TrueCFGDv4-UT", "MICEe-TrueCFGDv2-UT", "MICEe-CFv4-UT", "MICEe-CFv2-UT",  "CFv2-NoQ-UT", "ICSMA-UT"],
                           ordenationRestricionList=rho03,
                           yAxisTicks=yaxis1,
                           varFileNameAlias="UT")

    multiLinePlot(figName+"09.1-UT-", aliasDict, queueMeanL,variationParam="algo",
                           ordenationParam="rho",
                           restrictionParam="beta",
                           restrictionValueList=[1.0],
                           restrictionParam2="gamma", 
                           restrictionValueList2=[0, 2.5], 
                           variationRestrictionList=["MICE-ICSMAPURE-UT", "MICEe-TrueCFGDv4-UT", "MICEe-TrueCFGDv2-UT", "MICEe-CFv4-UT", "MICEe-CFv2-UT",  "CFv2-NoQ-UT", "ICSMA-UT"],
                           ordenationRestricionList=rho03,
                           yAxisTicks=yaxis1,
                           varFileNameAlias="UT")

    multiLinePlot(figName+"09.2-UT-", aliasDict, queueMeanL,variationParam="algo",
                           ordenationParam="rho",
                           restrictionParam="beta",
                           restrictionValueList=[1.0],
                           restrictionParam2="gamma", 
                           restrictionValueList2=[0, 2.5], 
                           variationRestrictionList=["MICE-ICSMAPURE-UT", "MICEe-TrueCFGDv4-UT", "MICEe-CFv4-UT", "CFv2-NoQ-UT", "ICSMA-UT"],
                           ordenationRestricionList=rho03,
                           yAxisTicks=yaxis1,
                           varFileNameAlias="UT")      

  multiLinePlot(figName+"10-UT2-", aliasDict, queueMeanL,variationParam="algo",
                         ordenationParam="rho",
                         restrictionParam="beta",
                         restrictionValueList=[0.01, 0.1, 1.5],
                         restrictionParam2="gamma", 
                         restrictionValueList2=[0, 2.5], 
                         variationRestrictionList=["MICE-ICSMAPURE-UT2", "MICEe-TrueCFGDv4-UT2", "MICEe-TrueCFGDv2-UT2", "MICEe-CFv4-UT2", "MICEe-CFv2-UT2",  "CFv2-NoQ-UT2", "ICSMA-UT2"],
                         ordenationRestricionList=rho03,
                         yAxisTicks=yaxis1,
                         varFileNameAlias="UT2")

  #MICE-ICSMA-UT variando gamma, fixo beta = 1.0
  multiLinePlot(figName+"11.0-UT-", aliasDict, queueMeanL,variationParam="gamma",
                           ordenationParam="rho",
                           restrictionParam="algo",
                           restrictionValueList=["MICE-ICSMAPURE-UT"],
                           restrictionParam2="beta", 
                           restrictionValueList2=[1.0],
                           yAxisTicks=yaxis3)
  #MICE-ICSMA-UT variando gamma, fixo beta = 0.1
  multiLinePlot(figName+"11.1-UT-", aliasDict, queueMeanL,variationParam="gamma",
                           ordenationParam="rho",
                           restrictionParam="algo",
                           restrictionValueList=["MICE-ICSMAPURE-UT"],
                           restrictionParam2="beta", 
                           restrictionValueList2=[0.1],
                           yAxisTicks=yaxis3)
  #MICE-ICSMA-UT variando gamma, fixo beta = 1.5
  multiLinePlot(figName+"11.2-UT-", aliasDict, queueMeanL,variationParam="gamma",
                           ordenationParam="rho",
                           restrictionParam="algo",
                           restrictionValueList=["MICE-ICSMAPURE-UT"],
                           restrictionParam2="beta", 
                           restrictionValueList2=[1.5],
                           yAxisTicks=yaxis3)  

  #MICE-ICSMA-UT2 variando gamma, fixo beta = 1.0
  multiLinePlot(figName+"12.0-UT2-", aliasDict, queueMeanL,variationParam="gamma",
                           ordenationParam="rho",
                           restrictionParam="algo",
                           restrictionValueList=["MICE-ICSMAPURE-UT2"],
                           restrictionParam2="beta", 
                           restrictionValueList2=[1.0],
                           yAxisTicks=yaxis3)
  #MICE-ICSMA-UT2 variando gamma, fixo beta = 0.1
  multiLinePlot(figName+"12.1-UT2-", aliasDict, queueMeanL,variationParam="gamma",
                           ordenationParam="rho",
                           restrictionParam="algo",
                           restrictionValueList=["MICE-ICSMAPURE-UT2"],
                           restrictionParam2="beta", 
                           restrictionValueList2=[0.1],
                           yAxisTicks=yaxis3)
  #MICE-ICSMA-UT2 variando gamma, fixo beta = 1.5
  multiLinePlot(figName+"12.2-UT2-", aliasDict, queueMeanL,variationParam="gamma",
                           ordenationParam="rho",
                           restrictionParam="algo",
                           restrictionValueList=["MICE-ICSMAPURE-UT2"],
                           restrictionParam2="beta", 
                           restrictionValueList2=[1.5],
                           yAxisTicks=yaxis3) 

  #MICE-EsMa-UT variando beta,  gamma = 2.5
  multiLinePlot(figName+"13-UT-", aliasDict, queueMeanL,variationParam="beta",
                             ordenationParam="rho",
                             restrictionParam="algo",
                             restrictionValueList=["MICEe-TrueCFGDv2-UT"],
                             restrictionParam2="gamma",
                             restrictionValueList2=[2.5],
                             yAxisTicks=yaxis1)

  #MICE-EsMa-UT2 variando beta,  gamma = 2.5
  multiLinePlot(figName+"14-UT2-", aliasDict, queueMeanL,variationParam="beta",
                             ordenationParam="rho",
                             restrictionParam="algo",
                             restrictionValueList=["MICEe-TrueCFGDv2-UT2"],
                             restrictionParam2="gamma",
                             restrictionValueList2=[2.5],
                             yAxisTicks=yaxis1)  

  #MICE-EsMa variando beta,  gamma = 2.5
  multiLinePlot(figName+"15-", aliasDict, queueMeanL,variationParam="beta",
                             ordenationParam="rho",
                             restrictionParam="algo",
                             restrictionValueList=["MICEe-TrueCFGDv2"],
                             restrictionParam2="gamma",
                             restrictionValueList2=[2.5],
                             yAxisTicks=yaxis7)
  #MICE-EsMa variando GAMMA,  BETA = 1.5
  multiLinePlot(figName+"16-", aliasDict, queueMeanL,variationParam="gamma",
                             ordenationParam="rho",
                             restrictionParam="algo",
                             restrictionValueList=["MICEe-TrueCFGDv2"],
                             restrictionParam2="beta",
                             restrictionValueList2=[1.5],
                             yAxisTicks=yaxis7)  

  #MICE-EsMa-UT variando GAMMA,  BETA = 1.5
  multiLinePlot(figName+"17-UT-", aliasDict, queueMeanL,variationParam="gamma",
                             ordenationParam="rho",
                             restrictionParam="algo",
                             restrictionValueList=["MICEe-TrueCFGDv2-UT"],
                             restrictionParam2="beta",
                             restrictionValueList2=[1.5],
                             yAxisTicks=yaxis6)  

  #MICE-EsMa-UT2 variando GAMMA,  BETA = 1.5
  multiLinePlot(figName+"18-UT2-", aliasDict, queueMeanL,variationParam="gamma",
                             ordenationParam="rho",
                             restrictionParam="algo",
                             restrictionValueList=["MICEe-TrueCFGDv2-UT2"],
                             restrictionParam2="beta",
                             restrictionValueList2=[1.5],
                             yAxisTicks=yaxis6)  
















if False and figName == "RFfiles":
  #comparação ICSMA e MICE-ICSMA
  multiLinePlot(figName+"01-", aliasDict, queueMeanL,variationParam="algo",
                         ordenationParam="rho",
                         restrictionParam="",
                         restrictionValueList="Todos",
                         restrictionParam2="gamma", 
                         restrictionValueList2=[0,2.5], 
                         variationRestrictionList=["MICE-ICSMAPURE", "ICSMA"],
                         ordenationRestricionList=rho01,
                         yAxisTicks=yaxis1)

  multiLinePlot(figName+"02-", aliasDict, queueMeanL,variationParam="algo",
                         ordenationParam="rho",
                         restrictionParam="",
                         restrictionValueList="Todos",
                         restrictionParam2="gamma", 
                         restrictionValueList2=[0,2.5], 
                         variationRestrictionList=["MICE-ICSMAPURE", "MICEe-TrueCFGDv4", "MICEe-TrueCFGDv2", "MICEe-CFv4", "MICEe-CFv2", "CFv2-NoQ"],
                         ordenationRestricionList=rho01,
                         yAxisTicks=yaxis2)

  multiLinePlot(figName+"03-", aliasDict, queueMeanL,variationParam="algo",
                         ordenationParam="rho",
                         restrictionParam="",
                         restrictionValueList="Todos",
                         restrictionParam2="gamma", 
                         restrictionValueList2=[0,2.5], 
                         variationRestrictionList=["MICE-ICSMAPURE", "MICEe-TrueCFGDv4", "MICEe-TrueCFGDv2", "MICEe-CFv4", "MICEe-CFv2",  "CFv2-NoQ"],
                         ordenationRestricionList=rho02,
                         yAxisTicks=yaxis2)


  multiLinePlot(figName+"04-", aliasDict, queueMeanL,variationParam="algo",
                         ordenationParam="rho",
                         restrictionParam="",
                         restrictionValueList="Todos",
                         restrictionParam2="gamma", 
                         restrictionValueList2=[0,2.5], 
                         ordenationRestricionList=rho01,
                         yAxisTicks=yaxis2)

  multiLinePlot(figName+"05-", aliasDict, queueMeanL,variationParam="algo",
                         ordenationParam="rho",
                         restrictionParam="",
                         restrictionValueList="Todos",
                         restrictionParam2="gamma", 
                         restrictionValueList2=[0,2.5], 
                         ordenationRestricionList=rho02,
                         yAxisTicks=yaxis2)

  multiLinePlot(figName+"06-", aliasDict, queueMeanL,variationParam="rho",
                           ordenationParam="beta",
                           restrictionParam="algo",
                           restrictionValueList=["MICE-ICSMAPURE"],
                           restrictionParam2="gamma", 
                           restrictionValueList2=[2.5],
                           variationRestrictionList=[0.9],
                           yAxisTicks=yaxis1) 

if True and figName=="RDelayed":
  multiLinePlot(figName+"01-", aliasDict, queueMeanL,variationParam="algo",
                         ordenationParam="delayT",
                         restrictionParam="algo",
                         restrictionValueList=["MICE-ICSMAPURE","ICSMA"],
                         restrictionParam2="rho", 
                         restrictionValueList2=[0.8],
                         #variationRestrictionList=None,
                         yAxisTicks=yaxis1) 
