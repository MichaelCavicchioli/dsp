def euclide_esteso(a, b) -> int:
    # caso base in cui a = 0 e b = 1
    if a % b == 0: return (b, 0, 1) 
    else:
        # inverto i valori di 'a' e 'b' 
        mcd, c, d = euclide_esteso(b%a, a) 

        # calcolo il nuovo valore di c
        x = d - (b//a) * c

    return mcd, x, c

n = 1309914994772590863210166992356557234456075980579048604758768205496404269677841156459642052158879494989630338961154043468325508153199153204245943547981

c1 = 1208833588708967444709375
c2 = 411294544478239271886338859092185183748200324266700081787109375

e1, e2 = 5, 13

_, x, y = euclide_esteso(e1, e2)

_, _, c1_inverse = euclide_esteso(c1, n)

m = ((c1**x) * (c2**y)) % n

print("Il messaggio è:", m)