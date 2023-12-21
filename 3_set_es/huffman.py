def riordina_dati(lettere: list, probabilita: list):

    for i in range(len(lettere)):
        k = -1
        probabilita_minima = 1
        for j in range(i, len(probabilita)):
            if probabilita[j] < probabilita_minima:
                probabilita_minima = probabilita[j]
                k = j
        if k != -1:
            probabilita_da_spostare_in_avanti = probabilita[i]
            probabilita_da_spostare_indietro = probabilita[k]
            probabilita[i] = probabilita_da_spostare_indietro
            probabilita[k] = probabilita_da_spostare_in_avanti

            lettera_da_spostare_in_avanti = lettere[i]
            lettera_da_spostare_indietro = lettere[k]
            lettere[i] = lettera_da_spostare_indietro
            lettere[k] = lettera_da_spostare_in_avanti

def aggiorna_valori(dizionario_percorsi: dict, chiave, valore: int):
    for c in chiave:
        # ho una tupla
        if len(c) > 1: aggiorna_valori(dizionario_percorsi, c, valore)
        # aggiorno il valore della chiave
        else:
            dizionario_percorsi[c] = valore + dizionario_percorsi.get(c)

def codice_huffman(lettere: list, probabilita: list) -> dict:
    if len(lettere) != len(probabilita): raise Exception("Una delle due liste ha troppi valori, riprovare.")
    if sum(probabilita) != 1: raise Exception("La somma delle probabilità non fa 1, riprovare.")
    
    # ordino i dati in modo crescente -> anche le lettere associate alle probabilità
    riordina_dati(lettere, probabilita)    

    dizionario_percorsi = {}

    # ad ogni iterazione:
    # 1) prendo una coppia di probabilità e la sommo tra loro,
    # aggiungo 0 alla lettera di sx corrispondente e 1 a quella di dx
    # 2) riordino in modo crescente
    while probabilita.count(1.0) != 1:
        probabilita_1 = probabilita.pop(0)
        probabilita_2 = probabilita.pop(0)
        
        # considero il numero di cifre decimale delle due probabilità
        # mi servirà per arrotondare al numero di cifre decimali maggiore
        n_1 = len(str(probabilita_1).split(".")[1])
        n_2 = len(str(probabilita_2).split(".")[1])

        # inserisco in prima posizione la nuova probabilità calcolata,
        # arrotondandola ad un numero di cifre decimali pari a quelle presenti
        # nella 'vecchia' probabilità
        probabilita.insert(0, (round(probabilita_1 + probabilita_2, n_1 if n_1 > n_2 else n_2)))

        lettera_1 = lettere.pop(0)
        lettera_2 = lettere.pop(0)
        lettere.insert(0, ((lettera_1, lettera_2)))
        dizionario_percorsi[lettera_1] = '0'
        dizionario_percorsi[lettera_2] = '1'

        riordina_dati(lettere, probabilita)
        
    for chiave, valore in dizionario_percorsi.items():
        # sono in presenza di una tupla
        if len(chiave) > 1:
            aggiorna_valori(dizionario_percorsi, chiave, valore)

    dizionario_percorsi = {chiave: valore for chiave, valore in dizionario_percorsi.items() if len(chiave) < 2}
    return dizionario_percorsi

def decodifica_huffman(codice_pf: dict, stringa_binaria: str) -> str:
    # ad ogni iterazione
    # 1) considero una lettera alla volta nella stringa
    # 2) controllo che faccia parte del codice:
    # si -> salvo la lettera corrispondente
    # no -> continuo ad iterare
    stringa_decodificata = ''
    blocco = ''
    for lettera in stringa_binaria:
        blocco += lettera

        # esiste la codifica
        if codice_pf.get(blocco) != None:
            stringa_decodificata += codice_pf.get(blocco)
            blocco = ''

    return stringa_decodificata

lettere =  ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
probabilita = [0.025, 0.025, 0.05, 0.1, 0.13, 0.17, 0.25, 0.25]
print(codice_huffman(lettere, probabilita))

codice = {'00000': 'a',
          '00001': 'b',
          '00010': 'c',
          '00011': 'd',
          '00100': 'e',
          '00101': 'f',
          '00110': 'g',
          '00111': 'h',
          '01000': 'i',
          '01001': 'j',
          '01010': 'k',
          '01011': 'l',
          '01100': 'm',
          '01101': 'n',
          '01110': 'o',
          '01111': 'p',
          '10000': 'q',
          '10001': 'r',
          '10010': 's',
          '10011': 't',
          '10100': 'u',
          '10101': 'v',
          '10110': 'w',
          '10111': 'x',
          '11000': 'y',
          '11001': 'z',
          '11010': ' '
        }
stringa_binaria = '0110001000110100111101000000000001000010010000111001101011101101001000110100000101000100100001001110100111001101000'
print(decodifica_huffman(codice, stringa_binaria))