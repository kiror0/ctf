+++
title = "TPCTF 2017 - Bad Encryption Writeup"
date = "2017-12-07 12:30:54"
categories = ["rev", "writeup"]
+++

> I was making an encryption program, but it is far from perfect. Instead of make the encryption work, I decided to just encrypt everything 100 times. Hint : I bet the encryption works at least most of the time.

Diberikan 2 file, yakni encode.py dan encoded.zip. Python : https://paste.safe.moe/erebibexes.coffee ZIP: https://a.safe.moe/qUbq4.zip (md5sum 15906c946870428ba60f88bae2e679f3) Unzip file encoded.zip, akan didapat file out[0-99].png. Lalu, analisa file encode.py,

```python
#!/usr/bin/env python2

for i in range(1,101):
    tel1l1l1l1l1l1l1lt = "REDACTED"
    import builtins, random
    l1l1l1l1l1l1l1l = getattr(builtins, "__import__")
    l1l1l1l1l1l1l1l = l1l1l1l1l1l1l1l("PIL.Image")
    l1l1l1l1l1l1l1ll1l1l1l1l1l1l1l = l1l1l1l1l1l1l1l.Image
    l1l1l1l1l1l1l1ll1l1l1l1l1l1l1ll1l1l1l1l1l1l1l = l1l1l1l1l1l1l1ll1l1l1l1l1l1l1l.new("RGB", (len(tel1l1l1l1l1l1l1lt), 1), "white")
    l1l1l1l1l1l1l1ll1l1l1l1l1l1l1ll1l1l1l1l1l1l1ll1l1l1l1l1l1l1l = l1l1l1l1l1l1l1ll1l1l1l1l1l1l1ll1l1l1l1l1l1l1l.load()
    l1l1l1l1l1l1l1ll1l1l1l111l1l11 = 0
    for l1l1l1l1l1l1l1ll1l1l1l1l1l1l11 in tel1l1l1l1l1l1l1lt:
        l1l1l1l1l1l1l1ll1l1l1l1l1l1l11 = ord(l1l1l1l1l1l1l1ll1l1l1l1l1l1l11)
        l1l1l1l1l1l1l1ll1l1l1l1lll1l111 = random.randint(1,256)
        l1l1l1l1l1l1l1ll1l1l1l1lll1l112 = random.randint(1,256)
        l1l1l1l1l1l1l1ll1l1l1l1lll1l113 = random.randint(1,256)
        l1l1l1l1l1l1l11ll1l1l1l1lll1l111 = (l1l1l1l1l1l1l1ll1l1l1l1lll1l111/256)
        l1l1l1l1l1l1l11ll1l1l1l1lll1l112 = (l1l1l1l1l1l1l1ll1l1l1l1lll1l112/256)
        l1l1l1l1l1l1l11ll1l1l1l1lll1l113 = (l1l1l1l1l1l1l1ll1l1l1l1lll1l113/256)
        l1l121l1l1l1l11ll1l1l1l1lll1l111 = l1l1l1l1l1l1l1ll1l1l1l1l1l1l11*l1l1l1l1l1l1l11ll1l1l1l1lll1l111
        l1l121l1l1l1l11ll1l1l1l1lll1l112 = l1l121l1l1l1l11ll1l1l1l1lll1l111*l1l1l1l1l1l1l11ll1l1l1l1lll1l112
        l1l1l1l1l1l1l1ll1l1l1l1l1l1l1ll1l1l1l1l1l1l1ll1l1l1l1l1l1l1l[l1l1l1l1l1l1l1ll1l1l1l111l1l11,0] = (l1l1l1l1l1l1l1ll1l1l1l1lll1l111, l1l1l1l1l1l1l1ll1l1l1l1lll1l112, round(l1l121l1l1l1l11ll1l1l1l1lll1l112*10))
        l1l1l1l1l1l1l1ll1l1l1l111l1l11 += 1
    l1l1l1l1l1l1l1ll1l1l1l1l1l1l1ll1l1l1l1l1l1l1l.save("out"+str(i)+".png")
```

Ugh.. Variabelnya agak sedikit membingunkan, coba diperbaiki sedikit, hasilnya

```python
for i in range(1,101):
    realflag = "REDACTED"
    import builtins, random
    _import = getattr(builtins, "__import__")
    _import = _import("PIL.Image")
    _PIL_image = _import.Image
    _new_image = _PIL_image.new("RGB", (len(realflag), 1), "white")
    _image_pixels = _new_image.load()
    pos = 0
    for i in realflag:
        i = ord(i)
        rand1 = random.randint(1,256)
        rand2 = random.randint(1,256)
        rand3 = random.randint(1,256)
        rand1div = (rand1/256)
        rand2div = (rand2/256)
        rand3div = (rand3/256)
        _k = i*rand1div
        _k = _k*rand2div
        _image_pixels[pos,0] = (rand1, rand2, round(_k*10))
        pos += 1
    _new_image.save("out"+str(i)+".png")
```

Dari kode tersebut dapat diketahui `realflag` dienkripsi dengan

$$ enc[i] = round(realflag[i] \times \frac{rand1}{256} \times \frac{rand2}{256} \times 10)&bg=1b1b1b&s=2 $$

dan disimpan kedalam file out[0-99].png pada nilai pixel BLUE. Nah, rand1 dan rand2 sendiri terdapat pada nilai pixel RED dan GREEN. Ada hal yang menarik dari cara enkripsi ini. Pada enkripsi, digunakan fungsi round() yang dapat memiliki 'dualisme nilai' atau nilai yang biasa saya sebut 'off-by-one'. Seperti yang tertera pada hint, 'I bet the encryption works at least most of the time', enkripsi ini diperkirakan bisa saja gagal. Salah satu cara untuk mengembalikan flag adalah dengan bruteforce printable character satu per satu dan membandingkan hasilnya dengan enc[i], namun karena disini enkripsinya bisa saja gagal maka, diperlukan tabel frekuensi seringnya muncul dari hasil enkripsi karakter tersebut. Nah, flagnya sendiri bisa jadi didapat dari karakter dengan kemunculan terbanyak. Berikut script python-nya,

```python
import PIL.Image

alpha = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}_!@#$%^&*()_+:;[]|<>,./?'
flag = ''
# image.w = 38; image.h = 1
freq = [[0 for c in xrange(len(alpha))] for r in xrange(38)]

for i in range(1, 101):
    image = PIL.Image.open('encode/out%s.png' % i)
    w = image.width
    h = image.height # always 1
    pixels = image.load()
    for pos in xrange(w):
        rand1, rand2, enc = pixels[pos, 0]
        for a in xrange(len(alpha)):
            if round(ord(alpha[a])*rand1*rand2*10/0x10000) == enc:
                freq[pos][a] += 1

for pos in xrange(w):
    flag += alpha[ freq[pos].index( max( freq[pos]) ) ]
print flag
```

Setelah dijalankan, didapat hasil `uqdtf{i_c4ou_7h1ok_0f_a_gUnoy_f14g_:(}` Hmm.. formatnya mirip flag tapi masih salah :(. Nah, disinilah kenapa disebut tadi 'off-by-one'. uqdtf -> tpctf, terlihat jelas untuk beberapa kasus, frekuensi karakter yang muncul ternyata lebih banyak atau sama dengan karakter setelah huruf tersebut.

`t -> u`

`p -> q`

`c -> d`

...

Agak dibenerin sedikit karakternya supaya bisa terbaca dan 'make sense' saat diartikan dengan cara nge-dukun, didapat flag `tpctf{i_c4nt_7h1nk_0f_a_fUnny_f14g_:(}`

FLAG : `tpctf{i_c4nt_7h1nk_0f_a_fUnny_f14g_:(}`