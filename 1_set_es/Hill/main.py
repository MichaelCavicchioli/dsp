from hill import Hill
from attacker import Attacker

hill = Hill()

# Fase di Encryption
hill.encryption()

# Fase di Decryption
hill.decryption()

######### ATTACCO #########
attacker = Attacker(hill.get_pt(), hill.get_ct(), hill.get_block_dim())
attacker.attack()