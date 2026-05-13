from model.model import Model

# TESTIAMO IL MODELLO

# 1) Crea istanza del modello
myModel = Model()

# 2) Creo il grafo
myModel.buildGraph(5)
#Printo numero nodi e archi del grafo
nNodes,nEdges = myModel.getGraphDetails()
print(f"Num nodes: {nNodes}, num edges: {nEdges}")