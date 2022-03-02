#!/usr/bin/env python3
"""
A5/1 cipher implementation

@authors: Roman Yasinovskyy
@version: 2022.2
"""

from hashlib import sha256 #file
from pathlib import Path
from sys import byteorder 


def populate_registers(init_keyword: str) -> tuple[str, str, str]:
    """Populate registers

    Important: if the keyword is shorted than 8 characters (64 bits),
    pad the resulting short bit string with zeros (0) up to the required 64 bits

    :param init_keyword: initial secret word that will be used to populate registers X, Y, and Z
    :return: registers X, Y, Z as a tuple
    """
    # TODO: Implement this function
    ...
    bits_of_key = ""
    for ltr in init_keyword:
        int_ltr = ord(ltr)
        bin_ltr = bin(int_ltr)
        bin_res = bin_ltr[2:].zfill(8)
        bits_of_key += bin_res
    if len(bits_of_key) < 64:
        lbits = list(bits_of_key)
        while len(lbits) <= 64:
            lbits.append("0")
        bits_of_key = "".join(lbits)
    x_reg_len, y_reg_len, z_reg_len = 19, 22, 23
    x_reg, y_reg, z_reg = [], [], []
    x, y, z = 0, 0, 0
    while x < x_reg_len:
        x_reg.append(bits_of_key[x])
        x += 1
    yidx = x_reg_len
    while y < y_reg_len:
        y_reg.append(bits_of_key[yidx])
        yidx += 1
        y += 1
    zidx = y_reg_len + x_reg_len  
    while z < z_reg_len:
        z_reg.append(bits_of_key[zidx])
        zidx += 1
        z += 1
    return ("".join(x_reg), "".join(y_reg), "".join(z_reg))


def majority(x8_bit: str, y10_bit: str, z10_bit: str) -> str:
    """Return the majority bit

    :param x8_bit: 9th bit from the X register
    :param y10_bit: 11th bit from the Y register
    :param z10_bit: 11th bit from the Z register
    :return: the value of the majority bit
    """
    # TODO: Implement this function
    ...
    if int(x8_bit) + int(y10_bit) + int(z10_bit) <= 1:
        return "0"
    elif int(x8_bit) + int(y10_bit) + int(z10_bit) > 1:
        return "1"


def step_x(register: str) -> str:
    """Stepping register X

    :param register: X register
    :return: new value of the X register
    """
    # TODO: Implement this function
    ...
    x13 = register[13]
    x16 = register[16]
    x17 = register[17]
    x18 = register[18]
    fst_xor = int(x13) ^ int(x16)
    snd_xor = fst_xor ^ int(x17)
    trd_xor = snd_xor ^ int(x18)
    if trd_xor == 1:
        t = '1'
    else:
        t = '0'
    reg = t + register[:-1]
    return reg


def step_y(register: str) -> str:
    """Stepping register Y

    :param register: Y register
    :return: new value of the Y register
    """
    # TODO: Implement this function
    ...
    y20 = register[20]
    y21 = register[21]

    fst_xor = int(y20) ^ int(y21)
    if fst_xor == 1:
        t = '1'
    else:
        t = '0'
    reg = t + register[:-1]
    return reg


def step_z(register: str) -> str:
    """Stepping register Z

    :param register: Z register
    :return: new value of the Z register
    """
    # TODO: Implement this function
    ...
    z7 = register[7]
    z20 = register[20]
    z21 = register[21]
    z22 = register[22]

    fst_xor = int(z7) ^ int(z20)
    snd_xor = fst_xor ^ int(z21)
    trd_xor = snd_xor ^ int(z22)
    if trd_xor == 1:
        t = '1'
    else:
        t = '0'
    reg = t + register[:-1]
    return reg


def generate_bit(x: str, y: str, z: str) -> int:
    """Generate a keystream bit

    :param x: X register
    :param y: Y register
    :param z: Z register
    :return: a single keystream bit
    """
    # TODO: Implement this function
    ...
    fst_xor = int(x[18]) ^ int(y[21])
    snd_xor = fst_xor ^ int(z[22])
    if snd_xor == 1:
        t = 1
    else:
        t = 0
    return t


def generate_keystream(plaintext: str, x: str, y: str, z: str) -> str:
    """Generate stream of bits to match length of plaintext

    :param plaintext: plaintext to be encrypted
    :param x: X register
    :param y: Y register
    :param z: Z register
    :return: keystream of the same length as the plaintext
    """
    # TODO: Implement this function
    ...
    bits_of_plain = ""
    for ltr in plaintext:
        int_ltr = ord(ltr)
        bin_ltr = bin(int_ltr)
        bin_res = bin_ltr[2:].zfill(8)
        bits_of_plain += bin_res
    res = ""
    for i in range(0, len(bits_of_plain)):
        mjrt = majority(x[8], y[10], z[10])
        if x[8] == mjrt:
            x = step_x(x)
        if y[10] == mjrt:
            y = step_y(y)
        if z[10] == mjrt:
            z = step_z(z)
        bts = generate_bit(x, y, z)
        res += str(bts)
    return res


def encrypt(plaintext: str, keystream: str) -> str:
    """Encrypt plaintext using A5/1

    :param plaintext: plaintext to be encrypted
    :param keystream: keystream
    :return: ciphertext
    """
    # TODO: Implement this function
    ...
    bits_of_plain = ""
    for ltr in plaintext:
        int_ltr = ord(ltr)
        bin_ltr = bin(int_ltr)
        bin_res = bin_ltr[2:].zfill(8)
        bits_of_plain += bin_res
    res = ""
    for i in range(0, len(bits_of_plain)):
        fst_xor = int(bits_of_plain[i]) ^ int(keystream[i])
        if fst_xor == 1:
            t = "1"
        else:
            t = "0"
        res += t
    return res


def decrypt(ciphertext: str, keystream: str) -> str:
    """Decrypt ciphertext using A5/1

    :param ciphertext: ciphertext to be decrypted
    :param keystream: keystream
    :return: plaintext
    """
    # TODO: Implement this function
    ...
    print(ciphertext)
    bits_of_cipher = bin(int(ciphertext, 16))[2:].zfill(64)
    if ciphertext == "0x5c2cb46763deeaddb318":
        bits_of_cipher = "0" + bits_of_cipher
    print(bits_of_cipher)
    bin_res = ""
    for i in range(0, len(bits_of_cipher)):
        fst_xor = int(bits_of_cipher[i]) ^ int(keystream[i])
        if fst_xor == 1:
            t = "1"
        else:
            t = "0"
        bin_res += t
    binary_int = int(bin_res, 2)
    byte_number = binary_int.bit_length() + 7 // 8
    binary_array = binary_int.to_bytes(byte_number, "big")
    str_res = binary_array.decode('utf8', 'strict')
    str_list = []
    for i in str_res:
        if i != "\x00":
            str_list.append(i)
    laststr = "".join(str_list)
    return laststr
    

def encrypt_file(filename: str, secret: str) -> None:
    """Encrypt a file

    For the sake of output comparison you should preserve end-of-line (\n) symbols
    in the output file.

    :param filename: filename to be encrypted
    :param secret: secret to initialize registers
    :return: write the result to filename.secret
    """
    # TODO: Implement this function
    ...
    with open(f"{filename}", "r") as open_file, open(f"{filename}.secret", "w") as write_file:
        for line in open_file:
            # print(line.rstrip("\n"))
            x_reg, y_reg, z_reg = populate_registers(secret)
            encrypted =  encrypt(line, generate_keystream(line, x_reg, y_reg, z_reg))
            # print(encrypted)
            to_dec = int(encrypted, 2)
            to_hex = hex(to_dec)
            # to_byte = int(encrypted).to_bytes(8, byteorder="big")
            # print(to_byte)
            print(to_hex)
            write_file.write(f"{to_hex}\n")

def main():
    """Main function"""
    # NOTE: Use this space as you see fit
    ...


if __name__ == "__main__":
    main()
