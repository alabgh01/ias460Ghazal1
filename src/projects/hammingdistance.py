#!/usr/bin/env python3
"""
Hamming Distance Calculations for Pro9
"""
Alice = "0xBE439AD598EF5147"
bin_Alice = bin(int(Alice, 16))[2:].zfill(64)
Bob = "0x9C8B7A1425369584"
Charlie = "0x885522336699CCBB"

users = {"Uu" : "0xC975A2132E89CEAF",\
"Vu" : "0xDB9A8675342FEC15",\
"Wu" : "0xA6039AD5F8CFD965",\
"Xu" : "0x1DCA7A54273497CC",\
"Yu" : "0xAF8B6C7D5E3F0F9A"}

sums = {}
for i in users.values():
    bin_i = bin(int(i, 16))[2:].zfill(64)
    sum = 0
    for x, y in zip(list(bin_i), list(bin_Alice)):
        if x == y:
            sum += 1
    sums[i] = sum
mx = 0
winner = ""
for user, val in zip(sums.keys(), sums.values()):
    if val > mx:
        mx = val
        winner = user
for user, val in zip(users.keys(), users.values()):
    if val == winner:
        print(f"{user}: {val} is most likely to be Alice")

        
