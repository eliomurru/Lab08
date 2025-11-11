from database.impianto_DAO import ImpiantoDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()

    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        try:
            tuple_consumo_impianto = list()
            for impianto in self._impianti:
                consumi = impianto.get_consumi()
                if consumi:
                    consumi_mensili = list()
                    for consumo in consumi:
                        if str(consumo.data)[5:7] == f"{mese:02d}":
                            consumi_mensili.append(consumo.kwh)
                    media = sum(consumi_mensili) / len(consumi_mensili)
                else:
                    media = 0
                tuple_consumo_impianto.append((impianto.nome, media))
            return tuple_consumo_impianto
        except Exception as e:
            print(e)
            return None

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        # Condizione terminale
        if giorno > 7:
            if costo_corrente < self.__costo_ottimo or self.__costo_ottimo == -1:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = sequenza_parziale.copy()
            return

        # Loop sugli impianti disponibili
        for impianto_id, consumi in consumi_settimana.items():
            costo_giorno = consumi[giorno-1]
            # aggiungi costo di spostamento se diverso dall'ultimo impianto
            if ultimo_impianto is not None and ultimo_impianto != impianto_id:
                costo_giorno += 5  # costo fisso di spostamento

            # Aggiorna sequenza parziale
            sequenza_parziale.append(impianto_id)

            # Ricorsione giorno successivo
            self.__ricorsione(sequenza_parziale, giorno + 1, impianto_id, costo_corrente + costo_giorno,
                              consumi_settimana)

            # Backtracking
            sequenza_parziale.pop()

    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: dict {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        try:
            consumi_settimana = dict()
            for impianto in self._impianti:
                consumi = impianto.get_consumi()
                giorn = [0] * 7
                for c in consumi:
                    data_str = str(c.data)
                    mese_corrente = int(data_str[5:7])
                    giorno = int(data_str[8:10])
                    if mese_corrente == mese and 1 <= giorno <= 7:
                        giorn[giorno - 1] = c.kwh
                consumi_settimana[impianto.id] = giorn
            return consumi_settimana
        except Exception as e:
            print(e)
            return None

