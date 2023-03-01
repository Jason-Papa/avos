import struct

def to_binary(num):
    return f"{num:08b}"

def merge_bytes(b1, b2, b3):
    b1 = f"{to_binary(b1)}{to_binary(b2)[:4]}"
    b3 = f"{to_binary(b2)[4:]}{to_binary(b3)}"
    return int(b1,2), int(b3,2)

def lzw_decode():
    bytes_8 = []
    with open("b.z", "rb") as f:
        while (byte := f.read(1)):
            bytes_8.append(ord(byte))
    
    bytes_12 = []
    for i in range(0, len(bytes_8), 3):
        try:
            b1, b2 = merge_bytes(bytes_8[i], bytes_8[i+1], bytes_8[i+2])
            bytes_12.append(b1)
            bytes_12.append(b2)
        except:
            bytes_12.append(0, bytes_8[i], bytes_8[i+1])
    print(bytes_12)
    ascii_dict = {i: chr(i) for i in range(256)}
    result = ""
    prev_string = ""
    next_code = 256
    for int_byte in bytes_12:
        if int_byte not in ascii_dict:
            ascii_dict[int_byte] = prev_string + prev_string[0]
        result += ascii_dict[int_byte]
        if prev_string:
            ascii_dict[next_code] = prev_string + ascii_dict[int_byte][0]
            next_code += 1
        prev_string = ascii_dict[int_byte]
    print(result)
lzw_decode()
