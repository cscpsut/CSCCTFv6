
def hash(m, block_size = 5, shift = 3):
    blocks = [m[i: i + block_size] for i in range(0, len(m), block_size)]
    ct = []
    for block in blocks:
        ct.append("".join([block[(i + shift) % len(block)] for i in range(block_size)]))
        
    return "".join(ct)

# Example usage
hashed_password = " fZip pilewoassNOrd HET TAG FLZi : lepFiptCrynioGesusus"
original_password = hash(hashed_password, 5, 2)
print(original_password)
