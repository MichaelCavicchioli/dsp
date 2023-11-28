from algoritmi import *

def main():
        
    print("Euclide esteso con 60 e 17:")
    print("(60, 17) = " + str(euclide_esteso(60, 17)[0]))
    print("Identità di Bèzout x = " + str(euclide_esteso(60, 17)[1]))
    print("Identità di Bèzout y = " + str(euclide_esteso(60, 17)[2]), "\n")

    print("Esponenziazione modulare veloce di 3^11 mod 10 = " + str(esponenziazione_modulare_veloce(3, 11, 10)), "\n")

    print("Miller-Rabin (T = composto, F = forse primo):")
    print("41:", miller_rabin(41)) # F
    print("15:", miller_rabin(15)) # V
    print("561:", miller_rabin(561)) # V
    print("17:", miller_rabin(17), "\n") # F

    print("Il numero primo è:", generatore_numeri_primi(200), "\n")

    print("RSA:")
    rsa()

    print("RSA (3.2):")
    rsa_3_2()

if __name__ == '__main__':
    main()