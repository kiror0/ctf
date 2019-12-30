+++
title = "Security Fest CTF 2018 - bluepill"
date = "2018-06-02"
categories = ["rev", "writeup"]
+++

> This your last chance. After this there is no turning back. You take the blue pill, the story ends. You wake up in your bed and believe whatever you want to. You take the red pill, you stay in Wonderland, and I show you how deep the rabbit hole goes. Remember, all I'm offering is the truth. Nothing more. This challenge was sponsored by ATEA! If you are a local student player you are eligible to turn in the flag at the ATEA booth for a prize!
>
> Solves: 27
>
> Service: nc rev.trinity.neo.ctf.rocks 31337 or nc 209.97.136.62 31337
>
> Download: bluepill.tar.gz

```sh
$ tar xvf bluepill.tar.gz
bluepill.ko
init
run.sh
tiny.kernel
$ file bluepill.ko
bluepill.ko: ELF 64-bit LSB relocatable, x86-64, version 1 (SYSV), BuildID[sha1]=3e46a2d1b5659bcf7947bb4ec5c11d2226289df1, not stripped
$ cat run.sh
#! /usr/bin/env bash

qemu-system-x86_64 -kernel ./tiny.kernel -initrd ./init -m 32 -nographic -append "console=ttyS0"
```

An unique one i guess, it's rare to see a kernel problem on reversing category but the goal is clear, we have to reverse engineer the kernel module.

```c
int __cdecl bluepill_init()
{
  signed __int64 v0; // rcx
  file_operations *v1; // rdi

  printk("\x016[BLUEPILL] Loaded ...\n");
  v0 = 62LL;
  v1 = &fops_35702;
  while ( v0 )
  {
    LODWORD(v1->owner) = 0;
    v1 = (file_operations *)((char *)v1 + 4);
    --v0;
  }
  fops_35702.write = (ssize_t (*)(file *, const char *, size_t, loff_t *))pill_choice;
  proc_create("bluepill", 0666LL, 0LL, &fops_35702);
  return 0;
}
```

So, kernel module create a rw (0666) proc at `/proc/bluepill`, with `write` routine at `pill_choice`.

```c
size_t __fastcall pill_choice(file *sp_file, const char *buf, size_t size, loff_t *offset)
{
  size_t v4; // r12
  file *v5; // rax
  file *v6; // rbx
  file *v7; // rdi
  const unsigned __int8 *v8; // rbx
  char *v9; // r13
  __int64 v10; // rbp
  int v11; // eax
  unsigned int v12; // edx
  signed __int64 v13; // rdi
  _QWORD *v14; // rcx
  __int64 v15; // rax
  _QWORD *i; // rdx
  unsigned __int8 digest[8]; // [rsp+7h] [rbp-59h]
  __int64 v19; // [rsp+Fh] [rbp-51h]
  __int64 s2; // [rsp+17h] [rbp-49h]
  char v21; // [rsp+1Fh] [rbp-41h]

  v4 = strncpy_from_user(&user_input, buf, 20LL, offset);
  v5 = file_open("/proc/version");
  if ( v5 )
  {
    v6 = v5;
    file_read(v5, (unsigned __int8 *)magic, 0x1F4u);
    v7 = v6;
    v8 = &user_input;
    filp_close(v7, 0LL);
    if ( strlen((const char *)&user_input) > 0xB )
    {
      v9 = const_bss;
      while ( 1 )
      {
        v10 = 0LL;
        memset(&v21, 0, 0x19uLL);
        *(_QWORD *)digest = 0LL;
        v19 = 0LL;
        s2 = 0LL;
        calc(v8, 4uLL, digest);
        do
        {
          v11 = magic[v10];
          v12 = digest[v10];
          v13 = 2 * v10++;
          sprintf((char *)&s2 + v13, "%02x", v11 ^ v12);
        }
        while ( v10 != 16 );
        if ( memcmp(v9, &s2, 0x20uLL) )
          break;
        v8 += 4;
        v9 += 0x21;
        if ( v8 == &user_input + 12 )
        {
          printk("\x011[BLUEPILL] You made the right choice! Now see the world for what it really is ..................... !\n");
          v14 = &init_task;
          while ( 1 )
          {
            v15 = v14[58];
            v14 = (_QWORD *)(v15 - 0x1D0);
            if ( (_UNKNOWN *)(v15 - 0x1D0) == &init_task )
              break;
            if ( v15 + 192 != *(_QWORD *)(v15 + 192) )
            {
              for ( i = *(_QWORD **)(v15 + 192); (_QWORD *)(v15 + 192) != i; i = (_QWORD *)*i )
              {
                if ( *(_DWORD *)(i[36] + 4LL) == 1337 )
                  i[36] = *(_QWORD *)(v15 + 496);
              }
            }
          }
          return v4;
        }
      }
    }
  }
  printk("\x011[BLUEPILL] Morpheus sighs loudly .................................................................. \n");
  return v4;
}
```

Here, the first check to `user_input` is `if ( strlen(&user_input) > 0xB )`. So, take a note for that. Then, somehow it gets calculated `calc(v8, 4uLL, digest);`. What's this calc function does?

```c
void __fastcall calc_md5(const unsigned __int8 *initial_msg, size_t initial_len, unsigned __int8 *digest)
...
  qmemcpy(msg, v3, initial_len);
  msg[initial_len] = -128;
  while ( i > v6 )
    msg[v6++] = 0;
  v8 = 0x98BADCFE;
  v9 = 0xEFCDAB89;
  v10 = 0x67452301;
  to_bytes(8 * initial_len, &msg[i]);
  to_bytes(v13 >> 29, (v12 + v11 + 4));
  v15 = v14;
...
      else
      {
        v29 = v23 ^ v25 & (v23 ^ v24);
      }
      v31 = v26 + w[v28] + k[v27] + v29;
      v32 = r[v27++];
      v33 = __ROL4__(v31, v32);
      v26 = v23;
      v34 = v25 + v33;
      if ( v27 == 64 )
...
```

The calc function is huge, some byte magic happen in place, so I'm guessing this is a hash function. A __md5__ hash to be exact, because there are these constant `0x98BADCFE`, `0xEFCDAB89`, and `0x67452301`.

Back to `pill_choice` function again, so we know that our `user_input` got calculated with md5. Next check happen at this part,

```c
v5 = file_open("/proc/version");
...
v9 = const_data;
...
file_read(v5, (unsigned __int8 *)magic, 0x1F4u);
...
v10 = 0LL;
...
do
{
  v11 = magic[v10];
  v12 = digest[v10];
  v13 = 2 * v10++;
  sprintf((char *)&s2 + v13, "%02x", v11 ^ v12);
}
while ( v10 != 16 );
if ( memcmp(v9, &s2, 0x20uLL) )
  break;
v8 += 4;
v9 += 0x21;
...
```

Now, our __hashed__ `user_input` got _xor_-ed with bytes from `/proc/version`, then compare it with constant at `.data` section.

```
.data:0000000000000800 const_md5       db '40369e8c78b46122a4e813228ae8ee6e',0
.data:0000000000000821                 db 'e4a75afe114e4483a46aaa20fe4e6ead',0
.data:0000000000000842                 db '8c3749214f4a9131ebc67e6c7a86d162',0
```

Welp, thats all the checks. Lets sum it up

- `strlen(user_input) > 11`
- `md5(user_input[0:4]) ^ bytes(/proc/version) == '40369e8c78b46122a4e813228ae8ee6e'`
- `md5(user_input[4:8]) ^ bytes(/proc/version) == 'e4a75afe114e4483a46aaa20fe4e6ead'`
- `md5(user_input[8:12]) ^ bytes(/proc/version) == '8c3749214f4a9131ebc67e6c7a86d162'`

Oh, right, the content from `/proc/version` is `Linux version 4.17.0-rc4+ (likvidera@ubuntu) (gcc version 7.2.0 (Ubuntu 7.2.0-8ubuntu3.2)) #9 Sat May 12 12:57:01 PDT 2018`

---

Final solver script, this script just xor the constant from `.data` section with bytes from `/proc/version` which print the real md5 of our `user_input` then pass the real md5 to site like, hashkiller, etc.

```py
#!/usr/bin/env python
procver = 'Linux version 4.17.0-rc4+ (likvidera@ubuntu) (gcc version 7.2.0 (Ubuntu 7.2.0-8ubuntu3.2)) #9 Sat May 12 12:57:01 PDT 2018'

const = [
    '40369e8c78b46122a4e813228ae8ee6e',
    'e4a75afe114e4483a46aaa20fe4e6ead',
    '8c3749214f4a9131ebc67e6c7a86d162'
]

new_const = []
for c in const:
    new_const.append(map(lambda x: int(x, 16), [c[i:i+2] for i in range(0, len(c), 2)]))

for c in new_const:
    raw = ''
    i = 0
    for k in c:
        raw += hex(ord(procver[i]) ^ k)[2:].rjust(2, '0')
        i += 1
    print raw
```

```sh
$ python solve.py
0c5ff0f900941747d69b7a4de4c8da40
a8ce348b696e32e6d619c34f906e5a83
c05e2754376ae75499b5170314a6e54c
```

... From <https://hashkiller.co.uk>,
```
0c5ff0f900941747d69b7a4de4c8da40 MD5 : g1Mm
a8ce348b696e32e6d619c34f906e5a83 MD5 : 3Th3
c05e2754376ae75499b5170314a6e54c MD5 : r3D1
```

Final `user_input` string, `giMm3Th3r3D1`. Welp, too bad the service is down after CTF ends. But this is the answer tho, solved while CTF still running. Anyway, to get the flag, you just need to write the final `user_input` to `/proc/bluepill` for example,

```
echo -ne 'giMm3Th3r3D1' > /proc/bluepill
```

Then, you will get an escalated permission to read the flag file.
