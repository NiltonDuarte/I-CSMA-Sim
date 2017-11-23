import plotly
import plotly.plotly as py
from plotly.graph_objs import *
from interference_graph import *
from device_graph import *
import datetime as dt
import time


print plotly.__version__                # At least 1.8.6 is required. Upgrade with: $ pip install plotly --upgrade

filePath = "./randomGraphs/savedGraphs/"
fileNames = ["DevGraph16AllRandWR", "DevGraph16NPV","DevGraph16NPV_MD3_"]
name = fileNames[2]
nameIdx=22

LattInterfDist = 80.
LattDistance = 70.
LattSize = 4
LattPairDist = 40.

rt = RandomTopology()
rt.load(filePath+name+str(nameIdx)+".csv")
interfGraph = InterferenceGraph(rt, LattInterfDist, False)
interfGraph.nodes.sort(key=lambda node: node.id)

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
    mode='markers',
    hoverinfo='text',
    marker=Marker(
        showscale=True,
        # colorscale options
        # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
        # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
        colorscale='YIGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
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
    adjacencies = interfGraph.getNeighbours(node)
    node_trace['marker']['color'].append(len(adjacencies))
    node_info = '# de vizinhos: '+str(len(adjacencies))+' id: '+str(node.id)
    node_trace['text'].append(node_info)

fig = Figure(data=Data([edge_trace, node_trace]),
             layout=Layout(
                title='<br>Interference Graph for {}{}'.format(name,nameIdx),
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="{}".format(dt.date.today().ctime()),
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))




plotly.offline.plot(fig, filename='reference-graph.html')