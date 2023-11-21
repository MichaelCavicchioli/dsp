import random, time

def euclide_esteso(a, b) -> int:
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

def trova_m_dispari_e_r(n_1, r):
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
    m, r = trova_m_dispari_e_r(n_1, 0)    

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

def rsa_decryption(ct, d, n):
    return esponenziazione_modulare_veloce(ct, d, n)

def rsa():
    # generazione di p, q
    while True: 
        p, q = generatore_numeri_primi(200), generatore_numeri_primi(200)
        if p != q: break
        
    # calcolo n
    n = p*q
    # calcolo phi(n)
    phi_n = (p-1) * (q-1)

    # genero 'd' ed 'e'
    while True:
        d = generatore_numeri_primi(200)
        e = euclide_esteso(d, phi_n)[1]
        if euclide_esteso(d, phi_n)[0] == 1: break

    # se negativa => calcolo il modulo 
    if e < 0:
        e %= phi_n

    # scambio i valori di 'e' con 'd' e 'd' con 'e' 
    # per avere 'd' > 'e', altrimenti l'attaccante
    # potrebbe trovare 'd' per tentativi
    if e > d: e, d = d, e

    # genero 100 ct, randomicamente, di lunghezza 100 
    for i in range(100):
        ct = random.randrange(1, 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999)
        inizio = time.time()
        pt = rsa_decryption(ct, d, n)
        fine = time.time()
        print(fine-inizio)        

rsa()