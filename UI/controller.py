import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._choiceArrivo = None
        self._choicePartenza = None

    def handleAnalizza(self, e):
        cMin = self._view._txtInCMin.value
        if cMin=="":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserire un valore per il numero minimo di compagnie", color="red")
            )
            self._view.update_page()
            return
        try:
            cMinInt = int(cMin)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserisci un valore intero per il numero minimo di compagnie", color="red")
            )
            self._view.update_page()
            return

        if cMinInt <= 0:
            self._view.txt_results.control.clear()
            self._view.txt_results.control.append(
                ft.Text("Inserisci un valore intero positivo per il numero minimo di compagnie", color="red")
            )
            self._view.update_page()
            return

        self._model.buildGraph(cMinInt)

        allNodes = self._model.getAllNodes()
        self._fillDropdown(allNodes)
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("Grafo correttamente creato", color="green")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo contiene {nNodes} nodi e {nEdges} archi")
        )
        self._view.update_page()



    def handleConnessi(self, e):
        if self._choicePartenza is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Seleziona un eroporto di partenza", color="red")
            )
            self._view.update_page()
            return
        viciniT = self._model.getViciniOrdinati(self._choicePartenza)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"I vicni del nodo {self._choicePartenza} sono: ")
        )
        for v in viciniT:
            self._view.txt_result.controls.append(
                ft.Text(f"{v[0]} - peso {v[1]}")
            )
        self._view.update_page()
        return

    def handleTestConnessione(self, e):
        if self._choicePartenza is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Seleziona un aeroporto di partenza", color="red")
            )
            self._view.update_page()
            return
        if self._choiceArrivo is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Seleziona un aeroporto di arrivo", color="red")
            )
            self._view.update_page()
            return

        if not self._model.hasPath(self._choicePartenza, self._choiceArrivo):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Non esiste un cammino tra {self._choicePartenza} e {self._choiceArrivo}")
            )
            self._view.update_page()
            return


        path = self._model.getPath(self._choicePartenza, self._choiceArrivo)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Esiste un cammino tra {self._choicePartenza} e {self._choiceArrivo}:")
        )
        for p in path:
            self._view.txt_result.controls.append(
                ft.Text(p)
            )

        self._view.update_page()
        return


    def handleCerca(self, e):
        t = self._view._txtInNtratteMax.value
        if t == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserisci un valore nel campo tratte", color="red")
            )
            self._view.update_page()
            return

        try:
            tInt = int(t)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserisci un valore intero nel campo tratte",color="red")
            )
            self._view.update_page()
            return

        if self._choicePartenza is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Seleziona un aeroporto di partenza", color="red")
            )
            self._view.update_page()
            return
        if self._choiceArrivo is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Seleziona un aeroporto di arrivo", color="red")
            )
            self._view.update_page()
            return

        path, score = self._model.getCamminoOttimo(self._choicePartenza, self._choiceArrivo, tInt)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Cammino tra {self._choicePartenza} e {self._choiceArrivo} trovato")
        )
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Il cammino ha uno score complessivo di {score} e contiene i seguenti nodi:")
        )

        for p in path:
            self._view.txt_result.controls.append(
                ft.Text(p)
            )
        self._view.update_page()
        return


    def _fillDropdown(self, allNodes):
        for n in allNodes:
            # Aggiungo l'oggetto n (Aeroporto) e on_click è il meotod attivato quando
            # seleziono un aeroporto
            self._view._ddAeroportoP.options.append(
                ft.dropdown.Option(data = n,
                                   key = n.IATA_CODE,
                                   on_click = self._choiceDdPartenza)
            )
            self._view._ddAeroportoA.options.append(
                ft.dropdown.Option(data=n,
                                   key=n.IATA_CODE,
                                   on_click=self._choiceDdArrivo)
            )

        self._view.update_page()


    def _choiceDdPartenza(self, e):
        # Salva nella variabile self._choicePartenza l'oggetto Aeroporto selezionato
        self._choicePartenza = e.control.data
        print(f"Hai scelto come aeroporto di partenza: {self._choicePartenza}")

    def _choiceDdArrivo(self, e):
        # Salva nella variabile self._choicePartenza l'oggetto Aeroporto selezionato
        self._choiceArrivo = e.control.data
        print(f"Hai scelto come aeroporto di partenza: {self._choiceArrivo}")


