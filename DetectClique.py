import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.approximation import clique
import operator
from networkx.algorithms import cluster

def approxrelax(G, x):

    tri = nx.triangles(G)
        
    trianglesTemp = dict(tri)


    tri = dict(trianglesTemp)
    DecG = G.copy()
    arr = []
    numTriangles = sum(tri.values())/3


    for y in range(0, G.number_of_nodes()): 
        minNodeEntry = min(tri.iteritems(), key=operator.itemgetter(1))
        minNode = minNodeEntry[0]
        minNodeNum = minNodeEntry[1]
        numTriangles -= minNodeNum
        for neighbor in DecG[minNode]:
            for neighbor2 in DecG[neighbor]:
                if minNode in DecG[neighbor2]: #triangle detected
                    tri[neighbor] -= 1 #only remove from first to avoid double counting
        DecG.remove_node(minNode)
        tri.pop(minNode)
        try:
            ratio = float(numTriangles)/float(DecG.number_of_nodes())
        except:
            ratio = 0.0
        kcompleteEdges = (DecG.number_of_nodes()*(DecG.number_of_nodes()-1))/2
        add = (minNode,ratio, kcompleteEdges, kcompleteEdges-DecG.number_of_edges(), DecG.number_of_edges())
        arr.append(add)

    for i in arr:
        if(i[4] <= x):
            break
          G.remove_node(i[0])

    return G