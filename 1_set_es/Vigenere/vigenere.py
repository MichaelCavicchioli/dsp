import math, collections
from collections import Counter
import numpy as np

class Vigenere:

    # inizializzo l'attributo
    def __init__(self) -> None:
        self.ct = "ZYIVIUPYKFJZLKRRIFVJMTGBLTSAVYEPXFWYIJTU"\
        "KSSXHKRJOKLKEYEBTVQGRCAYQVHYXXAVMYXGXNIZVRYRWZOBJ"\
        "YMYKXOHTUETHLOHTULOQYEYLGYYLKDVTKSGDUNRUWMTGXENYZ"\
        "RMZOSPUJMZCZHRGZVGVUUAJYMSFKCBSZRMTGIALLPRCANLOVPJ"\
        "MTGOKWSXINEFRZTVIJFEKVXUSTEFOUIZLKSRTJIZLGTQOJGUZK"\
        "RVTXECEETBHIIGGNTUOJFGVXIRXNSAPJSBSVLUARIOKIEZINIZ"\
        "CRWISSPRRCMTKHUGNVOTICIGCRWGFYUEJVZKROFUKUMJJONQGW"\
        "PGAONGNVTXSMRNSNLOGNEAGSPKHNIZZFFXIGKGNISAKNHRQEIC"\
        "LKDTGZRTSZHVTXFAXJEPXVEYMTGYEIIGPOSGOTWAVXOHTUMTKY"\
        "TUKIIISXDVTXGUYRDBTCCISTTNOEGUQVLRZVMTJURZGKMURLOEV"\
        "FMTXYOSBZICAOTUOEEIIXTNOEJOROTRFFRKERLGNVVKAGSGUVWI"\
        "EVEGUNEYEXETOFRCLKRRNZWBMKWBLKLKGOTLCFYRHHESACPUJJI"\
        "FZFVZMUNFGEHUQOSFOFRYETDJULPJIBEAZLERPEFNJVXUFRAPQY"\
        "IYXKPCKUFGGQFEUDXNIIOETVVNERFQOJTOVOTRJYERJGMHYVHCL"\
        "GTUGULKLUPRJKSLMTDNJFSXEZTUKVHMIUFGNVQUHKLZGIOKHKXV"\
        "ZKLXSAGUCYMILNEPULPJAGLXULXORZOEKRPOXE".lower()    

    # calcolo e stampo a schermo le ripetizioni di ogni trigramma
    # ottenuto con sovrapposizione
    def repetitions(self) -> None:  
        ct = self.get_ct()
        self.repetitions_dict = {}
        n = 3  
        start = 0
        finish = n    

        iterations = len(ct) - n + 1
        while iterations > 0:
            # considero trigrammi, ma mi muovo di 1 carattere alla volta
            trigram = ct[start : finish]   
            # creo un dizionario che ha per chiavi i trigrammi
            # e per valori il rispettivo numero di ripetizioni nel testo
            self.get_repetitions_dict().update({trigram: self.get_repetitions_dict().get(trigram, 0) + 1})
            start += 1
            finish += 1 
            iterations -= 1

        # creo un dizionario simile al precedente, ma solo per trigrammi
        # che hanno più di una ripetizione
        self.trigram_dict_with_one_more_than_one_repetition = {} 
        for trigram, repetitions in self.get_repetitions_dict().items():
            # la prima non conta come ripetizione
            if repetitions >= 2:
                self.get_trigram_dict_with_one_more_than_one_repetition().update({trigram: repetitions})

        print("Tutte le ripetizioni:", self.get_repetitions_dict(), "\n")        
        print("Ripetizioni (caso con ripetizioni > 1):", self.get_trigram_dict_with_one_more_than_one_repetition(), "\n")

    # calcolo e stampo a schermo le distanze di ogni trigramma
    def distances(self) -> None:
        # creo un dizionario che ha per chiavi i trigrammi
        # e per valori le rispettive posizioni nel testo
        self._ceate_trigrams_positions_dict()

        # creo un dizionario che ha per chiavi i trigrammi
        # e per valori le rispettive distanze dagli altri trigrammi uguali
        self.trigrams_distances_dict = {}
        for trigram, positions in self.get_trigrams_positions_dict().items():  
            distances = [positions[i] - positions[i - 1] for i in range(1, len(positions))]   
            self.get_trigrams_distances_dict().update({trigram: distances})
        
        print("Distanze:", self.get_trigrams_distances_dict(), "\n")

    # calcolo i possibili valori di m tramite il metodo di Kasiski
    def m_values(self) -> None:     
        # creo un dizionario che ha per chiavi i trigrammi
        # e per valori il rispettivo MCD ottenuto dalle distanze
        self._create_trigrams_dict_with_gcd()

        already_seen_m = []
        trigrams_gcd_dict = self.get_trigrams_gcd_dict()
        for key in trigrams_gcd_dict.keys():

            # ottengo m
            m = trigrams_gcd_dict.get(key)
            
            # se non l'ho già visto, allora lo aggiungo alla lista dei possibili m
            if already_seen_m.count(m) == 0:
                already_seen_m.append(m)
        
        # ordino la lista e la printo
        already_seen_m.sort()
        print("I valori possibili di m sono (senza ripetizioni):", already_seen_m, "\n")
        
        # stampo a schermo quello più comune
        gcd_frequencies = collections.Counter(trigrams_gcd_dict.values())   
        print("L'm più comune è:", [gcd for gcd, _ in gcd_frequencies.most_common(1)], "\n")

    # trovo l'm corretto e i rispettivi indici di coincidenza
    def correct_m_and_coincidences_indexes(self) -> None:
        # definisco un valore altissimo per la deviazione minima
        # solo per riutilizzarlo in seguito
        min_deviation = 1000000000

        best_indexes = []
        # provo tutte le chiavi tra [2,16)
        for key in range(2, 16):
            # ottengo il testo codificato in base al valore della chiave
            encoded_txts = self._get_encoded_txt_with_same_rotation_key(key)

            # ottengo gli indici di coincidenza per il testo codificato
            indexes = [self._get_coincidence_index(encoded_txt) for encoded_txt in encoded_txts]        
            
            # calcolo la deviazione
            deviation = math.sqrt(sum((coincidence_index - 0.065) ** 2 for coincidence_index in indexes) / key)  
            
            # salvo il valore migliore della chiave e dell'indice di coincidenza
            # aggiornando anche il valore minimo della deviazione
            if deviation < min_deviation:   
                self._set_best_key(key)   
                min_deviation = deviation   
                best_indexes = indexes   

        print("Miglior chiave tramite gli IC:", self.get_best_key(), "\n")
        print("Valori degli IC:", best_indexes, "\n")
    
    # calcolo la chiave
    def calculate_key(self) -> None:
        # ottengo il testo codificato in base al valore migliore della chiave
        encoded_txts = self._get_encoded_txt_with_same_rotation_key(self.get_best_key())   

        # definisco l'alfabeto
        letters = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z"
        ]

        # definisco il vettore contenente le frequenze della lingua inglese
        eng_frequencies = np.array([0.08167, 0.01492, 0.02782, 0.04253, 
                            0.12702, 0.02228, 0.02015, 0.06094, 0.06966,
                            0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
                            0.07507, 0.01929, 0.00095, 0.05987, 0.06327,
                            0.09056, 0.02758, 0.00978, 0.02360, 
                            0.00150, 0.01974, 0.00074]) 

        self.key = ""
        for encoded_txt in encoded_txts:
            # calcolo tutte le occorrenze
            occurrences = Counter(encoded_txt)   
            # crea un vettore contenente le occorrenze di tutte le lettere presenti nel testo
            occurrences = [occurrences.get(letter, 0) for letter in letters]  
            
            # totale delle occorrenze
            N = sum(occurrences)   
            
            # calcolo le frequenze
            frequencies = np.array([occurrence/N for occurrence in occurrences]) 
            Mg = 0
            key_letter = ""
            
            # calcolo lo shift migliore 
            for g in range(26):
                # moltiplico le frequenze inglesi per le frequenze delle lettere, applicando lo shift 
                Mg_temp = np.dot(eng_frequencies, np.roll(frequencies, -1 * g))   
            
                # mi salvo lo shift che massimizza il prodotto scalare
                if Mg_temp > Mg:   
                    key_letter = chr(g + 97)   
                    Mg = Mg_temp
            
            print("Lettera della chiave: ", key_letter, "\n")
            print("Prodotto scalare: ", Mg, "\n")
            
            # salvo la chiave
            self._set_key(key_letter)
        
        print("La chiave è:", self.get_key(), "\n")

    # eseguo la decryption tramite la chiave e il CT
    def decryption(self) -> None:
        key = [ord(chr) for chr in self.get_key()]
        ct = [ord(chr) for chr in self.get_ct()]

        plain_txt = ""
        for i in range(len(ct)):
            plain_txt += chr(((ct[i] - key[i % len(key)]) % 26) + 97)
        
        print("Il PT è:", plain_txt)

    def get_trigrams_gcd_dict(self) -> dict:
        return self.trigrams_gcd_dict

    def get_ct(self) -> str:
        return self.ct

    def get_repetitions_dict(self) -> dict:
        return self.repetitions_dict

    def get_trigram_dict_with_one_more_than_one_repetition(self) -> dict:
        return self.trigram_dict_with_one_more_than_one_repetition

    def get_trigrams_distances_dict(self) -> dict:
        return self.trigrams_distances_dict

    def get_trigrams_positions_dict(self) -> dict:
        return self.trigrams_positions_dict

    def get_best_key(self) -> int:
        return self.best_key
    
    def get_key(self) -> str:
        return self.key

    def _set_key(self, new_key) -> chr:
        self.key += new_key
    
    def _set_best_key(self, best_key) -> None:
        self.best_key = best_key

    # creo un dizionario che ha per chiavi i trigrammi che hanno più di una ripetizione
    # e per chiavi le rispettive posizioni nel testo
    def _ceate_trigrams_positions_dict(self) -> None:   
        ct = self.get_ct()
        self.trigrams_positions_dict = {} 

        for trigram, repetitions in self.get_trigram_dict_with_one_more_than_one_repetition().items():
            positions = []
            position = 0 
            
            # cerco e salvo tutte le posizioni dei trigrammi
            while repetitions > 0:
                position = ct.find(trigram, position)
                positions.append(position)
                repetitions -= 1
                position += 1
            
            # aggiorno i valori nel dizionario
            self.trigrams_positions_dict.update({trigram: positions})

    # creo un dizionario che ha per chiavi i trigrammi
    # e per valori il rispettivo MCD del trigramma in base alle distanze
    def _create_trigrams_dict_with_gcd(self) -> None:   
        self.trigrams_gcd_dict = {}  
        for trigram, distances in self.get_trigrams_distances_dict().items():   
            gcd = distances[0]
    
            # calcolo l'MCD
            for distance in distances:
                gcd = math.gcd(gcd, distance)
    
            # aggiorno i valori del dizionario
            self.get_trigrams_gcd_dict().update({trigram: gcd})

    # metodo per calcolare l'indice di coincidenza
    def _get_coincidence_index(self, txt):   
        # creo un dizionario temporaneo che ha per chiavi i trigrammi
        # e per valori le rispettive occorrenze dei trigrammi uguali nel testo
        occurrences_chars_dict = {}  
        for chr in txt: 
            occurrences_chars_dict.update({chr: (occurrences_chars_dict.get(chr, 0) + 1)})
        
        # calcolo l'indice di coincidenza
        coincidence_index = 0
        for key in occurrences_chars_dict.keys():
            occurrences = occurrences_chars_dict.get(key) 
            coincidence_index += (occurrences * (occurrences - 1))
        
        N = (len(txt) * (len(txt)- 1))
        coincidence_index /= N
        return coincidence_index

    # creo un vettore di 'key' celle e in ogni cella inserisco un carattere alla volta.
    # quando ho inserito i primi 'key' valori, riparto dalla prima cella e così via
    # fino a quando non concludo il testo 
    def _get_encoded_txt_with_same_rotation_key(self, key):
        encoded_txt = ["" for _ in range(key)]  
        for i, chr in enumerate(self.get_ct()): 
            encoded_txt[i % key] += chr

        return encoded_txt
    
def main():
    v = Vigenere()

    # ripetizioni
    v.repetitions()

    # distanze
    v.distances()

    # valori di m
    v.m_values()

    # indici di coincidenza
    v.correct_m_and_coincidences_indexes()

    # chiave
    v.calculate_key()

    # decifratura
    v.decryption()
    
if __name__ == '__main__':
    main()