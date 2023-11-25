import random, time
import numpy as np

def euclide_esteso(a, b):
    # caso base in cui a = 0 e b = 1
    if a % b == 0: return (b, 0, 1) 
    else:
        # inverto i valori di 'a' e 'b' 
        mcd, c, d = euclide_esteso(b%a, a) 

        # calcolo il nuovo valore di c
        x = d - (b//a) * c

    return mcd, x, c

print(euclide_esteso(60, 17))

def esponenziazione_modulare_veloce(a, e, m) -> int:
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

print(esponenziazione_modulare_veloce(3, 11, 10))

def trova_m_dispari_e_r(n_1, r = 0):
    if n_1 % 2 != 0: return n_1, r
    n_1, r = trova_m_dispari_e_r(n_1//2, r + 1)
    return n_1, r

# True = Composto 
# False = forse primo
def miller_rabin(n, x = 2) -> bool:
    if n < 1: raise Exception("n deve essere >= 1, riprovare.")
    if x >= n: raise Exception("x >= n non è ammesso, riprovare.")
    if n % 2 == 0: return True

    n_1 = n-1
    m, r = trova_m_dispari_e_r(n_1)    

    x = esponenziazione_modulare_veloce(x, m, n)

    # x banale
    if x == 1 or x == -1: return False

    while r > 0:
        # x banale
        if ((x % n) - n) == -1: return False

        x = esponenziazione_modulare_veloce(x, 2, n)
        r -= 1

    return True

print(miller_rabin(41)) # F
print(miller_rabin(15)) # V
print(miller_rabin(561)) # V
print(miller_rabin(17)) # F

def generatore_numeri_primi(k) -> list:
    while True:
        # 1) n = vettore di k bit casuali, il + e - significativo a 1
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

print("Il numero primo è:", generatore_numeri_primi(200))

def rsa_decryption_normale(ct, d, n):
    return esponenziazione_modulare_veloce(ct, d, n)

def rsa_decryption_crt(p, q, sp, sq, n):
    q_inverso = euclide_esteso(q, p)[1]
    p_inverso = euclide_esteso(p, q)[1]
    
    return ((q*(q_inverso % p)*sp + p*(p_inverso % q)*sq) % n)

def rsa():
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
        # in prima posizione (più a sx) e riporto il risultato in bit
        d = int.from_bytes(random.randbytes(int.bit_count(n)//8), "big")
        # d*e congruo 1 mod phi_n
        mcd, e, _ = euclide_esteso(d, phi_n) 
        if mcd == 1: break

    # se negativa => calcolo il modulo 
    if e < 0: e %= phi_n

    # scambio i valori di 'e' con 'd' e 'd' con 'e' 
    # per avere 'd' > 'e', altrimenti l'attaccante
    # potrebbe trovare 'd' per tentativi
    if e > d: e, d = d, e

    '''
    print("N", int.bit_count(n))
    print("q", int.bit_count(d))
    print(len(str(p)))
    print(len(str(q)))
    print(len(str(n)))
    print(len(str(d)))
    print(len(str(e)))
    '''
    
    # genero 100 ct, randomicamente, di lunghezza 100 
    iterazioni = 100
    norm_maggiore_crt = 0
    while iterazioni > 0:
        ct = random.randrange(1, 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999)        

        '''
        print("ct", int.bit_count(ct))
        print("r1crt", int.bit_count(resto1_crt))
        print("r2crt", int.bit_count(resto2_crt))
        '''
        inizio_decr_norm = time.time()
        uno = rsa_decryption_normale(ct, d, n)
        fine_decr_norm = time.time()
        
        sp = esponenziazione_modulare_veloce(ct, d, p)
        sq = esponenziazione_modulare_veloce(ct, d, q)
        inizio_decr_crt = time.time()
        due = rsa_decryption_crt(p, q, sp, sq, n)
        fine_decr_crt = time.time()

        diff_norm = fine_decr_norm - inizio_decr_norm
        diff_crt = fine_decr_crt - inizio_decr_crt
        print("Norm", diff_norm)
        print("Crt", diff_crt)

        if diff_crt < diff_norm: norm_maggiore_crt += 1   
        iterazioni -= 1        
    
    print(norm_maggiore_crt)

rsa()







# True = Composto 
# False = forse primo
def miller_rabin_modificato(n, m, r, x = 2) -> bool:
    x = esponenziazione_modulare_veloce(x, m, n)

    # x banale
    if x == 1 or x == -1: return -1

    while r > 0:
        # x banale
        if ((x % n) - n) == -1: return -1

        x_precedente = x
        x = esponenziazione_modulare_veloce(x, 2, n)

        if x == 1 and (x_precedente % n != - 1):
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
            return 0

        iterazioni += 1
        # Miller-Rabin     
        mcd = miller_rabin_modificato(n, m, r, x)
        if mcd != -1: return iterazioni

def rsa_3_2():
    tempo_esecuzione_algoritmo = [0.0] * 100
    numero_iterazioni_algoritmo = [0] * 100

    for i in range(100):
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
            # in prima posizione (più a sx) e riporto il risultato in bit
            d = int.from_bytes(random.randbytes(int.bit_count(n)//8), "big")
            # d*e congruo 1 mod phi_n
            mcd, e, _ = euclide_esteso(d, phi_n)
            if mcd == 1: break

        inizio = time.time()
        iterazioni_algoritmo =  decryptionexp(n, d, e)
        fine = time.time()

        numero_iterazioni_algoritmo[i] = iterazioni_algoritmo
        tempo_esecuzione_algoritmo[i] = fine - inizio

    print("# medio iterazioni:", str(sum(numero_iterazioni_algoritmo) / 100))
    print("Tempo medio esecuzione (secondi):", str(sum(tempo_esecuzione_algoritmo) / 100))
    print("Varianza (s^2):", np.var(tempo_esecuzione_algoritmo))

rsa_3_2()