from operator import itemgetter
import os, math
import matplotlib.pyplot as plt
import numpy as np

class AnalisiFrequenze:

    # inizializzo gli attributi
    def __init__(self) -> None:
        self.filename = os.getcwd() + "/1_set_es/Istogrammi/moby.txt"
        self.txt = self._get_moby_txt()

    # creo l'istogramma
    def histogram(self) -> None:
        labels = [
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
        self._plot(labels, self._get_occurrences())

     # creo gli m istogrammi per gli m-grammi
    def m_histograms(self, m) -> None:
        # dizionario che tiene traccia delle occorrenze dei blocchi di lettere 
        # chiave = blocco, valore = # occorrenze
        self.m_blocks = self._create_dictionary_for_occurrences(m)
        
        # scelgo quanti elementi plottare, altrimenti si sovrapporrebbero
        if m == 1:
            n = 26
        elif m == 2:
            n = 70
        elif m == 3:
            n = 45
        elif m == 4:
            n = 35

        # creo un nuovo dizionario con i primi n valori
        # ordinati in maniera descrescente
        new_m_blocks = dict(sorted(self.get_dict_items(), key=itemgetter(1), reverse=True)[:n])
        # e li plotto
        self._plot(new_m_blocks.keys(), new_m_blocks.values())

    # calcolo l'indice di coincidenza
    def coincidence_index(self) -> float:
        ic = 0
        for key in self.get_dict_keys():
            occurrences = self.get_dict_value_from_key(key)
            ic += (occurrences * (occurrences-1))

        N = self._calculate_all_occurrences()
        ic = ic / (N*(N-1))
        return ic

    # calcolo l'Entropia di Shannon
    def shannon_entropy(self) -> float:
        entropy = 0
        N = self._calculate_all_occurrences()
        for key in self.get_dict_keys():
            entropy += (self.get_dict_value_from_key(key)/N) * math.log2(self.get_dict_value_from_key(key)/N)
        entropy *= (-1)
        return entropy

    def get_filename(self) -> str:
        return self.filename
    
    def get_txt(self) -> str:
        return self.txt
    
    def get_dict_items(self):
        return self.m_blocks.items()
    
    def get_dict_keys(self):
        return self.m_blocks.keys()
    
    def get_dict_value_from_key(self, key) -> int:
        return self.m_blocks.get(key)
    
    def _get_dict_values(self):
        return self.m_blocks.values()
    
    # sommo tutte le occorrenze
    def _calculate_all_occurrences(self) -> int:
        return sum(self._get_dict_values())

    # creo il plot
    def _plot(self, x, height) -> None:
        plt.bar(x, height)
        plt.show()

    # creo un dizionario con chiave il blocco di lettere
    # e valore il numero di occorrenze nel testo
    def _create_dictionary_for_occurrences(self, m) -> dict:
        m_blocks = {}
        start = 0
        finish = m
        while True:
            m_block = self.get_txt()[start:finish]
            # ho scorso tutto il testo -> esco
            if m_block == "":
                break
            # se il blocco è presente -> incremento l'occorrenza
            if m_block in m_blocks:
                m_blocks.update({m_block: m_blocks[m_block] + 1})
            # altrimenti lo aggiungo e l'occorrenza la imposto a 1
            else:
                if len(m_block) == m:
                    m_blocks.update({m_block: 1})

            start = finish
            finish += m
        return m_blocks

    # rimuovo i caratteri non presenti in Z26
    def _remove_chars(self, txt) -> None:
        moby = ""
        for chr in txt:
            i_chr = ord(chr)
            if i_chr >= 97 and i_chr <= 122:
                moby += chr
        return moby

    # vado a leggere il file di Moby Dick
    def _get_moby_txt(self) -> None:
        txt = ""
        with open(file=self.get_filename(), mode="r", encoding="utf8") as f:
            # leggo e setto il lowercase
            txt = f.read().lower()
        return self._remove_chars(txt)

    # calcolo le occorrenze
    def _get_occurrences(self):
        # inizializzo il vettore delle occorrenze a 0
        occurrences = np.zeros(shape=26, dtype=int)
        for chr in self.get_txt():
            # converto il carattero in numero
            chr = ord(chr)
            # incremento il valore nella posizione associata alla lettera
            # es: oc[0=a], oc[1=b], ...
            occurrences[chr-97] += 1
        return occurrences

def main():
    an_freqs = AnalisiFrequenze()
    
    # istogramma
    an_freqs.histogram()

    # 1-gramma e relativo IC ed entropia
    an_freqs.m_histograms(1)
    print("IC - M = 1: ", an_freqs.coincidence_index())
    print("Entropia - M = 1: ", an_freqs.shannon_entropy())

    # 2-gramma e relativo IC ed entropia
    an_freqs.m_histograms(2)
    print("IC - M = 2: ", an_freqs.coincidence_index())
    print("Entropia - M = 2: ", an_freqs.shannon_entropy())

    # 3-gramma e relativo IC ed entropia
    an_freqs.m_histograms(3)
    print("IC - M = 3: ", an_freqs.coincidence_index())
    print("Entropia - M = 3: ", an_freqs.shannon_entropy())

    # 4-gramma e relativo IC ed entropia
    an_freqs.m_histograms(4)
    print("IC - M = 4: ", an_freqs.coincidence_index())
    print("Entropia - M = 4: ", an_freqs.shannon_entropy())

if __name__ == '__main__':
    main()