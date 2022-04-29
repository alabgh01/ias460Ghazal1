#!/usr/bin/env python3
"""
passgen
"""

from flask import Flask, Response, jsonify, make_response, redirect, request
from flask_cors import CORS, cross_origin
from string import printable, punctuation, digits
import random
import math

app = Flask(__name__)
cors = CORS(app)

exclude = ["I", "O", "l", "|"]
al = list(printable[2:94])
for i in al:
    if i in exclude:
        al.remove(i)
lowerc = al[8:33]
upperc = al[33:56]
lowup = al[8:56]
spl = al[57:88]
prntbl = al[0:56]

@app.route("/api/psgn1/")
@cross_origin()
def hello_world():
    return "Hello, World!"

@app.route(f"/api/psgn1/digits/<int:ln>/<int:num>")
@cross_origin()
def digits(ln, num):
    res = {}
    for j in range(num):
        ps = ""
        for i in range(ln):
            ch = random.randint(2, 9)
            ps += str(ch)
        res[f"{ps}"] = int(calc_entropy(7,ln))
    return res

@app.route(f"/api/psgn1/lower/<int:ln>/<int:num>")
@cross_origin()
def lower(ln, num):
    res = {}
    for j in range(num):
        ps = ""
        for i in range(ln):
            idx = random.randint(0, len(lowerc)-1)
            ps += lowerc[idx]
        res[f"{ps}"] = int(calc_entropy(len(lowerc),ln))
    return res

@app.route(f"/api/psgn1/upper/<int:ln>/<int:num>")
@cross_origin()
def upper(ln, num):
    res = {}
    for j in range(num):
        ps = ""
        for i in range(ln):
            idx = random.randint(0, len(upperc)-1)
            ps += upperc[idx]
        res[f"{ps}"] = int(calc_entropy(len(upperc),ln))
    return res

@app.route(f"/api/psgn1/letters/<int:ln>/<int:num>")
@cross_origin()
def letters(ln, num):
    res = {}
    for j in range(num):
        ps = ""
        for i in range(ln):
            idx = random.randint(0, len(lowup)-1)
            ps += lowup[idx]
        res[f"{ps}"] = int(calc_entropy(len(lowup),ln))
    return res

@app.route(f"/api/psgn1/alphanum/<int:ln>/<int:num>")
@cross_origin()
def alphanum(ln, num):
    res = {}
    for j in range(num):
        ps = ""
        for i in range(ln):
            idx = random.randint(0, len(prntbl)-1)
            ps += prntbl[idx]
        res[f"{ps}"] = int(calc_entropy(len(prntbl),ln))
    return res

@app.route(f"/api/psgn1/special/<int:ln>/<int:num>")
@cross_origin()
def special(ln, num):
    res = {}
    for j in range(num):
        ps = ""
        for i in range(ln):
            idx = random.randint(0, len(spl)-1)
            ps += spl[idx]
        res[f"{ps}"] = int(calc_entropy(len(spl),ln))
    return res

@app.route(f"/api/psgn1/all/<int:ln>/<int:num>")
@cross_origin()
def all(ln, num):
    res = {}
    for j in range(num):
        ps = ""
        for i in range(ln):
            idx = random.randint(0, len(al)-1)
            ps += al[idx]
        res[f"{ps}"] = int(calc_entropy(len(al),ln))
    return res

@app.route(f"/api/psgn1/psphrs/<string:sprtr>/<int:ln>/<int:num>")
@cross_origin()
def psphrs(sprtr, ln, num):
    # open file to get words
    with open("../words") as f:
        lines = f.read().splitlines()
        res = {}
        for j in range(num):
            ps = ""
            for i in range(ln):
                idx = random.randint(0, len(lines)-1)
                ps += lines[idx] + sprtr
            res[f"{ps}"] = int(calc_entropy(len(lines),len(ps)))
        return res

def calc_entropy(l,ln):
    return math.log(l**ln, 2)

    
