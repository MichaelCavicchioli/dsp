import random, time
import numpy as np

def euclide_esteso(a, b):
    # caso base in cui a = 0 e b = 1
    if a == 0: return (b, 0, 1) 
    else:
        # inverto i valori di 'a' e 'b' 
        mcd, c, d = euclide_esteso(b%a, a) 

        # calcolo il nuovo valore di a
        x = d - (b//a) * c

    return mcd, x, c

def esponenziazione_modulare_veloce(a, e, m) -> int:
    if e < 0: raise Exception("L'esponente deve essere >= 0, riprovare.")
    if m < 1: raise Exception("Il modulo deve essere >= 1, riprovare.")

    # l'esponente lo converto in base 2 ed elimino i primi
    # due caratteri (0b)
    e = bin(e)[2:]
    d = 1
    c = 0
    
    for i in e:
        d = (d * d) % m
        c *= 2
        
        if i == '1':
            d = (d * a) % m
            c += 1
    
    return d            

def trova_m_dispari_e_r(n_1, r = 0):
    if n_1 % 2 != 0: return n_1, r
    n_1, r = trova_m_dispari_e_r(n_1//2, r + 1)
    return n_1, r

# True = Composto 
# False = forse primo
def miller_rabin(n, x = 2) -> bool:
    if n < 1: raise Exception("n deve essere >= 1, riprovare.")
    if x >= n or x < 0: raise Exception("x >= n o x < 0 non è ammesso, riprovare.")
    if n % 2 == 0: return True
    
    m, r = trova_m_dispari_e_r(n-1)    

    x = esponenziazione_modulare_veloce(x, m, n)

    # x banale
    if x == 1 or x == n - 1: return False

    while r > 0:
        # x banale
        if x == n - 1: return False

        x = esponenziazione_modulare_veloce(x, 2, n)
        r -= 1

    return True

def generatore_numeri_primi(k) -> list:
    while True:
        # 1) n = vettore di k bit casuali, il più e il meno significativo a 1
        n = '1'
        for _ in range(k-2): 
            n += str(random.randint(0,1))
        n += '1'

        # trasformo n in numero intero
        n = int(n, 2)

        # genero una x randomica
        x = random.randrange(2, n-1)

        # 2) n primo?
        # se non è composto e l'mcd = 1 => n forse è primo 
        n_primo = miller_rabin(n, x) == False and euclide_esteso(n, x)[0] == 1 

        # setto valori della soglia 
        tolleranza = 1/4
        tolleranza_soglia = 0.0000000001

        while tolleranza > tolleranza_soglia and n_primo:
            # se non è composto e l'mcd = 1 => n forse è primo
            n_primo = miller_rabin(n, x) == False and euclide_esteso(n, x)[0] == 1 

            if n_primo:
                # scelgo una nuova x
                x = random.randrange(2, n-1)
                tolleranza *= 1/4  

        if tolleranza <= tolleranza_soglia and n_primo:
            return n
        
def encryption_rsa(pt, e, n):
    return esponenziazione_modulare_veloce(pt, e, n)

def decryption_normale_rsa(ct, d, n):
    return esponenziazione_modulare_veloce(ct, d, n)

def decryption_crt_rsa(ct, d, p, q, p_inverso, q_inverso, n):
    sp = esponenziazione_modulare_veloce(ct, d, p)
    sq = esponenziazione_modulare_veloce(ct, d, q)
        
    return ((q*(q_inverso % p)*sp + p*(p_inverso % q)*sq) % n)

def genera_valori_rsa():
    # generazione di p, q
    while True: 
        p, q = generatore_numeri_primi(200), generatore_numeri_primi(200)
        if p != q: break
        
    # calcolo n
    n = p*q
    # calcolo phi(n)
    phi_n = (p-1) * (q-1)

    # genero 'd' (di circa 200 bit) ed 'e'
    while True:
        # considero i bit di 'n' e li divido per 8 per ottenere il numero di byte
        # genero randomicamente quei byte, mettendo il valore più sigificativo
        # in prima posizione (più a sx) e riporto il risultato in intero
        d = int.from_bytes(random.randbytes(len(bin(n))//8), "big")
        # d*e congruo 1 mod phi_n
        mcd, e, _ = euclide_esteso(d, phi_n) 
        if mcd == 1: break

    # se negativa => calcolo il modulo 
    if e < 0: e %= phi_n

    # scambio i valori di 'e' con 'd' e 'd' con 'e' 
    # per avere 'd' > 'e', altrimenti l'attaccante
    # potrebbe trovare 'd' per tentativi
    if e > d: e, d = d, e

    return n, p, q, phi_n, e, d

def rsa():
    # genero i valori per RSA
    n, p, q, _, e, d = genera_valori_rsa()

    # genero 100 pt, randomicamente, di lunghezza 1000
    iterazioni = 100
    numero_volte_tempo_decr_normale_maggiore_crt = 0
    numero_volte_tempo_decr_crt_maggiore_normale = 0
    while iterazioni > 0:
        pt = random.randrange(2, 10**1000) 

        # ottengo il ct
        ct = encryption_rsa(pt, e, n)

        inizio_decr_norm = time.time()
        decryption_normale = decryption_normale_rsa(ct, d, n)
        fine_decr_norm = time.time()

        # pre-computo i valori per il CRT        
        q_inverso = euclide_esteso(q, p)[1]
        p_inverso = euclide_esteso(p, q)[1]
        inizio_decr_crt = time.time()
        decryption_crt = decryption_crt_rsa(ct, d, p, q, p_inverso, q_inverso, n)
        fine_decr_crt = time.time()

        assert(decryption_normale == decryption_crt), "Errore in fase di decryption."

        diff_norm = fine_decr_norm - inizio_decr_norm
        diff_crt = fine_decr_crt - inizio_decr_crt

        if diff_norm > diff_crt: numero_volte_tempo_decr_normale_maggiore_crt += 1
        elif diff_norm < diff_crt: numero_volte_tempo_decr_crt_maggiore_normale += 1
        print("Tempo Decr. normale: " + str(diff_norm) + ", tempo Decr. CRT: " + str(diff_crt))
        
        iterazioni -= 1

    print("# volte in cui tempo della decr. normale è stato maggiore di quello della decr. con Crt:", numero_volte_tempo_decr_normale_maggiore_crt)
    print("# volte in cui tempo della decr. con Crt è stato maggiore di quello della decr. normale:", numero_volte_tempo_decr_crt_maggiore_normale, "\n")

# True = Composto 
# False = forse primo
def miller_rabin_modificato(n, m, r, x = 2) -> bool:
    x = esponenziazione_modulare_veloce(x, m, n)

    # x banale
    if x == 1 or x == n - 1: return -1

    while r > 0:
        x_precedente = x
        x = esponenziazione_modulare_veloce(x, 2, n)

        # x banale
        if x == n - 1: return -1
        # se Xj == 1 e X_(j-1) non è congruo -1 mod n 
        elif x == 1 and ((x_precedente % n) - n) != -1:
            # restituisco il mcd
            return euclide_esteso(x_precedente + 1, n)[0]

        r -= 1

    return -1

def decryptionexp(n, d, e):
    iterazioni = 0
    # 1) ed - 1 = 2^r * m 
    m, r = trova_m_dispari_e_r((e*d-1))

    # 2) x, random, coprimo con n
    while True:
        x = random.randint(2, n-1)

        # mcd != 1 => ho trovato l'mcd
        if euclide_esteso(x, n)[0] != 1:
            return iterazioni

        iterazioni += 1
        # Miller-Rabin     
        mcd = miller_rabin_modificato(n, m, r, x)
        if mcd != -1: return iterazioni

def rsa_3_2():
    tempo_esecuzione_algoritmo = [0.0] * 100
    numero_iterazioni_algoritmo = [0] * 100

    for i in range(100):
        # genero i valori per RSA
        n, _, _, _, e, d = genera_valori_rsa()
        
        inizio = time.time()
        iterazioni_algoritmo = decryptionexp(n, d, e)
        fine = time.time()

        numero_iterazioni_algoritmo[i] = iterazioni_algoritmo
        tempo_esecuzione_algoritmo[i] = fine - inizio

    print("# medio iterazioni:", str(sum(numero_iterazioni_algoritmo) / 100))
    print("Tempo medio esecuzione (secondi):", str(sum(tempo_esecuzione_algoritmo) / 100))
    print("Varianza (s^2):", np.var(tempo_esecuzione_algoritmo))
