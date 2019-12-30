+++
title = "HackToday 2018 - not /a/game"
date = "2018-09-05 22:42:44"
categories = ["rev", "writeup"]
+++

> Downloads:
>
> [id.hacktoday.thisis.not.a.game.apk](/assets/hacktoday/notagame/id.hacktoday.thisis.not.a.game.apk)
>
> [solver.py](/assets/hacktoday/notagame/unluac.py)
> 
> [xxtea.py](/assets/hacktoday/notagame/xxtea.py)

```
cocos2dlua, Kill the Bug
```

## intro
Ada beberapa tahapan recon yang perlu dilakukan sebelum masuk ke reverse engineering. Judul sendiri sudah menjelaskan kalau aplikasi ini bukan game, dilihat dari jangka waktu lomba sendiri, tidak mungkin peserta memainkan sebuah game untuk mematikan serangga sebanyak 73311337 kali untuk mendapatkan flag. Meskipun sudah memakai program tambahan untuk _nge-cit_, flag tidak akan keluar (intended). Terus gimana?

## recon
Sedikit info dari hint dan skill gugel, cocos2dlua merupakan salah satu ___open source___ game engine yang lumayan banyak dipakai pada OS Android dan Kill the Bug meruapakan contoh sample project untuk game engine cocos2dlua ([cocos2d-x/cocos2d-x-samples](https://github.com/cocos2d/cocos2d-x-samples)). Sebagian isi dari APK sendiri secara singkat seperti berikut,
```
λ › ls -l assets/src/
total 20K
drwxr-xr-x  4 zero zero 4096 Sep  5 22:54 app
drwxr-xr-x 14 zero zero 4096 Sep  5 22:54 cocos
-rw-r--r--  1 zero zero  670 Dec 31  1979 config.luac
-rw-r--r--  1 zero zero  358 Dec 31  1979 main.luac
drwxr-xr-x  3 zero zero 4096 Sep  5 22:54 packages
λ › 
λ › hexdump -n 16 -C ./assets/src/config.luac
00000000  58 58 54 45 41 43 52 59  50 54 4b 43 12 4b 23 97  |XXTEACRYPTKC.K#.|
λ › hexdump -n 16 -C ./assets/src/main.luac
00000000  58 58 54 45 41 43 52 59  50 54 a4 61 43 31 00 f4  |XXTEACRYPT.aC1..|
λ › hexdump -n 16 -C ./assets/src/app/MyApp.luac
00000000  58 58 54 45 41 43 52 59  50 54 a9 b2 fa 7e df 4c  |XXTEACRYPT...~.L|
```
Oops, bukan plaintext lua yang didapat tapi beberapa file dengan header yang hampir sama. Header pada file ini sebenarnya adalah hint lanjutan dalam soal ini. `XXTEACRYPT` ini adalah salah satu jenis block crypto yang digunakan cocos2dlx-lua untuk enkripsi source code gamenya.

## reversing
Source code dari game ada di [https://github.com/cocos2d/cocos2d-x-samples/blob/v3/samples/KillBug/](https://github.com/cocos2d/cocos2d-x-samples/blob/v3/samples/KillBug/) karena mau fokus mencari bagaimana dekripsi dari file luac, yang perlu diperhatikan bukan di Java atau Lua, tapi implementasi di native C{,++} itu sendiri. Dengan _grep_-ing dengan keyword XXTEA, didapat bagian yang menarik, yakni [src](https://github.com/cocos2d/cocos2d-x-samples/blob/9f1472d9083a18853bb1fe97a337292f42abe44a/samples/KillBug/frameworks/runtime-src/Classes/AppDelegate.cpp#L67-L68)
```cpp
bool AppDelegate::applicationDidFinishLaunching()
{
    ...
    LuaStack* stack = engine->getLuaStack();
    stack->setXXTEAKeyAndSign("2dxLua", strlen("2dxLua"), "XXTEA", strlen("XXTEA"));
    ...
}
```
Dari sini sudah terlihat jelas bagaimana game mem-_prepare_ untuk mendekripsi luac. Dalam contoh diatas `2dxLua` adalah key untuk dekripsi luac. Lanjut ke analisa di APK sendiri, native-lib ada di `lib/armeabi-v7a/libcocos2dlua.so`,
```asm
.text:00AD2E00 ; AppDelegate::applicationDidFinishLaunching(void)
.text:00AD2E00                 EXPORT _ZN11AppDelegate29applicationDidFinishLaunchingEv
.text:00AD2E00 _ZN11AppDelegate29applicationDidFinishLaunchingEv
...
.text:00AD2E4E                 LDR             R1, [SP,#0xA0+var_48]
.text:00AD2E50                 STR             R0, [SP,#0xA0+var_64]
.text:00AD2E52                 MOV             R0, R1
.text:00AD2E54                 BLX.W           j__ZN7cocos2d9LuaEngine11getLuaStackEv ; cocos2d::LuaEngine::getLuaStack(void)
.text:00AD2E58                 STR             R0, [SP,#0xA0+var_50]
.text:00AD2E5A                 LDR             R0, [SP,#0xA0+var_50]
.text:00AD2E5C                 LDR             R1, [R0]
.text:00AD2E5E                 LDR             R1, [R1,#0x74]
.text:00AD2E60                 MOV             R2, SP
.text:00AD2E62                 MOV.W           LR, #0xA
.text:00AD2E66                 STR.W           LR, [R2,#0xA0+var_A0]
.text:00AD2E6A                 LDR             R2, =(aAkukamumemangj - 0xAD2E70)
.text:00AD2E6C                 ADD             R2, PC  ; "akukamumemangjos"
.text:00AD2E6E                 LDR.W           LR, =(aXxteacrypt - 0xAD2E76)
.text:00AD2E72                 ADD             LR, PC  ; "XXTEACRYPT"
.text:00AD2E74                 MOVS            R3, #0x10
.text:00AD2E76                 STR             R1, [SP,#0xA0+var_68]
.text:00AD2E78                 MOV             R1, R2
.text:00AD2E7A                 MOV             R2, R3
.text:00AD2E7C                 MOV             R3, LR
.text:00AD2E7E                 LDR.W           LR, [SP,#0xA0+var_68]
.text:00AD2E82                 BLX             LR
...
```
Terlihat familiar? kurang lebih dalam pseudo-C
```C
bool AppDelegate::applicationDidFinishLaunching(void)
...
stack = cocos::LuaEngine::getLuaStack();
*(stack + 0x74)(this???, "akukamumemangjos", 0x10, "XXTEACRYPT", 0xA);
...
```
yep, key untuk xxtea adalah `akukamumemangjos`. Langkah terakhir hanya perlu membuat solver untuk dekripsi file luac.

## solver
Full solver, implementasi xxtea di cocos2d-x bisa dilihat di [https://github.com/cocos2d/cocos2d-x-samples/blob/9f1472d9083a18853bb1fe97a337292f42abe44a/samples/SwiftTetris/cocos2d/external/xxtea/xxtea.cpp](https://github.com/cocos2d/cocos2d-x-samples/blob/9f1472d9083a18853bb1fe97a337292f42abe44a/samples/SwiftTetris/cocos2d/external/xxtea/xxtea.cpp)
```
#!/usr/bin/env python
import os
import argparse

from xxtea import decrypt, encrypt

parser = argparse.ArgumentParser(description='Decrypt/Encrypt XXTEA Block chiper recursively in a folder')
parser.add_argument("-d", "--dir", help="Input directory", required=True)
parser.add_argument("-k", "--key", help="Key for decryption", required=True)
parser.add_argument("-s", "--sign", help="File signature", required=True)
parser.add_argument("-o", "--out", help="Output directory")
parser.add_argument("-vv", "--verbose", help="Verbose output", action="store_true")
args = parser.parse_args()

curdir = args.dir

for file in os.listdir(curdir):
	curfile = curdir + '/' + file
	print('\n\n' + curfile + '\n\n')
	if not os.path.isdir(curfile):
		fp = open(curfile, 'rb')
		raw = fp.read()
		if raw[:len(args.sign)] == args.sign:
			print(decrypt(raw[len(args.sign):], args.key))
		else:
			print('Error!')
```
Quick run,
```
λ › python unluac.py -d assets/src/app/views/ -k akukamumemangjos -s XXTEACRYPT|grep Hack
       -- local flag = string.format("FLAG: HackToday{c0mpil3_to_byt3c0de_t0_rem0ve__d3bug_1nf0_1n_c0mment}")
```

## rants
Soal ini sebenernya dari pengalaman lama pribadi, lagi reversing game untuk belajar ~~cheat~~, eh, ketemu masalah file luac yang terenkripsi. Setelah berhasil dekripsi ternyata beberapa developer game (ini testing hampir ke semua top list di play store yang pakai game engine cocos2d-x lua) masih membiarkan beberapa debug info dan password untuk akses server db game. Baru sadar setelah lomba juga, writeup seperti ini sebenarnya udah pernah ditulis di blog lama, tapi kayanya juga udah hilang entah kemana tersisa hanya tulisan copy-paste dari orang lain.