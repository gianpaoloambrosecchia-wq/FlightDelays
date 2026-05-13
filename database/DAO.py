from database.DB_connect import DBConnect
from model.airport import Airport
from model.tratta import Tratta


class DAO():


    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        # In quella annidata considero aeroport e compagnia area e vedo quanti voli (count) in partenza
        # o in arrivo da quell'aeroporto per quella compagnia.
        # A me serve contare il numnero di comoagnie distinte, quindi dalla tabella t
        # considero ogni aeroporto e conto il numero di righe (cioè il numero di compagnie aeree)
        query = """select *
                    from airports a
                    """

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(nMin, idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        # In quella annidata considero aeroport e compagnia area e vedo quanti voli (count) in partenza
        # o in arrivo da quell'aeroporto per quella compagnia.
        # A me serve contare il numnero di comoagnie distinte, quindi dalla tabella t
        # considero ogni aeroporto e conto il numero di righe (cioè il numero di compagnie aeree)
        query = """select t.ID, t.IATA_CODE, count(*) as N
                    from  (select a.ID, a.IATA_CODE, f.AIRLINE_ID, count(*)
                    from airports a, flights f
                    where a.ID = f.ORIGIN_AIRPORT_ID  or a.ID = f.DESTINATION_AIRPORT_ID
                    group by a.ID, a.IATA_CODE, f.AIRLINE_ID) t
                    group by t.ID, t.IATA_CODE
                    having N >= %s
                    order by N asc"""

        cursor.execute(query, (nMin,))

        for row in cursor:
            result.append(idMapA[row["ID"]])

        cursor.close()
        conn.close()
        return result


    # 1) Metodo con query semplice per trovare gli archi (gestisco le condizioni con phyton)
    @staticmethod
    def getAllEdgesV1(idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        # In quella annidata considero aeroport e compagnia area e vedo quanti voli (count) in partenza
        # o in arrivo da quell'aeroporto per quella compagnia.
        # A me serve contare il numnero di comoagnie distinte, quindi dalla tabella t
        # considero ogni aeroporto e conto il numero di righe (cioè il numero di compagnie aeree)
        query = """select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as peso
                    from flights f
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID 
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID """

        cursor.execute(query)

        for row in cursor:
            result.append(Tratta(idMapA[row["ORIGIN_AIRPORT_ID"]],
                           idMapA[row["DESTINATION_AIRPORT_ID"]],
                           row["peso"]))

        cursor.close()
        conn.close()
        return result

    # 2) Metodo con query complessa per avere direttamente gli archi, con il loro peso
    @staticmethod
    def getAllEdgesV2(idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        # Faccio la left join tra le due tabelle del DAO precdente con un join on aeroporto di partenza e di arrivo.
        # In questo modo ho affiancate le righe con stesse coppie di aeroporti. Uso la condizione
        # del where per considerare le coppie uguali come una sola e sommo i count
        # colaesce restituisce il primo valore diverso da null, quindi se t.n è null restituisce 0
        # altrimenti restituisce t1.n (serve quando per uan coppia di aeroporti c'è un volo
        # in partenza ma non in arrivo o viceversa)
        query = """select t1.origin_airport_id, t1.destination_airport_id , coalesce(t1.n,0) + coalesce(t2.n,0) as peso
                    from (select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as n
                    from flights f
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID 
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID ) t1
                    left join (select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as n
                    from flights f
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID 
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID ) t2
                    on t1.origin_airport_id = t2.destination_airport_id and t1.destination_airport_id = t2.origin_airport_id
                    where t1.origin_airport_id < t2.origin_airport_id or t2.origin_airport_id is Null"""

        cursor.execute(query)

        for row in cursor:
            result.append(Tratta(idMapA[row["origin_airport_id"]],
                           idMapA[row["destination_airport_id"]],
                           row["peso"]))

        cursor.close()
        conn.close()
        return result