from secret import password

def hash(m, block_size = 5, shift = 3):
    blocks = [m[i: i + block_size] for i in range(0, len(m), block_size)]
    ct = []
    for block in blocks:
        ct.append("".join([block[(i + shift) % len(block)] for i in range(block_size)]))
        
    return "".join(ct)

# obvious as hard as hamoor 3
print(f"Super secret hashed password = '{hash(password)}'")

# Super secret hashed password = ' fZip pilewoassNOrd HET TAG FLZi : lepFiptCrynioGesusus'