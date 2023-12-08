def converti_valori(vettore_riferimenti):

    str_compressa = ''

    for i in range(len(vettore_riferimenti)):   
        
        bit_totali = len(bin(i)[2:])    
        riferimento = vettore_riferimenti[i][0]
        riferimento = bin(riferimento)[2:]

        # se non vale => devo aggiungere tanti 0 quanti la differenza tra loro
        if bit_totali != len(riferimento):
            zero_da_aggiungere = bit_totali - len(riferimento)

            while zero_da_aggiungere > 0:
                str_compressa += '0'         
                zero_da_aggiungere -= 1

        lettera = vettore_riferimenti[i][1]
        str_compressa += (riferimento + lettera)
    return str_compressa

def contiene_blocco(d, temp):
    for blocco in d: 
        if blocco[0] == temp: return True

    return False

def prendi_riferimento(d, temp):
    for blocco in d: 
        if blocco[0] == temp: 
            return blocco[1]

def lz(stringa):
    lista_riferimento_valore = []
    indice = 1
    blocco = ''
    riferimento = 0
    vettore_riferimenti = []
    contatore = 1

    for lettera in stringa:
        blocco += lettera

        # non è presente il blocco
        if contiene_blocco(lista_riferimento_valore, blocco) == False:
            lista_riferimento_valore.append((blocco, indice))
            vettore_riferimenti.append((riferimento, '0' if lettera == 'A' else '1'))

            blocco = ''
            indice += 1
            riferimento = 0
        # è presente
        else:
            # controllo per aggiungere l'ultimo elemento
            if contatore - len(stringa) == 0:
                lista_riferimento_valore.append((blocco, indice))
                vettore_riferimenti.append((riferimento, '0' if lettera == 'A' else '1'))

            riferimento = prendi_riferimento(lista_riferimento_valore, blocco)

        contatore += 1

    return converti_valori(vettore_riferimenti)

assert('011101001010010111001011001001' == lz('AABABBBABAABABBBABBABB')[1:])