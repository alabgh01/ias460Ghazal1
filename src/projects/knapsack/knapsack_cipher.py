#!/usr/bin/env python3
"""
Merkle-Hellman Knapsack cipher implementation

@authors: 
@version: 2022.3
"""

import math
import pathlib
from pydoc import plain
import random

BLOCK_SIZE = 64



def generate_sik(size: int = BLOCK_SIZE) -> tuple[int, ...]:
    """
    Generate a superincreasing knapsack of the specified size

    :param size: block size
    :return: a superincreasing knapsack as a tuple
    """
    # TODO: Implement this function
    ...

    sum = 0
    sik = []
    for w in range(size):
        # for i in sik:
        # i = 0
        # if w > sum:
        #     i = w
        wi = random.randrange(sum+1, sum+10)
        sik.append(wi)
        # sum += i
        sum += wi
    return tuple(sik)


def calculate_n(sik: tuple) -> int:
    """
    Calculate N value

    N is the smallest number greater than the sum of values in the knapsack

    :param sik: a superincreasing knapsack
    :return: n
    """
    # TODO: Implement this function
    ...
    sik = list(sik)
    sum = 0
    for w in sik:
        sum += w
    # bg = []
    # for i in sik:
        # if i > sum:
            # bg.append(i)
    # sml = bg.min()
    # n = sml
    return sum+1
    

def calculate_m(n: int) -> int:
    """
    Calculate M value

    M is the largest number in the range [1, N) that is co-prime of N
    :param n: N value
    """
    # TODO: Implement this function
    ...
    # lrg = 0
    # for i in range(1,n-1):
    #     if 
    return n-1

def calculate_inverse(sik: tuple[int, ...], n: int = None, m: int = None) -> int:
    """
    Calculate inverse modulo

    :param sik: a superincreasing knapsack
    :param n: N value
    :param m: M value
    :return: inverse modulo i so that m*i = 1 mod n
    """
    # TODO: Implement this function
    ...

    nn = n
    if n == None:
        sum = 0
        for i in sik:
            sum += i
        return sum
    elif(n == 1):
        return 0

    x, lastX = 0, 1
    y, lastY = 1, 0
    while (n != 0):
        q = m // n
        m, n = n, m % n
        x, lastX = lastX - q * x, x
        y, lastY = lastY - q * y, y
    if(lastX < 0):
        lastX += nn
    return lastX

    # nn = n
    # if(n == None):
    #     sum = 0
    #     for i in sik:
    #         sum += i
    #     return sum
    # elif(n == 1):
    #     return 0
    # lastx, lasty = 1, 0
    # while(m > 1):
    #     dvd = m // n
    #     m, n = n, m % n
    #     lastx, lasty = lasty, lastx - dvd * lasty
    # if(lastx < 0):
    #     lastx += nn
    # return lastx


def generate_gk(sik: tuple[int, ...], n: int = None, m: int = None) -> tuple[int, ...]:
    """
    Generate a general knapsack from the provided superincreasing knapsack

    :param sik: a superincreasing knapsack
    :param n: N value
    :param m: M value
    :return: the general knapsack
    """
    # TODO: Implement this function
    ...
    if(n == None):
        n = calculate_n(sik)
        m = calculate_m(n)
    if(m == None):
        m = calculate_m(n)
    gk = []
    for w in range(len(sik)):
        gk.insert(w, sik[w]*m%n)
    return tuple(gk)



def encrypt(
    plaintext: str, gk: tuple[int, ...], block_size: int = BLOCK_SIZE
) -> list[int]:
    """
    Encrypt a message

    :param plaintext: text to encrypt
    :param gk: general knapsack
    :param block_size: size of the encryption block
    :return: encrypted text
    """
    # TODO: Implement this function
    ...
    if block_size != 64:
        bin_plain = "".join([bin(ord(x))[2:] for x in plaintext])
        block = gk[:block_size]
        bplain = [bin_plain[i:i + block_size] for i in range(0, len(bin_plain), block_size)]
        sum = []
        for i in bplain:
            if len(i) < len(block):
                i = i.zfill(len(block))
            summ = 0
            for j in range(len(block)):
                summ += int(i[j])*int(block[j])
            sum.append(summ)
        return(sum)
    else:
        bin_plain = "".join([bin(ord(x))[2:].zfill(8) for x in plaintext])
        sum = 0
        gki = len(gk) - 1
        bii = len(bin_plain) - 1
        while gki >=0:
            sum += int(bin_plain[bii])*gk[gki]
            gki -= 1
            bii -= 1
        return [sum]

    # bin_plain = "".join([bin(ord(x))[2:].zfill(8) for x in plaintext])

    # bin_plain = "".join([bin(ord(x))[2:] for x in plaintext])
    # print(len(gk), len(bin_plain), block_size)
    # if len(bin_plain) < len(gk):
    #     if block_size <= len(gk):
    #         bin_plain = bin_plain.zfill(len(gk))
    #         block = gk[:block_size]
    #         bplain = [bin_plain[i:i + block_size] for i in range(0, len(bin_plain), block_size)]
    #         sum = []
    #         for i in bplain:
    #             summ = 0
    #             for j in range(len(block)):
    #                 summ += int(i[j])*block[j]
    #             sum.append(summ)
    #         return(sum)
    #     else:
    #         sum = 0
    #         bin_plain = bin_plain.zfill(len(gk))
    #         for i in range(len(bin_plain)):
    #             sum += int(bin_plain[i])*gk[i]
    #         return [sum]
    # # elif len(bin_plain) == block_size:
    # #     block = []
    # #     for el in range(block_size):
    # #         block.append(gk[el])
    # #     sum = 0
    # #     for i in range(block_size):
    # #         sum += int(bin_plain[i])*int(block[i])
    # elif len(bin_plain) == len(gk):
    #     sum = 0
    #     for i in range(len(bin_plain)):
    #         sum += int(bin_plain[i])*gk[i]
    #     return [sum]

    
    # ogk = gk.copy()
    
    # suml = []
    
    # while len(gk) > 0:
    
    #     # blockgk = [0]*block_size
        
    #     bin_plain = bin_plain[len(suml):]
        
    #     blockgk = [gk[i:i + block_size] for i in range(0, len(gk), block_size)]
        
    #     if len(bin_plain) < len(blockgk[0]):
    #         break
        
    #     # for i in blockgk:
    #     sumblock = 0
    #     for j in range(len(blockgk[0])):
    #         sumblock += int(bin_plain[j])*int(blockgk[0][j])
            
    #     suml.append(sumblock)
            
            
            
        
    # return suml
    # if len(plaintext) == 1:
    #     bin_plain = bin(ord(plaintext))[2:].zfill(8) 

    # bin_plain = ("".join([bin(ord(x))[2:].zfill(8) for x in plaintext]))
    # bgsum = 0
    # st = 0
    # bls = block_size
    # for b in gk[st:bls]:
    #     sum = 0
    #     cs = bin_plain[st:bls]
    #     for i in range(len(cs)):
    #         res = int(cs[i])*gk[i]
    #         sum += res
    #     st, bls = bls, bls+bls
    #     bgsum += sum
    #     print(sum)
    # return [bgsum]
    # if len(plaintext) == 1:
    #     binary_val = []
    #     binary_val += bin(ord(plaintext))[2:].zfill(8)
    #     result = []
    #     res = 0
    #     gk_idx = len(gk) - 1
    #     bi_idx = len(binary_val) - 1
    #     while gk_idx >=0 and bi_idx >= 0:
    #         res += gk[gk_idx]*int(binary_val[bi_idx])
    #         gk_idx -= 1
    #         bi_idx -= 1
    #     result.append(res)
    # else:
    #     plaintext = list(plaintext)
    #     print(plaintext)
    #     print(len(plaintext))
    #     binary_val = []
    #     for i in range(len(plaintext)):
    #         # print(plaintext[i])
    #         binary_val += bin(ord(plaintext[i]))[2:].zfill(8)
    #         # binary_val.append(bin_plain)
    #         # print(binary_val)
    #         # print(gk[i])
    #     result = []
    #     res = 0
    #     gk_idx = len(gk) - 1
    #     bi_idx = len(binary_val) - 1
    #     # print(gk)
    #     # print(gk_idx, bi_idx)
    #     for i in plaintext:
    #         while gk_idx >=0 and bi_idx >= 0:
    #             res += gk[gk_idx]*int(binary_val[bi_idx])
    #             gk_idx -= 1
    #             bi_idx -= 1
    #         result.append(res)
        # while gk_idx >=0 and bi_idx >= 0:
        #     result.append(gk[gk_idx]*int(binary_val[bi_idx]))
        #     gk_idx -= 1
        #     bi_idx -= 1

    # x = 0
    # while x < len(binary_val) and x < len(gk):
    #     # result += gk[x]*int(binary_val[x]
    #     if binary_val[x] == "1":
    #         result += gk[x]
    #     x += 1

    # return result




def decrypt(
    ciphertext: list[int],
    sik: tuple[int, ...],
    n: int = None,
    m: int = None,
    block_size: int = BLOCK_SIZE,
) -> str:
    """
    Decrypt a single block
    
    :param ciphertext: text to decrypt
    :param sik: superincreasing knapsack
    :param n: N value
    :param m: M value
    :param block_size: block size
    :return: decrypted string
    """
    # TODO: Implement this function
    ...
    calc_cipher = ciphertext[0] * calculate_inverse(sik, n, m) % n
    li = len(sik) - 1
    sum = ""
    while li >= 0 and calc_cipher > 0:
        if calc_cipher >= sik[li]:
            sum = "1" + sum
            calc_cipher -= sik[li]
        else:
            sum = "0" + sum
        li -=1
    sum = chr(int(sum, 2))
    return sum

   


def main():
    """
    Main function
    Use your own values to check that functions work as expected
    You still need to rely on tests for proper verification
    """
    print("Hellman-Merkle example")
    

if __name__ == "__main__":
    main()
