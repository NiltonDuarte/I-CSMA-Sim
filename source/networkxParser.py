import networkx as nx
from interference_graph import *
from device_graph import *

class NxGraph:
	def __init__(self):
		self.graph = None
		pass

	def importInterferenceGraph(self, ig):
		self.graph = nx.Graph()
		for node in ig.nodes:
			self.graph.add_node(node.id)
		for edge in ig.edges:
			self.graph.add_edge(edge.nodes[0].id, edge.nodes[1].id)

	def nodes(self):
		return self.graph.nodes()

	def edges(self):
		return self.graph.edges()

if __name__ == '__main__':
	filePath = "./randomGraphs/savedGraphs/"
	fileNames = ["DevGraph16AllRandWR", "DevGraph16NPV","DevGraph16NPV_MD3_"]
	name = fileNames[1]
	nameIdx=10

	LattInterfDist = 80.
	LattDistance = 70.
	LattSize = 4
	LattPairDist = 40.

	rt = RandomTopology()
	rt.load(filePath+name+str(nameIdx)+".csv")
	interfGraph = InterferenceGraph(rt, LattInterfDist, False, LattDistance*(LattSize), LattDistance*(LattSize))
	interfGraph.nodes.sort(key=lambda node: node.id)
	nxg = NxGraph()
	nxg.importInterferenceGraph(interfGraph)
	print len(interfGraph.edges)
	print nxg
	print len(nxg.nodes()), nxg.nodes()
	print len(nxg.edges()), nxg.edges()
