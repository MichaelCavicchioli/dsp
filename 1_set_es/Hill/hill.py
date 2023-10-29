import math
import numpy as np

class Hill:

    # inizializzo gli attributi
    def __init__(self) -> None:
        print("Hill...")
        self.pt, self.block_dim = self._check_input()

    # eseguo l'encryption
    def encryption(self):
        print("Encryption...")
        
        # rimuovo i caratteri superflui dal PT e sostituisco le lettere con i numeri
        self._remove_chars_from_pt()
        self._replace_chars_with_nums()

        # genero randomicamente la matrice K NxN solo se:
        # il MCD(det(K), 26) = 1
        self._generate_k_matrix()

        print("PT:", self.get_pt())
        print("K:", self.get_K())

        # genero il CT
        self._set_ct(self._generate_plain_or_cipher_text(K=self.get_K(), known_text=self.get_pt()))
        print("Encryption is:", self.get_ct())

    # eseguo la decryption
    def decryption(self):
        print("Decryption...")

        # calcola la matrice K^(-1)
        K_inverse = self._get_inverse_matrix(self.get_K())

        # genero il PT
        self._set_pt(self._generate_plain_or_cipher_text(K=K_inverse, known_text=self.get_ct()))
        print("Decryption is:", self.get_pt())

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

    # Rimuovo caratteri dal PT perchè n non lo divide perfettamente
    def _remove_chars_from_pt(self):
        num_chars_to_remove = len(self.get_pt()) % self.get_block_dim()
        if num_chars_to_remove > 0:
            # Rimuove gli ultimi 'num_chars_to_remove' caratteri
            self._set_pt(self.get_pt()[:-num_chars_to_remove]) 

    # sostituisco i caratteri con i numeri
    def _replace_chars_with_nums(self):
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
        # Sostituisco le lettere in numeri per il PT
        message_list = []
        for chr in self.get_pt():
            message_list.append(int(chr.replace(chr, dict[chr])))
        self._set_pt(message_list)

    # genero randomicamente la matrice K (mod 26)
    # la restituisco solo se coprima con 26
    def _generate_k_matrix(self):
        while True:
            self.K = np.random.randint(low=0, high=26, size=(self.get_block_dim(), self.get_block_dim()))
            if math.gcd(self._get_determinant(self.get_K()), 26) == 1:
                break

    # genero il PT/CT tramite la chiave K ed il CT/PT
    def _generate_plain_or_cipher_text(self, K, known_text) -> str:
        generated_txt = [0 for _ in range(len(known_text))]

        start, index = 0, 0
        finish = self.get_block_dim()
        block_dim = self.get_block_dim()

        iterations = len(generated_txt) // block_dim
        while iterations > 0:
            # mi muovo di n caratteri alla volta
            array = known_text[start:finish] 
            
            for j in range(block_dim):
                # moltiplico la riga j-esima di K per l'i-esimo PT 
                generated_txt[index] = np.matmul(K[j], array)%26 
                index += 1
            
            start += block_dim
            finish += block_dim
            iterations -= 1
    
        return generated_txt
    
    # calcolo la matrice inversa
    def _get_inverse_matrix(self, A):
        # ottengo il determinante
        determinant = self._get_determinant(A)

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

    # calcolo il determinante
    def _get_determinant(self, A):
        return round((np.linalg.det(A))%26)

    # rimuovo la riga j e la colonna i dalla matrice
    def _get_matrix_with_no_j_row_i_col(self, A, j, i):
        M = np.array(A)
        M = np.delete(np.delete(M, j, axis=0), i, axis=1)
        return M
    
    # controllo che l'utente inserisca correttamente gli input
    def _check_input(self):
        # PT in lowercase
        pt = input("Enter the PT (Z26): ").lower()
        if len(pt) == 0:
            raise Exception("You must enter a PT.")
        if any(chr.isdigit() for chr in pt):
            raise Exception("Numbers are not allowed.")

        # dimensione dei blocchi
        block_dim = input("Enter the dimension of blocks: ")

        if len(block_dim) == 0:
            raise Exception("You must enter a dimension.")
        if block_dim.isalpha():
            raise Exception("Only numbers are allowed.")
        block_dim = int(block_dim)
        if block_dim == 0:
            raise Exception("The dimension must be > 0.")

        return pt, block_dim