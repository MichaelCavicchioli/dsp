def euclide_esteso(a, b) -> int:
    if a - b == 0: return b 
    else:
        q = 1
        while True:
            if a - (b*q) <= 0: break
            q += 1

        q -= 1
        b = euclide_esteso(b, (a-(b*q)))
    return b

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

#print(esponenziazione_modulare_veloce(3, 11, 10))

def trova_m_dispari(n_1) -> int:
    if n_1 % 2 != 0: return n_1
    n_1 = trova_m_dispari(n_1//2)
    return n_1

# True = Composto 
# False = forse primo
def miller_rabin(n, r=1, x = 2) -> bool:
    if x >= n: raise Exception("x >= n non è ammesso, riprovare.")
    if n % 2 == 0: return True
    
    n_1 = n-1
    m = trova_m_dispari(n_1)    
    while True:
        if (2**r)*m == n_1: break
        r += 1

    x = esponenziazione_modulare_veloce(x, m, n)
    while r > 0:
        if ((x % n) - n) == -1: return False
        x = esponenziazione_modulare_veloce(x, 2, n)
        r -= 1
        
    return True

print(miller_rabin(41)) # F
print(miller_rabin(15)) # V
print(miller_rabin(561)) # V
print(miller_rabin(17)) # F

def generatore_numeri_primi(k) -> list:
    import random
    # 1) n = vettore di k bit casuali, il + e - significativo a 1
    n = '1'
    for _ in range(k-2): n += str(random.randint(0,1))
    n += '1'

    # trasformo n in numero intero
    n = int(n, 2)

    # 2) n primo?
    # Si => stop
    # No => 1)

    # richiama Miller Rabin

generatore_numeri_primi(10)
