from device_graph import *
from interference_graph import *
from interference_SINR_graph import *
from n_csma import *
from network_structure import *
import sys
print "Initializing sim"

LattInterfDist = 80.

windowP1 = 20
windowP2 = 8
heuristicWindowP2 = 28

  numIt = 60000
  dc = 50000
  dmax=100000
  dmin= 0
filePath = "./randomGraphs/savedGraphs/"
  saveFilePath = "../resultados/"
  fileNames = ["DevGraph16AllRandWR", "DevGraph16NPV","DevGraph16NPV_MD3_"]
