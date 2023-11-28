from algoritmi import euclide_esteso, esponenziazione_modulare_veloce

n = 1309914994772590863210166992356557234456075980579048604758768205496404269677841156459642052158879494989630338961154043468325508153199153204245943547981

c1 = 1208833588708967444709375
c2 = 411294544478239271886338859092185183748200324266700081787109375

e1, e2 = 5, 13

# e1*x + e2*y = 1
_, x, y = euclide_esteso(e1, e2)

# print("x:", x)
# print("y:", y)

# c1*c1_inverso congruo 1 mod n
c1_inverso = euclide_esteso(c1, n)[1]

# abs(x) = prendo il valore assoluto, quindi positivo
m = (
    esponenziazione_modulare_veloce(c1_inverso, abs(x), n) * 
    esponenziazione_modulare_veloce(c2, y, n)
    ) % n

print("Il messaggio è:", m)