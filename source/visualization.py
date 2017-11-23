import plotly
import plotly.plotly as py
from plotly.graph_objs import *
from interference_graph import *
from device_graph import *
from access_algorithm import *
import datetime as dt
import time


print plotly.__version__                # At least 1.8.6 is required. Upgrade with: $ pip install plotly --upgrade



def plot(indx, maa, schedule, name):
  interfGraph = maa.interfGraph
  edge_trace = Scatter(
      x=[],
      y=[],
      line=Line(width=0.5,color='#888'),
      hoverinfo='none',
      mode='lines')

  for edge in interfGraph.edges:
      x0 = edge.nodes[0].sourceObj.devices[0].position[0]
      y0 = edge.nodes[0].sourceObj.devices[0].position[1]
      x1 = edge.nodes[1].sourceObj.devices[0].position[0]
      y1 = edge.nodes[1].sourceObj.devices[0].position[1]
      edge_trace['x'] += [x0, x1, None]
      edge_trace['y'] += [y0, y1, None]

  node_trace = Scatter(
      x=[],
      y=[],
      text=[],
      mode='markers+text',
      #hoverinfo='text',
      hovertext=False,
      textposition='top center',
      marker=Marker(
          showscale=False,
          colorscale='YIGnBu',
          reversescale=True,
          color=[],
          size=10,
          colorbar=dict(
              thickness=15,
              title='Node State',
              xanchor='left',
              titleside='right'
          ),
          line=dict(width=2)))

  for node in interfGraph.nodes:
      x = node.sourceObj.devices[0].position[0]
      y = node.sourceObj.devices[0].position[1]
      node_trace['x'].append(x)
      node_trace['y'].append(y)

  for node in interfGraph.nodes:
      Fv = maa.queueFunction(node.getQueueSize())
      S = maa.S(node)
      CvON = Fv*S
      CcON = -maa.g*(Fv**2)
      CvOFF = -1*S
      CcOFF = -maa.g
      st = 1 if node.state!=-1 else -1
      node_trace['marker']['color'].append(st)
      node_info = "Id:{} St:{} Q:{:10.3f}\
              <br>Fv:{:10.3f} S:{:10.3f} q:{:10.3f}\
              <br>C+:{:10.3f} Cv+:{:10.3f} Cc+:{:10.3f}\
              <br>C-:{:10.3f} Cv-:{:10.3f} Cc-:{:10.3f}".format(node.id, st, node.queueSize,Fv,S,node.q,CvON+CcON,CvON,CcON,CvOFF+CcOFF,CvOFF,CcOFF)
      node_trace['text'].append(node_info)
   
  fig = Figure(data=Data([edge_trace, node_trace]),
               layout=Layout(
                  title='<br>Interference Graph for {}'.format(name),
                  titlefont=dict(size=16),
                  showlegend=False,
                  hovermode='closest',
                  margin=dict(autoexpand=False, b=5,l=125,r=125,t=120, pad=1000),
                  annotations=[ dict(
                      text="",#"{}".format(dt.date.today().ctime()),
                      showarrow=False,
                      xref="paper", yref="paper",
                      x=0.005, y=-0.002 ) ],
                  xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                  yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))




  plotly.offline.plot(fig, filename='gitignore-graph{}.html'.format(indx))
  #plotly.offline.plot(fig, image='png', image_filename='lattice{}'.format(indx))


if __name__ == '__main__':
  name = "Lattice 4x4 "


  LattInterfDist = 80.
  LattDistance = 70.
  LattSize = 4
  LattPairDist = 40.
  beta = 0.1
  windowP1 = 20
  windowP2 = 8
  heuristicWindowP2 = 28
  r=0.5
  numIt = 10000
  plotRange = range(9990,10000)

  lattice = Lattice(LattSize,LattDistance,LattPairDist)
  interfGraph = InterferenceGraph(lattice, LattInterfDist, False)
  interfGraph.nodes.sort(key=lambda node: node.id)

  arrivalMean = {'0':0.5, '1':0.5, '2':0.5,  '3':0.5,  '4':0.5,  '5':0.5,  '6':0.5,  '7':0.5,
             '8':0.5, '9':0.5, '10':0.5, '11':0.5, '12':0.5, '13':0.5, '14':0.5, '15':0.5}

  maa = MultipleAccessAlgorithm(interfGraph, beta, 252+28,r, arrivalMean, False, True)
  maa.g=0.8
  #turnOnFunctions(self, newQF, newSF, newQP, newCP2):
  #maa.turnOnFunctions(False,False, False, False)

  #maa.turnOnFunctions(True,True, False, False)

  maa.turnOnFunctions(True,True, 'placeholder', False)
  for i in range(numIt):
    schedule = maa.runCollisionFree(1, 'v2', 4, 4)
    #schedule = maa.runICSMA(1, windowP1, windowP2)
    #schedule = maa.runHeuristicICSMA(1, heuristicWindowP2)
    if i in plotRange:
      plot(i, maa, schedule, name+str(i))