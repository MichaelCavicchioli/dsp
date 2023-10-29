from itertools import combinations
import math
import numpy as np

class Attacker:

    # inizializzo gli attributi
    def __init__(self, pt, ct, block_dim) -> None:
        self.pt, self.ct, self.block_dim = pt, ct, block_dim

    # eseguo l'attacco
    def attack(self) -> None:
        print("Attack...")
        # mi salvo i valori del PT e del CT per testare
        # successivamente i risultati
        pt_test = self.get_pt()
        ct_test = self.get_ct()
        
        # PT e CT vengono trasformati di dimensione pari 
        # alla dimensione del blocco di lettere  
        self._create_block_matrix()

        # creo tutte le possibili combinazioni di PT e CT
        pt_combinations = list(combinations(self.get_pt(), self.get_block_dim()))
        ct_combinations = list(combinations(self.get_ct(), self.get_block_dim()))

        finished = False

        # provo tutte le possibili combinazioni di PT e CT per trovare la chiave 
        for ct_combination in ct_combinations:
            for pt_combination in pt_combinations:
                # calcolo P*^(-1)
                inverse_p_star = self._get_inverse_matrix(pt_combination)
                # se l'ho trovata
                if inverse_p_star is not None:
                    # calcolo K
                    self.K = np.matmul(np.array(ct_combination).T, np.array(inverse_p_star).T)%26
                    # dato il PT, genero il CT tramite K e PT
                    generated_ct = self._confirmation(pt_test)
                    # se il CT generato è uguale a quello che l'attaccante ha visto
                    if np.array_equal(generated_ct, ct_test):
                        # ho trovato la chiave K
                        print("C*:", np.array(ct_combination).T)
                        print("P*:", np.array(pt_combination).T)
                        print("P*^(-1):", np.array(inverse_p_star).T)
                        print("K:", np.array(self.get_K()))
                        print("Confirmation -> CT:\n", generated_ct)                    
                        finished = True
                        break
            if finished: break

    def get_pt(self) -> str:
        return self.pt
    
    def get_ct(self) -> str:
        return self.ct

    def get_block_dim(self) -> int:
        return self.block_dim
    
    def get_K(self):
        return self.K

    def _set_pt(self, new_pt) -> None:
        self.pt = new_pt
    
    def _set_ct(self, new_ct) -> None:
        self.ct = new_ct

    # calcolo il determinante    
    def _get_determinant(self, A):
        return round((np.linalg.det(A))%26)

    # sostituisco i caratteri con i numeri, sia per il PT, che per il CT
    def _replace_chars_with_nums(self) -> None:
        self._set_pt(self._replace(self.get_pt()))
        self._set_ct(self._replace(self.get_ct()))

    def _replace(self, txt) -> list:
        dict = {
            "a": "0",
            "b": "1",
            "c": "2",
            "d": "3",
            "e": "4",
            "f": "5",
            "g": "6",
            "h": "7",
            "i": "8",
            "j": "9",
            "k": "10",
            "l": "11",
            "m": "12",
            "n": "13",
            "o": "14",
            "p": "15",
            "q": "16",
            "r": "17",
            "s": "18",
            "t": "19",
            "u": "20",
            "v": "21",
            "w": "22",
            "x": "23",
            "y": "24",
            "z": "25",
        }
        message_list = []
        for chr in txt:
            message_list.append(int(chr.replace(chr, dict[chr])))
        return message_list
    
    # calcolo il CT tramite la chiave K ed il PT
    def _confirmation(self, pt):
        generated_txt = [0 for _ in range(len(pt))]

        start, index = 0, 0
        finish = self.get_block_dim()
        block_dim = self.get_block_dim()

        iterations = len(generated_txt) // block_dim
        while iterations > 0:
            # mi muovo di n caratteri alla volta
            array = pt[start:finish] 
            
            for j in range(block_dim):
                # moltiplico la riga j-esima di K per l'i-esimo PT 
                generated_txt[index] = np.matmul(self.get_K()[j], array)%26 
                index += 1
            
            start += block_dim
            finish += block_dim
            iterations -= 1
    
        return generated_txt

    # calcolo la mtrice inversa
    def _get_inverse_matrix(self, A):
        # ottengo il determinante della matrice
        determinant = self._get_determinant(A)

        # non esiste la matrice invertibile perchè A e 26 non sono coprimi
        if math.gcd(determinant, 26) != 1: return None

        # inizializzo la matrice inversa con tutti 0
        cols = self.get_block_dim()
        rows = self.get_block_dim()
        inverse_matrix = [[0 for _ in range(cols)] for _ in range(rows)]
        
        # calcolo l'inverso del determinante
        inverse_determinant = self._get_inverse_determinant(determinant)

        if inverse_determinant == None:
            raise Exception("Matrix has not inverse determinant.")

        # applico la formula di Cramer per calcolare la matrice inversa
        for i in range(0, rows):
            for j in range(0, cols):
                Aji = self._get_matrix_with_no_j_row_i_col(A, j, i)
                Aji_determinant = self._get_determinant(Aji)
                inverse_matrix[i][j] = ((-1)**(i+j)*Aji_determinant*inverse_determinant)%26

        return np.array(inverse_matrix)

    # calcolo l'inverso del determinante
    def _get_inverse_determinant(self, determinant) -> int:
        determinant = determinant % 26
        for x in range(1, 26):
            if (determinant * x) % 26 == 1:
                return x
        return None  # nessun inverso

    # elimino la riga j e la colonna i dalla matrice
    def _get_matrix_with_no_j_row_i_col(self, A, j, i):
        M = np.array(A)
        M = np.delete(np.delete(M, j, axis=0), i, axis=1)
        return M
    
    # scompongo PT e CT sottoforma di matrice di:
    # righe = lunghezza testo / dimensione del blocco di parole
    # colonne = dimensione del blocco di parole
    def _create_block_matrix(self) -> None:
        pt_arr = []
        ct_arr = []
        index = 0
        block_dim = self.get_block_dim()
        n = block_dim

        iterations = len(self.get_pt()) // n
        while iterations > 0:
            pt_arr.append((self.get_pt()[index:n]))
            ct_arr.append((self.get_ct()[index:n]))
            index = n
            n += self.get_block_dim()
            iterations -= 1

        self._set_pt((pt_arr))
        self._set_ct((ct_arr))