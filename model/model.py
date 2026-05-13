import networkx as nx

from database.DAO import DAO



class Model:
    def __init__(self):
        self._graph = nx.Graph()
        # In questo caso i nodi non sono tutti gli aeroporti ma la idMap
        # va costruita a partire da tutti gli aeroporti (anche quelli che non sono nodi)
        self._airports = DAO.getAllAirports()
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a

    def buildGraph(self, nMin):
        nodes = DAO.getAllNodes(nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        self.addEdgesV2()

    def addEdgesV1(self):
        allTratte = DAO.getAllEdgesV1(self._idMapAirports)
        # Queste tratte hanno due problemi:
        #   1) ho archi da A a B e da B ad A
        #   2) ho archi fra aeroporti che avevo filtrato (cioè che non sono nodi del grafo)

        for t in allTratte:
            # Controllo se i due aeroporti della tratta fanno parte del grafo (cioè sono nodi del grafo)
            if t.aeroportoP in self._graph and t.aeroportoD in self._graph:
                # Se il grafo ha già l'arco allora incremento il peso, altrimenti creo l'arco
                if self._graph.has_edge(t.aeroportoP, t.aeroportoD):
                    self._graph[t.aeroportoP][t.aeroportoD]['weight'] += 1
                else:
                    self._graph.add_edge(t.aeroportoP, t.aeroportoD, weight = t.peso)


    def addEdgesV2(self):
        allTratte = DAO.getAllEdgesV2(self._idMapAirports)
        # Queste tratte hanno un problema:
        #   2) ho archi fra aeroporti che avevo filtrato (cioè che non sono nodi del grafo)

        for t in allTratte:
            # Controllo se i due aeroporti della tratta fanno parte del grafo (cioè sono nodi del grafo)
            if t.aeroportoP in self._graph and t.aeroportoD in self._graph:
                self._graph.add_edge(t.aeroportoP, t.aeroportoD, weight = t.peso)



    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)


    def getAllNodes(self):
        nodes = list(self._graph.nodes)
        nodes.sort(key = lambda n: n.IATA_CODE)
        return nodes

