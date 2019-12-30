+++
title = "HackToday 2018 - Kompeni Pemberantas Korupsi"
date = "2018-08-05 17:52:20"
categories = ["rev", "writeup"]
+++

> Downloads:
>
> [kpk](/assets/hacktoday/kpk/kpk)
>
> [draw_chess.py](/assets/hacktoday/kpk/draw_chess.py)
>
> [chess.png](/assets/hacktoday/kpk/chess.png)
>
> [chess.png.kpk](/assets/hacktoday/kpk/chess.png.kpk)
>
> [flag.png.kpk](/assets/hacktoday/kpk/flag.png.kpk)
>
> [flag_recovered.png](/assets/hacktoday/kpk/flag_recovered.png)
>
> [solver.py](/assets/hacktoday/kpk/solver.py)

Ada beberapa cara yang dapat dilakukan untuk solve problem seperti ini, yang agak lebih mudah yaitu melakukan blackbox dengan fuzzing file input dan check file output yang dihasilkan. Berikut contoh script untuk menghasilkan file input (PNG),

```python
from PIL import Image

width, height = (200, 200)

pixels = [(0,0,0) for i in range(width * height)]

img = Image.new('RGB', (width, height))
img.putdata(pixels)
img.save('input.png')
```

Perlu dilakukan beberapa validasi bagaimana binary memproses data PNG, untuk itu dapat dilakukan pengubahan pola warna input menjadi chess tiles atau yang lain.

```
... warna hitam
00000000  7f 4b 50 4b c8 00 00 00  c8 00 00 00 ff 00 00 00
00000010  ff 00 00 00 ff 00 00 00  ff 00 00 00 ff 00 00 00
... warna putih
00000000  7f 4b 50 4b c8 00 00 00  c8 00 00 00 ff ff ff ff
00000010  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff
... 253 more
```

Dari hasil tersebut, dapat disimpulkan `7f4b504b` `\x7FKPK` adalah file signature dan `c8...` `c8...` adalah size `(width * height)` dari file PNG (0xc8 == 200). Untuk warna dari file PNG, dapat diasumsikan ter-encode dalam __RLE__ (info didapat dari hint) tanpa ada pengubahan dalam proses membaca data pixel dari gambar (linear read). Dengan begitu, langkah terakhir hanya dibutuhkan script untuk inflate file menjadi raw pixels dan simpan dalam bentuk gambar berukuran (width, height). [Full solver](/assets/hacktoday/kpk/solver.py), 

```python
from PIL import Image
from struct import unpack

u32 = lambda x : unpack("<I", x)[0]
u8 = lambda x : unpack("<B", x)[0]
uRGB = lambda x : unpack("<BBB", x)

with open('flag.png.kpk', 'rb') as f:
    data = f.read()
    length = len(data)

assert(data[0:4] == "\x7FKPK")

width = u32(data[4:8])
height = u32(data[8:12])

pos = 12

pixels = []

while len(pixels) < width * height:
    rl = u8(data[pos:pos+1])
    for _ in range(rl):
        pixels.append(uRGB(data[pos+1:pos+4]))
    pos += 4

img = Image.new('RGB', (width, height))
img.putdata(pixels)
img.save('flag_recovered.png')
```

Hasilnya,
![flag.png](/assets/hacktoday/kpk/flag_recovered.png)