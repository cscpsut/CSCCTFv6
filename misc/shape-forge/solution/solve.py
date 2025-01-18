def xor_hex_with_key(hex_string, key):

    key_bytes = key.encode()


    hex_bytes = bytes.fromhex(hex_string)


    result_bytes = bytearray()
    for i in range(len(hex_bytes)):
        result_bytes.append(hex_bytes[i] ^ key_bytes[i % len(key_bytes)])


    return result_bytes.decode('utf-8', errors='replace')

if __name__ == "__main__":
 
    hex_input = "1b03711b04742329022d0f406b0f5c68676d6d67473c635c6f656d6c3e4b3560406b0f4b68256d2a636d200f5f6b3e4f"  
    key = "XP2"

    print("Simulating input with hex string:", hex_input)

    try:
        result = xor_hex_with_key(hex_input, key)
        print("Resulting text:", result)
    except ValueError:
        print("Invalid hex string provided.")
