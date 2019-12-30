+++
title = "CTFZone 2018 Quals - android_ololo_country_checker"
date = "2018-07-23 08:21:09"
categories = ["rev", "writeup"]
+++

> It's a foreign android application. Let's try to guess the country!
> <br>Solves : 9
> <br>Point : 314. (Dynamic Score)
> <br>Download : 
> <br>- [ololo.8ed245a0a90f801ebf8ccf0676564ff1](https://ctf.bi.zone/files/ololo.8ed245a0a90f801ebf8ccf0676564ff1)
> <br>- [native-lib.c](/img/ctfzone2018/native-lib.c)
> <br>- [MainActivity.java](/img/ctfzone2018/MainActivity.java)

```sh
λ › file ololo.8ed245a0a90f801ebf8ccf0676564ff1
ololo.8ed245a0a90f801ebf8ccf0676564ff1: Zip archive data, at least v?[0] to extract
λ › jarsigner -verify ololo.8ed245a0a90f801ebf8ccf0676564ff1

jar is unsigned.
λ › unzip -l ololo.8ed245a0a90f801ebf8ccf0676564ff1
Archive:  ololo.8ed245a0a90f801ebf8ccf0676564ff1
  Length      Date    Time    Name
---------  ---------- -----   ----
     2592  00-00-1980 00:00   AndroidManifest.xml
       87  00-00-1980 00:00   META-INF/MANIFEST.MF
    15804  00-00-1980 00:00   classes.dex
    36184  00-00-1980 00:00   lib/armeabi-v7a/libnative-lib.so
     2192  00-00-1980 00:00   res/layout/activity_main.xml
   473197  00-00-1980 00:00   res/raw/a123hj1sa.png
   457171  00-00-1980 00:00   res/raw/hjdsajg12.png
   578662  00-00-1980 00:00   res/raw/j4321saa.png
   576558  00-00-1980 00:00   res/raw/kj1234c1.png
   388063  00-00-1980 00:00   res/raw/kjwqre32.png
   578662  00-00-1980 00:00   res/raw/mvke321kjd.png
     1856  00-00-1980 00:00   resources.arsc
---------                     -------
  3111028                     12 files
```

APK is unsigned, thus we need to sign the APK first if we're going to do dynamic analysis. There are many ways to do this, Google it. There is another thing important to note, the native-lib is __armeabi-v7a__ specific, it's better to have a phone support that CPU or use AVD emulator (comes with Android SDK) with armeabi-v7a system image.

Decompile classes.dex, use `apktool` for make changes to `*.smali` and `cfr` for decompile jar to java, easier to read than smali if you're not familiar with it.

```java
/* See attachment above (MainActivity.java) */
```

We will focus on 2 functions, `checkSomethings(int var1)` dan `getSoBody()`.

`getSoBody()`, unpack partial data from raw resource. The starting point is written at the end of file. Take a look at example,
```sh
λ › hexdump -C ./res/raw/a123hj1sa.png
...
00060e60  4e ff ff ec df cf fe fd  ec df cf fe fd ec df ff  |N...............|
00060e70  74 ff 7e 46 d0 3f fb f7  b3 7f 3f fb f7 b3 7f ff  |t.~F.?....?.....|
00060e80  53 fe 33 fb 1f f1 cd 56  d2 67 53 4d 99 00 00 00  |S.3....V.gSM....|
00060e90  00 49 45 4e 44 ae 42 60  82 dc 16 51 e9 90 1f da  |.IEND.B`...Q....|
00060ea0  fd 79 76 3f 27 f3 01 5e  09 9c 33 64 c8 0f 81 46  |.yv?'..^..3d...F|
00060eb0  9e 76 fb 77 ed fa b2 e2  05 97 4b c9 80 fe 2f bc  |.v.w......K.../.|
00060ec0  03 3d 57 3c d6 1c 20 61  97 6c e5 a3 2a fe 95 ed  |.=W<.. a.l..*...|
...
00073850  a3 af 0c d5 e3 59 d7 3f  f7 ea 5e b2 bd 7e f4 cc  |.....Y.?..^..~..|
00073860  9e 68 3e 77 ac bb 21 d1  46 99 0e 06 00           |.h>w..!.F....|
```
`IEND ?? ?? ?? ??` this is the signature for the end of PNG file, but there are still many trailing data following it. Assume this data is important for later, let's make a script to unpack it.
```python
from struct import unpack
import sys

u32 = lambda x : unpack("I", x)[0]

for i in range(1, len(sys.argv)):
    if sys.argv[i] == sys.argv[0]:
        continue

    basename = sys.argv[i].split('.')[0]
    
    with open(sys.argv[i], 'rb') as f:
        data = f.read()
        length = end = len(data)
    
    start = u32(data[length-4:length])
    
    with open(basename + '.bin', 'wb') as f:
        f.write(data[start:end-4])
```
```sh
λ › for i in $(ls ./res/raw | grep .bin); do; echo $i $(cat $i | wc -c); done
a123hj1sa.bin 76240
hjdsajg12.bin 76240
j4321saa.bin 76240
kj1234c1.bin 76240
kjwqre32.bin 76240
mvke321kjd.bin 76240
```
Okay, this is getting interesting. The data we have are the same size, moreover it's a multiples of 16 `(76240 % 16 == 0)`. The fact that all the data dosn't make sense, we can assume that we are dealing with some sort of block cipher later.

`checkSomethings(int var1)` is a native function, so we have to open libnative-lib.so in disassembler/decompiler.

```C
/* See attachment above (native-lib.c) */
```
Woa. this. is. huge. The actual deompiled from IDA doesn't have all these nice variables and functions name. The first thing I did was reading it from the bottom part. The last function before return called piqued my interest, because it calls `getSoBody()` and `getSoPath()` from java, after that, the data returned from `getSoBody()` passed to another function. The function use some constant which you can guess, sbox from AES. So, we know that the app uses AES to decrypt data from raw resource, but what about the keys?

The keys are crc32 calculated from some ID in android (`Line1Number`, `deviceID`, `subscriberID`, `packageName`, `sdk_ver`, `simCountryISO`). The hint for correct string are md5sum in `.data` section (`byte_XXXX`). You can see that in `checkSomethings(int)`
```C
while ( md5_deviceID[v57] == byte_9729[v57] )
{
  v39 = __OFSUB__(v57, 14);
  v37 = v57 == 14;
  v38 = v57++ - 14 < 0;
  if ( !((unsigned __int8)(v38 ^ v39) | v37) )
  {
    dword_9AA8[4] |= 1u;
    break;
  }
}
```
Looking up the hash value online, we could know what's the correct strings.
```
phone    = 8203412(03bec67d849e7114f1a828e1628495fe)/7793952(c377ec2ae9bc906448b6c39326e42f04)
deviceID = 89123988(e176e3acf427e59308520009b3e2a793)/01982375(b400b6e082104ce63f18f45e64c2fbfd)
iso_code = KZ(4aceb7d6b4564ec96bc6605cd5af37e7)/KG(56d721ccadb8bbfd8b47390d82a6ea4b)
subscriberID = 31231712(5b529e731eab2fb96185b0e9769fc498)
sdk_ver  = 19(1f0e3dad99908345f7439f8ffabdffc4)
package_name = ololo.ololo.ololo(5b4802bc02112666dabafe0c77ac18d0)
```
There's a problem though, assuming all of it as correct, some calculated md5 are checked 2 times, which means there will be 2 options for the correct string. From this point static analysis just getting hazy. Thus, i just decided to use all the possible options. There are only 3 ID with 2 options, (`2*2*2 = 8`) which will ends up with 8 possible combination, enough to do it by hands xD.

Rather than directly modify smali files (It'll took too much time since you'll need to modify, recompile, sign, and install. again and again), It's better to use things like `xposed` or `frida`. I used frida because it's easy to setup in emulator. Here's the final frida script,

```javascript
Java.perform(function () {
    const JavaString = Java.use('java.lang.String');
    var EADB = Java.use("aaa.aie.eadb");
    EADB.headb.implementation = function () {
        console.log("Called - aaa.aib.aib()");
        return false;
    }
    var EKPN = Java.use("aaa.aie.ekpn"); // PhoneNumber
    EKPN.egln.implementation = function () {
        console.log("Called - aaa.aie.ekpn.egln()");
        // return "7793952";
        return "8203412";
    };
    var EKD = Java.use("aaa.aie.ekd"); // DeviceId
    EKD.egdi.implementation = function () {
        console.log("Called - aaa.aie.ekd.egdi()");
        return "89123988";
        // return "01982375";
    };
    var EKL = Java.use("aaa.aie.ekl"); // SimIsoCountry
    EKL.egsci.implementation = function () {
        console.log("Called - aaa.aie.ekl.egcsi()");
        return "KZ";
        // return "KG";
    }
    // var EKA = Java.use("aaa.aie.eka");
    // EKA.ega.implementation = function () {
    //     console.log("Called - aaa.aie.eka.ega()");
    //     return JavaString.$new("19");
    // }
    // EKA.egn.implementation = function () {
    //     console.log("Called - aaa.aie.eka.egn()");
    //     return "ololo.ololo.ololo";
    // }
    var EKI = Java.use("aaa.aie.eki");
    EKI.egsi.implementation = function () {
        console.log("Called - aaa.aie.eki.egsi()");
        return "31231712";
    }
    Java.choose("ololo.ololo.ololo.MainActivity", {
        onMatch : function(instance) {
            instance.e.value = 0;
            instance.c.value = 0;
        },
        onComplete : function () {}
    });
});
```

Run the app, attach frida with the script above, boom, got the flag,

![](/img/ctfzone2018/ololo1.png)
![](/img/ctfzone2018/ololo2.png)

<center>`FLAG : ctfzone{1t_1s_0l0l0_g00d_4tt6mpt}`</center>

----------------------

Some notes and failed attack ideas. The first approach was static analysis and rewrite all of important function in C to decrypt raw data. The result? It fails miserably, it took me 1 hour to get to know frida and the flag, while rewrite took me 8 hours (8 hours of coding, mostly contemplating and asking what the fck am I doing for of not getting any progress. sad.) While the first reverse engineer part (decompile, analysis, and stuff) took me 1-2 hours. Yep, better to get another unique ideas if you are stuck for a long time. ~~but how? idk. sad.~~