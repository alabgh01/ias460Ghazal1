#!/usr/bin/env python3
# encoding: UTF-8

from calendar import c
from socket import socket, gethostname, AF_INET, SOCK_STREAM
from Crypto.Hash import SHA256, HMAC
from Crypto.Cipher import AES, DES, Blowfish
from diffiehellman.diffiehellman import DiffieHellman
from typing import Tuple, Dict



cphr_map = {"DES": DES, "AES": AES, "Blowfish": Blowfish}
iv_ln = {"DES": 8, "AES": 16, "Blowfish": 8}

def generate_cipher_proposal(supported: dict) -> str:
    """Generate a cipher proposal message
    
    :param supported: cryptosystems supported by the client
    :return: proposal as a string
    """
    # raise NotImplementedError
    # prop_str = "ProposedCiphers:"
    # for c, bs in supported.items():
    #     for i in bs:
    #         ps = c+":["+",".join(i)
    #     prop_str += "," + ps
        
    prop_str = "ProposedCiphers:" + ','.join([c + ':[' + ','.join([str(i) for i in bs]) + ']'
                     for c, bs in supported.items()])
    return prop_str


def parse_cipher_selection(msg: str) -> Tuple[str, int]:
    """Parse server's response
    
    :param msg: server's message with the selected cryptosystem
    :return: (cipher_name, key_size) tuple extracted from the message
    """
    # raise NotImplementedError
    print(msg)
    msg_lst = msg.split(':')[1].split(',')
    print(msg_lst)
    cphr = msg_lst[0]
    if len(msg_lst) <= 2:
        k_size = int(msg_lst[1])
    return (cphr, k_size)


def generate_dhm_request(public_key: int) -> str:
    """Generate DHM key exchange request

    :param: client's DHM public key
    :return: string according to the specification
    """
    # raise NotImplementedError

    res = "DHMKE:" + str(public_key)
    return res


def parse_dhm_response(msg: str) -> int:
    """Parse server's DHM key exchange request
    
    :param msg: server's DHMKE message
    :return: number in the server's message
    """
    # raise NotImplementedError
    return int(msg.split(':')[1])


def get_key_and_iv(
    shared_key: str, cipher_name: str, key_size: int
) -> Tuple[object, bytes, bytes]:
    """Get key and IV from the generated shared secret key

    :param shared_key: shared key as computed by `diffiehellman`
    :param cipher_name: negotiated cipher's name
    :param key_size: negotiated key size
    :return: (cipher, key, IV) tuple
    cipher_name must be mapped to a Crypto.Cipher object
    `key` is the *first* `key_size` bytes of the `shared_key`
    DES key must be padded to 64 bits with 0
    Length `ivlen` of IV depends on a cipher
    `iv` is the *last* `ivlen` bytes of the shared key
    Both key and IV must be returned as bytes
    """
    # raise NotImplementedError
    cphr = cphr_map.get(cipher_name)
    key = shared_key[:key_size//8]
    if cipher_name == "DES":
        key += '\0'
    key = key.encode()
    iv = shared_key[-1 * iv_ln.get(cipher_name):].encode()
    return cphr, key, iv


def add_padding(message: str) -> str:
    """Add padding (0x0) to the message to make its length a multiple of 16
    
    :param message: message to pad
    :return: padded message
    """
    # raise NotImplementedError
    padding = len(message)
    while padding % 16 != 0:
        padding += 1
    padding -= len(message)
    res = message + '\0' * padding
    return res


def encrypt_message(message: str, crypto: object, hashing: object) -> Tuple[bytes, str]:
    """
    Encrypt the message

    :param message: plaintext to encrypt
    :param crypto: chosen cipher, must be initialized in the `main`
    :param hashing: hashing object, must be initialized in the `main`
    :return: (ciphertext, hmac) tuple

    1. Pad the message, if necessary
    2. Encrypt using cipher `crypto`
    3. Compute HMAC using `hashing`
    """
    # raise NotImplementedError
    message = add_padding(message)
    cipher_t= crypto.encrypt(bytes(message, 'utf-8'))
    hashing.update(cipher_t)
    hashvalue = hashing.hexdigest()
    return cipher_t, hashvalue


def main():
    """Main event loop

    See vpn.md for details
    """

    HOST = gethostname()
    PORT = 4600
    SUPPORTED_CIPHERS = {"AES": [128, 192, 256],"Blowfish": [112, 224, 448], "DES": [56]}



    client_sckt = socket(AF_INET, SOCK_STREAM)
    client_sckt.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")

    print("Negotiating the cipher")
    cipher_name = "CS"
    key_size = 460
    # Follow the description
    msg_out = generate_cipher_proposal(SUPPORTED_CIPHERS)
    client_sckt.send(msg_out.encode())
    msg_in = client_sckt.recv(4096)
    cipher_name, key_size = parse_cipher_selection(msg_in)
    print(f"We are going to use {cipher_name}{key_size}")

    print("Negotiating the key")
    # Follow the description
    dh = DiffieHellman()
    dh.generate_public_key()
    msg_out = generate_dhm_request(dh.public_key)
    client_sckt.send(msg_out.encode())
    msg_in = client_sckt.recv(4096).decode('utf-8')
    server_public_key = parse_dhm_response(msg_in)
    dh.generate_shared_secret(server_public_key)
    cipher, key, iv = get_key_and_iv(dh.shared_key, cipher_name, key_size)
    print("The key has been established")

    print("Initializing cryptosystem")
    # Follow the description
    crypto = cipher.new(key, cipher.MODE_CBC, iv)
    hashing = HMAC.new(key, digestmod=SHA256)
    print("All systems ready")

    while True:
        msg_out = input("Enter message: ")
        if msg_out == "\\quit":
            client_sckt.close()
            break
        cphr_out, hmac_out = encrypt_message(msg_out, crypto, hashing)
        client_sckt.send(cphr_out.encode()+ hmac_out.encode())
        msg_in = client_sckt.recv(4096)
        print(msg_in.decode("utf-8"))


    # client_sckt = socket(AF_INET, SOCK_STREAM)
    # client_sckt.connect((HOST, PORT))
    # print(f"Connected to {HOST}:{PORT}")

    # print("Negotiating the cipher")
    # # cipher_name = "CS"
    # # key_size = 460
    # msg_out = generate_cipher_proposal(SUPPORTED_CIPHERS)
    # client_sckt.send(msg_out.encode())
    # msg_in = client_sckt.recv(4096).decode('utf-8')
    # cipher_name, key_size = parse_cipher_selection(msg_in)
    # # Follow the description
    # print(f"We are going to use {cipher_name}{key_size}")

    # print("Negotiating the key")
    # # Follow the description
    # dh = DiffieHellman()
    # dh.generate_public_key()
    # msg_out = generate_dhm_request(dh.public_key)
    # client_sckt.send(msg_out.encode())
    # msg_in = client_sckt.recv(4096).decode('utf-8')
    # server_public_key = parse_dhm_response(msg_in)
    # dh.generate_shared_secret(server_public_key)
    # cipher, key, iv = get_key_and_iv(dh.shared_key, cipher_name, key_size)
    # print("The key has been established")

    # print("Initializing cryptosystem")
    # # Follow the description
    # crypto = cipher.new(key, cipher.MODE_CBC, iv)
    # hashing = HMAC.new(key, digestmod=SHA256)
    # print("All systems ready")

    # while True:
    #     msg_out = input("Enter message: ")
    #     if msg_out == "\\quit":
    #         client_sckt.close()
    #         break
    #     ciph_out, hmac_out = encrypt_message(msg_out, crypto, hashing)
    #     client_sckt.send(msg_out.encode())
    #     msg_in = client_sckt.recv(4096)
    #     print(msg_in.decode("utf-8"))


if __name__ == "__main__":
    main()
