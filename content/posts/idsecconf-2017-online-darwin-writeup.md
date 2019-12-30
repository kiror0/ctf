---
title: IDSECCONF 2017 Online - Darwin Writeup
date: 2017-12-12 20:02:30
categories:
- rev
- writeup
---

> Darwin (??? pts) [Download](https://a.safe.moe/Ph9RJ.zip) Reverse Engineering Mach-O executable

Diberikan sebuah binary Mach-O 32bit, langsung ke analisa binarynya

```C
signed int start()
{
  char v0; // al
  signed int result; // eax
  signed int v2; // [esp+44h] [ebp-44h]
  char v3[32]; // [esp+58h] [ebp-30h]
  int v4; // [esp+78h] [ebp-10h]

  memset(v3, 0, 0x20u);
  printf("Enter the key : ");
  fflush(__stdoutp);
  v2 = 0;
  fgets(v3, 32, __stdinp);
  while ( v2 < 32 )
  {
    v0 = 0;
    if ( v3[v2] == 10 )
      v0 = -10;
    v3[v2++] += v0;
  }
  if ( sub_1A30((int)v3) )
    printf("Congratz, the flag :\\nflag{yOu_%s_3v3r}\\n", v3);
  else
    printf("Wrong %s not the key.\\n", v3);
  result = 7566;
  if ( __stack_chk_guard == v4 )
    result = 0;
  return result;
}
```

Intinya, program meminta input dan melakukan pengecekan input pada fungsi sub_1A30.

```C
BOOL __cdecl sub_1A30(int a1)
{
  int v2; // [esp+1Ch] [ebp-5Ch]
  int v3; // [esp+20h] [ebp-58h]
  int v4; // [esp+2Ch] [ebp-4Ch]
  int v5; // [esp+30h] [ebp-48h]
  int v6; // [esp+34h] [ebp-44h]
  int v7; // [esp+38h] [ebp-40h]
  signed int k; // [esp+40h] [ebp-38h]
  int j; // [esp+44h] [ebp-34h]
  signed int i; // [esp+48h] [ebp-30h]
  int v11; // [esp+4Ch] [ebp-2Ch]
  int v12; // [esp+50h] [ebp-28h]
  int v13; // [esp+54h] [ebp-24h]
  int v14; // [esp+58h] [ebp-20h]
  int v15; // [esp+5Ch] [ebp-1Ch]
  int v16; // [esp+60h] [ebp-18h]
  int v17; // [esp+64h] [ebp-14h]
  signed int v18; // [esp+68h] [ebp-10h]

  v18 = strlen((const char *)a1);
  v17 = 0;
  v16 = 0;
  v15 = 0;
  v14 = 0;
  v13 = 0;
  v12 = 0;
  for ( i = 0; i < v18; ++i )
  {
    if ( i % 2 )
      v7 = *(char *)(a1 + i) ^ v14;
    else
      v7 = v14;
    v14 = v7;
    if ( i % 2 == 1 )
      v6 = v13;
    else
      v6 = *(char *)(a1 + i) ^ v13;
    v13 = v6;
    if ( i % 2 )
      v5 = 0;
    else
      v5 = *(char *)(a1 + i);
    v17 += v5;
    if ( i % 2 == 1 )
      v4 = *(char *)(a1 + i) ^ v15;
    else
      v4 = v15;
    v15 = v4;
  }
  for ( j = 0; j < v18 / 2; ++j )
    v12 ^= *(char *)(a1 + j);
  for ( k = 0; k < v18; ++k )
  {
    if ( k % 2 )
      v3 = *(char *)(a1 + k);
    else
      v3 = 0;
    v16 += v3;
    if ( k % 2 )
      v2 = v15;
    else
      v2 = *(char *)(a1 + k) ^ v15;
    v15 = v2;
  }
  v11 = sub_19C0(a1);
  return v17 % 10 == 8
      && v16 % 10 == v17 % 10
      && v18 == 13
      && v15 == 90
      && v12 == 21
      && v14 == 56
      && (v16 + v17) / 10 == 116
      && (v16 + 2 * v17) / 10 == 183
      && *(_BYTE *)(a1 + 1) == '3'
      && *(_BYTE *)(a1 + 5) == '5'
      && *(_BYTE *)(a1 + 8) == '4'
      && *(_BYTE *)(a1 + 10) == '7'
      && v11 == 0xFD4E6A44;
}
```

Dapat diketahui, panjang string input harus 13 karakter, dan input[1] == '3', input[5] == '5', input[8] == '4', input[10] == '7'.

```C
v18 = strlen((const char *)a1);
...
return ... && v18 == 13
... 
&& *(_BYTE *)(a1 + 1) == '3'
&& *(_BYTE *)(a1 + 5) == '5'
&& *(_BYTE *)(a1 + 8) == '4'
&& *(_BYTE *)(a1 + 10) == '7'
```

Nah, selebihnya dapat dianalisa lebih lanjut pada 3 loop-for di dapat,

```
v12 = input[0] ^ input[1] ^ input[2] ^ input[3] ^ input[4] ^ input[5]
v14 = input[1] ^ input[3] ^ input[5] ^ input[7] ^ input[9] ^ input[11]
v15 = input[0] ^ input[1] ^ input[2] ^ input[3] ^ input[4] ^ input[5] ^ input[6] ^ input[7] ^ input[8] ^ input[9] ^ input[10] ^ input[11] ^ input[12]
v12 == 21
v14 == 56
v15 == 90

v16 = input[0] + input[2] + input[4] + input[6] + input[8] + input[10] + input[12]
v17 = input[1] + input[3] + input[5] + input[7] + input[9] + input[11]
v17 % 10 == 8
v16 % 10 == v17 % 10
(v16 + v17) / 10 == 116
(v16 + 2 * v17) / 10 == 183
```

Nah, untuk mengetahui value pasti dari v17 dan v16 bisa dihitung manual,

```
v17 = ??8
v16 = ??8
...
v16 + 17 = 1166
v16 + 2*v17 = 1834
...
v16 == 668
v17 == 498
```

Lanjut untuk analisa value dari v11,

```C
int __cdecl sub_19C0(const char *a1)
{
  signed int i; // [esp+8h] [ebp-10h]
  int v3; // [esp+Ch] [ebp-Ch]
  signed int v4; // [esp+10h] [ebp-8h]

  v4 = strlen(a1);
  v3 = 23;
  for ( i = 0; i < v4; ++i )
    v3 = (a1[i] << i) + 7 * v3;   return v3 >> 4;
}
```

Ugh.. konstrain untuk flag sudah makin ribet. Langsung aja ke intinya, soal-soal tipe seperti ini bisa digunakan SMT solver seperti z3 dengan menambahkan constaraint-constaraint diatas, berikut kodenya

```python
from z3 import *

s = Solver()

str = [BitVec(i, 32) for i in xrange(13)]

for x in str:
    s.add(x >= 0x20, x <= 0x7e)

s.add(str[1] == ord('3'))
s.add(str[5] == ord('5'))
s.add(str[8] == ord('4'))
s.add(str[10] == ord('7'))

s.add(str[0] ^ str[1] ^ str[2] ^ str[3] ^ str[4] ^ str[5] == 21)
s.add(str[0] ^ str[1] ^ str[2] ^ str[3] ^ str[4] ^ str[5] ^ str[6] ^ str[7] ^ str[8] ^ str[9] ^ str[10] ^ str[11] ^ str[12] == 90)
s.add(str[1] ^ str[3] ^ str[5] ^ str[7] ^ str[9] ^ str[11] == 56)

s.add(str[0] + str[2] + str[4] + str[6] + str[8] + str[10] + str[12] == 668)
s.add(str[1] + str[3] + str[5] + str[7] + str[9] + str[11] == 498)

v3 = 23
for i, char in enumerate(str):
    v3 = ((char << i) + 7 * v3) & 0xffffffff v3 = (v3 >> 4) & 0xffffffff

s.add(v3 == 0xFD4E6A44)

if s.check() == sat:
    model = s.model()
    flag = [chr(model[x].as_long()) for x in str]
    print ''.join(flag)
else:
    print 'Nope :('
```

Jalankan kodenya, didapatkan flag,

FLAG : `flag{yOu_r3ver5eM4s7er_3v3r}`

* * *

Side note: tbh ini ngerjainnya semalam suntuk. Hanya karena tidak menggunakan python2 waktu mengerjakan. Kenapa pengaruh banget? Iya, ini serius, vm ctfbox yang dipakai default python diubah ke python3 dan entah kenapa pas menjalankan kodingan diatas selalu return unsatisfied :(. Udah beberapa jam tapi gak sadar juga, sampai akhirnya coba pakai python2 dan output dapat satisfied (yeay). Whats learned? Coba-coba baca issues di github kalau nge-stuck. Pakai python2 buat solve sesuatu berhubungan dengan z3/SMT solver lain. Original idea by Bang Alfan (http://maulvi-cs.blogspot.com/).