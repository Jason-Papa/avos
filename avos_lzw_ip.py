####################
# Helper functions #
####################

def to_binary(num: int):
    return f"{num:08b}"

def merge_bytes(b1: int, b2: int, b3: int):
    binary_string_b1 = f"{to_binary(b1)}{to_binary(b2)[:4]}"
    binary_string_b2 = f"{to_binary(b2)[4:]}{to_binary(b3)}"
    return int(binary_string_b1,2), int(binary_string_b2,2)

def initialize_dict():
    return {i: chr(i) for i in range(256)}

############
# Solution #
############
def lzw_decode_from_file(file: str):
    bytes_8 = []
    # read bytes from file
    with open(file, "rb") as f:
        while (byte := f.read(1)):
            bytes_8.append(ord(byte))

    bytes_12 = []
    for i in range(0, len(bytes_8), 3):
        try:
            # if the encoded codes is not even, that would mean that the codes produced is not a multiple of 3
            # this is because every 2 encoded bytes of length 12 each, are broken down to 3 bytes (length 8)
            first_byte, second_byte, third_byte = bytes_8[i], bytes_8[i+1], bytes_8[i+2]
        except:
            first_byte, second_byte, third_byte = 0, bytes_8[i], bytes_8[i+1]
        
        encoded_byte1, encoded_byte2 = merge_bytes(first_byte, second_byte, third_byte)
        bytes_12.append(encoded_byte1)
        bytes_12.append(encoded_byte2)

    ascii_dict = initialize_dict()
    decoded = ""
    prev_string = ""
    next_code = 256
    
    for int_byte in bytes_12:
        if len(ascii_dict) == 4096:
            ascii_dict = initialize_dict()
            next_code = 256
        if int_byte not in ascii_dict:
            ascii_dict[int_byte] = prev_string + prev_string[0]
        decoded += ascii_dict[int_byte]
        if prev_string:
            ascii_dict[next_code] = prev_string + ascii_dict[int_byte][0]
            next_code += 1
        prev_string = ascii_dict[int_byte]
    return decoded

if __name__ == "__main__":
    files= ["01-hello.txt.z", "02-book.txt.z", "03-lyrics.txt.z", "04-icon.png.z"]
    files_text = "\n".join([f"{i+1}) {file}" for i, file in enumerate(files)])

    option = int(input(f"Which file do you want to decode?\n{files_text}\n"))
    while not 0 < option <= len(files):
        option = int(input(f"This is not a valid option please select a valid one to continue or Ctrl+C to exit. \n{files_text} \n"))
    
    decoded = lzw_decode_from_file(files[option-1])
    print(decoded)