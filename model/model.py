import copy

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

        self._bestCammino = []
        self._bestScore = 0

    def getCamminoOttimo(self, v0, v1, t):
        self._bestCammino = []
        self._bestScore = 0

        parziale = [v0]

        self._ricorsione(parziale, v1, t)
        return self._bestCammino, self._bestScore

    def _ricorsione(self, parziale, v1, t):
        # Verifico se parziale è una soluzione valida, ed in caso la salvo
        # In questo caso se l'ultimo elemento di parizla è la destinazione allora
        # mi trovo davanti ad una possibile soluzione
        if parziale [-1] == v1:
            if self._getScore(parziale) > self._bestScore:
                self._bestCammino = copy.deepcopy(parziale)
                self._bestScore = self._getScore(parziale)

        # Verifico se ha senso continuare ad aggiungere elementi in parziale, oppure esco
        # La lunghezza di parziale deve essere pari al numero di tratte piu 1, perche
        # le tratte sono gli archi, parziale i nodi e se la condizione è verificata
        # allora parziale ha già raggiunto il numero massimo di tratte
        if len(parziale) == t+1:
            return

        # Ciclo sui vicini dell'ultimo nodo che ho inserito in parziale
        for n in self._graph.neighbors(parziale[-1]):
            # Se n non è già in parziale
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, v1, t)
                parziale.pop()


    # Metodo che cicla su parziale e somma i pesi degli archi
    def _getScore(self, parziale):
        sumPesi = 0
        for i in range(0, len(parziale)-1):
            sumPesi += self._graph[parziale[i]][parziale[i+1]]['weight']

        return sumPesi


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

    # Metodo per trovare i vicini di un nodo (ordinati in base al peso dell'arco)
    def getViciniOrdinati(self, source):
        vicini = self._graph.neighbors(source)
        viciniT = []
        # Creo una lista di tuple con primo elemento il vicino
        # e secondo elemento l'arco che collega source al vicino v
        for v in vicini:
            viciniT.append((v, self._graph[source][v]['weight']))

        # Ordino la lista in base al secondo elemento della tupla (ovvero il peso)
        viciniT.sort(key=lambda x: x[1], reverse = True)
        return viciniT


    # Metodo che ritorna True se esiste un cammino tra v0 e v1
    def hasPath(self, v0, v1):
        # Metodo che dice il set di nodi della componente connessa del grafo che contiene v0
        if v1 in nx.node_connected_component(self._graph, v0):
            return True
        else:
            return False

    # Metodo per trovare il percorso tra due nodi
    def getPath(self, v0, v1):
        # Esplorazione bfs (tende a cercare i cammini minimi in termine di numeri di archi)
        # Ho un dizionario con chiave il nodo e valore il predecessore nell'albero di visita bfs
        dictOfPredecessors = dict(nx.bfs_predecessors(self._graph, v0))

        # AGgiungo il nodo v1 alla lista (il percorso)
        path = [v1]
        # Fino a quando non aggiungo v0 alla lista, inserisco in posizione 0
        # il predecessore del nodo
        while path[0] != v0:
            path.insert(0, dictOfPredecessors[path[0]])

        # In sostanza vado a ritroso, partendo da v1 analizzando tutti i predecessori
        # fino ad arrivare a v0


        # RICORDA!!! Posso fare la stessa cosa con dfs ma, esplorando in profondità,
        # ha cammini più lunghi

        # OPPURE, ho i metodi che mi danno il cammino minimo ( per quanto riguarda il peso) del grafo minimo tra v0 e v1
        path2 = nx.shortest_path(self._graph, v0, v1)
        path3 = nx.dijkstra_path(self._graph, v0, v1)
        # Se in nx.dijkstra_path(self._graph, v0, v1, weight = None) aggiungo l'ultimo argomento
        # allora cerca il cammino minimo non sul peso ma sul numero di archi

        return path3


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)


    def getAllNodes(self):
        nodes = list(self._graph.nodes)
        nodes.sort(key = lambda n: n.IATA_CODE)
        return nodes

