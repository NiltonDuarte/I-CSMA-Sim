import sys

saveResultsFilePath = "../testegrid.txt"
node = sys.argv[1]

for i in range(200):
  with open(saveResultsFilePath,"a") as f:
    f.write(node+"\n")