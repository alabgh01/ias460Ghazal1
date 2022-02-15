#!/usr/bin/env python3
# encoding: UTF-8
# Auther: Ghazal Alabtah

# python code to run password decryption scripts

import os
import re

# word from zip
pswrdOrgnl = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et dui eu libero fringilla facilisis. Aenean porttitor, tellus ut posuere sagittis, quam turpis fringilla elit, quis tincidunt est leo at quam. Quisque consectetur enim ipsum, at consequat tortor ullamcorper id. Donec in venenatis nisl. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Sed vulputate, eros at bibendum mollis, erat sem semper lectus, ac interdum neque nunc ut velit. Praesent commodo turpis arcu, non viverra tortor consectetur nec. Ut euismod at velit sit amet faucibus. Praesent eleifend pellentesque pellentesque. Vivamus sed condimentum purus. Suspendisse ultrices luctus eleifend. Curabitur sodales purus vitae tellus pulvinar, at euismod elit congue. Vestibulum vitae euismod mi. In ornare eros tellus, quis efficitur eros mattis vel. Nam risus enim, convallis eget sem eu, luctus sagittis ex. Integer tristique tellus ac purus fermentum, vel accumsan felis finibus."
# erase punc marks
pswrd = re.sub(r'[^\w\s]', '', pswrdOrgnl)
# change to list
pswrdList = pswrd.split()

#loop through each file and try each word of the password list
f2 = "src/projects/whenami/secret.2"
for ps in pswrdList:
    os.system(f"7z x {f2} -p{ps}")
f3 = "src/projects/whenami/secret.3"
for ps in pswrdList:
    os.system(f"7z x {f3} -p{ps}")
f4 = "src/projects/whenami/secret.4"
for ps in pswrdList:
    os.system(f"7z x {f4} -p{ps}")
f5 = "src/projects/whenami/secret.5"
for ps in pswrdList:
    os.system(f"7z x {f5} -p{ps}")
f6 = "src/projects/whenami/secret.6"
for ps in pswrdList:
    os.system(f"7z x {f6} -p{ps}")