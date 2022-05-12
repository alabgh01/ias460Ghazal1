#!/usr/bin/env python3
# encoding: UTF-8

from socket import socket, gethostname
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from typing import Tuple, Dict
from Crypto.Hash import SHA256, HMAC
from Crypto.Cipher import AES, DES, Blowfish
from diffiehellman.diffiehellman import DiffieHellman

cphr_map = {"DES": DES, "AES": AES, "Blowfish": Blowfish}
iv_ln = {"DES": 8, "AES": 16, "Blowfish": 8}

def parse_proposal(msg: str) -> Dict[str, list]:
    """Parse client's proposal
    
    :param msg: message from the client with a proposal (ciphers and key sizes)
    :return: the ciphers and keys as a dictionary
    """
    # raise NotImplementedError
    res = {}
    msg = msg[16:]
    cphr_nm = ''
    k_size = ''
    k_lst = []
    for m in msg:
        if m.isalpha():
            cphr_nm += m
        elif m.isalnum():
            k_size += m
        elif m == ',':
            if last_c.isalnum():
                k_lst.append(int(k_size))
                k_size = ''
        elif m == ']':
            k_lst.append(int(k_size))
            k_size = ''
            res[cphr_nm] = k_lst
            cphr_nm = ''
            k_lst = []
        last_c = m
    return res


def select_cipher(supported: dict, proposed: dict) -> Tuple[str, int]:
    """Select a cipher to use
    
    :param supported: dictionary of ciphers supported by the server
    :param proposed: dictionary of ciphers proposed by the client
    :return: tuple (cipher, key_size) of the common cipher where key_size is the longest supported by both
    :raise: ValueError if there is no (cipher, key_size) combination that both client and server support
    """
    # raise NotImplementedError
    ciphers = set(supported.keys()).intersection(proposed.keys())
    cphr = None
    k_size = -1
    if ciphers != set():
        for c in ciphers:
            crnt_k_size = max(set([-1]).union(set(supported.get(c)).intersection(proposed.get(c))))
            if crnt_k_size > k_size:
                k_size = crnt_k_size
                cphr = c
    if (not cphr) or (k_size == -1):
        raise ValueError(
            'Could not agree on a cipher')
    return (cphr, k_size)


def generate_cipher_response(cipher: str, key_size: int) -> str:
    """Generate a response message
    
    :param cipher: chosen cipher
    :param key_size: chosen key size
    :return: (cipher, key_size) selection as a string
    """
    # raise NotImplementedError
    return f"ChosenCipher:{cipher},{key_size}"


def parse_dhm_request(msg: str) -> int:
    """Parse client's DHM key exchange request
    
    :param msg: client's DHMKE initial message
    :return: number in the client's message
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
    cphr = cphr_map[cipher_name]
    key = shared_key[:key_size//8]
    if cipher_name == "DES":
        key += '\0'
    key = key.encode()
    iv = shared_key[-1 * iv_ln[cipher_name]:].encode()
    return cphr, key, iv


def generate_dhm_response(public_key: int) -> str:
    """Generate DHM key exchange response
    
    :param public_key: public portion of the DHMKE
    :return: string according to the specification
    """
    # raise NotImplementedError
    return f'DHMKE:{public_key}'


def read_message(msg_cipher: bytes, crypto: object) -> Tuple[str, str]:
    """Read the incoming encrypted message
    
    :param msg_cipher: encrypted message from the socket
    :crypto: chosen cipher, must be initialized in the `main`
    :return: (plaintext, hmac) tuple
    """
    # raise NotImplementedError
    cphr_in = msg_cipher[:-64]
    hmac = msg_cipher[-64:].decode('utf-8')
    plain = crypto.decrypt(cphr_in).decode('utf-8')
    plain = plain.strip('\0')
    return (plain, hmac)


def validate_hmac(msg_cipher: bytes, hmac_in: str, hashing: object) -> bool:
    """Validate HMAC
    
    :param msg_cipher: encrypted message from the socket
    :param hmac_in: HMAC received from the client
    :param hashing: hashing object, must be initialized in the `main`
    :raise: ValueError is HMAC is invalid
    """
    # raise NotImplementedError
    cphr = msg_cipher[:-64]
    hashing.update(cphr)
    hsh = hashing.hexdigest()
    if hsh == hmac_in:
        return True
    else:
        raise ValueError('Bad HMAC')


def main():
    """Main loop

    See vpn.md for details
    """

    HOST = gethostname()
    PORT = 4600

    server_sckt = socket(AF_INET, SOCK_STREAM)
    server_sckt.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_sckt.bind((HOST, PORT))
    server_sckt.listen()
    print(f"Listening on {HOST}:{PORT}")
    conn, client = server_sckt.accept()
    print(f"New client: {client[0]}:{client[1]}")

    print("Negotiating the cipher")
    cipher_name = "CS"
    key_size = 460
    # Follow the description
    print(f"We are going to use {cipher_name}{key_size}")

    print("Negotiating the key")
    # Follow the description
    print("The key has been established")

    print("Initializing cryptosystem")
    # Follow the description
    print("All systems ready")

    while True:
        msg_in = conn.recv(4096).decode("utf-8")
        if len(msg_in) < 1:
            conn.close()
            break
        print(f"Received: {msg_in}")
        msg_out = f"Server says: {msg_in[::-1]}"
        conn.send(msg_out.encode())


if __name__ == "__main__":
    main()
