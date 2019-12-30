---
title: INCTF 2017 - Secure Auth Writeup
categories:
  - rev
  - web
date: 2017-12-17 23:06:26
---

> Secure Auth (500 pts)
> ---------------------------
> 
> http://s3cur3auth.inctf.in/

Upon opening link, we're given a false alarm for site under maintenance. Lucky enough, after visiting /robots.txt we know that there's hidden folder in site.

User-agent: *
Disallow: /cgi-bin
Disallow: /zxcv

This /zxcv directory could be where the challange located,

![secure-auth-challange](https://a.safe.moe/gnBnR.png "login") yep, that's where the challange located.

After fiddling around a little bit, We know that the authentication is done within javascript, here's the source, (truncated)
```java
...
    var h = $(_0xf9c2('0x3'))[_0xf9c2('0x4')]();
    var n = h[_0xf9c2('0x5')](0x0, 0x4);
    n = n[_0xf9c2('0x6')]('')[_0xf9c2('0x7')]()['join']('');
    n = '0x' + n['split']('')[_0xf9c2('0x8')](_0x29995c => _0x29995c[_0xf9c2('0x9')](0x0)[_0xf9c2('0xa')](0x10))[_0xf9c2('0xb')]('');
    var m = h[_0xf9c2('0x5')](0x4, 0x8);
    m = m[_0xf9c2('0x6')]('')[_0xf9c2('0x7')]()[_0xf9c2('0xb')]('');
    m = '0x' + m[_0xf9c2('0x6')]('')[_0xf9c2('0x8')](_0x1c7b1c => _0x1c7b1c['charCodeAt'](0x0)[_0xf9c2('0xa')](0x10))[_0xf9c2('0xb')]('');
    var f = h[_0xf9c2('0x5')](0x8, 0xc);
    f = f[_0xf9c2('0x6')]('')[_0xf9c2('0x7')]()[_0xf9c2('0xb')]('');
    f = '0x' + f[_0xf9c2('0x6')]('')[_0xf9c2('0x8')](_0x41acdb => _0x41acdb[_0xf9c2('0x9')](0x0)['toString'](0x10))[_0xf9c2('0xb')]('');
    var j = h[_0xf9c2('0x5')](0xc, 0x10);
    j = j[_0xf9c2('0x6')]('')['reverse']()[_0xf9c2('0xb')]('');
    j = '0x' + j[_0xf9c2('0x6')]('')[_0xf9c2('0x8')](_0x4186f9 => _0x4186f9[_0xf9c2('0x9')](0x0)[_0xf9c2('0xa')](0x10))[_0xf9c2('0xb')]('');
    var g = h[_0xf9c2('0x5')](0x10, 0x13);
    g = g[_0xf9c2('0x6')]('')['reverse']()[_0xf9c2('0xb')]('');
    g = '0x' + g['split']('')[_0xf9c2('0x8')](_0x515f47 => _0x515f47[_0xf9c2('0x9')](0x0)['toString'](0x10))[_0xf9c2('0xb')]('');
    var c = $(_0xf9c2('0xc'))[_0xf9c2('0x4')]();
    var o = c[_0xf9c2('0x5')](0x0, 0x4);
    o = o['split']('')[_0xf9c2('0x7')]()['join']('');
    o = '0x' + o[_0xf9c2('0x6')]('')['map'](_0x12efcf => _0x12efcf['charCodeAt'](0x0)[_0xf9c2('0xa')](0x10))[_0xf9c2('0xb')]('');
    var i = c['slice'](0x4, 0x8);
    i = i['split']('')[_0xf9c2('0x7')]()[_0xf9c2('0xb')]('');
    i = '0x' + i['split']('')[_0xf9c2('0x8')](_0x3b0ae1 => _0x3b0ae1[_0xf9c2('0x9')](0x0)['toString'](0x10))[_0xf9c2('0xb')]('');
    var e = c[_0xf9c2('0x5')](0x8, 0xc);
    e = e[_0xf9c2('0x6')]('')[_0xf9c2('0x7')]()['join']('');
    e = '0x' + e['split']('')[_0xf9c2('0x8')](_0x40d2e3 => _0x40d2e3['charCodeAt'](0x0)['toString'](0x10))[_0xf9c2('0xb')]('');
    var k = c[_0xf9c2('0x5')](0xc, 0x10);
...
```

Uh oh.. succh obfuscate. Well, what i did was deobfuscate this by hand and here is the result,

```java
var _0x9c2f=['PROT_ALL','location','href','indexOf','/../','.html','Wrong\x20credentials,\x20sorry','#c_submit','click','preventDefault','#cuser','val','slice','split','reverse','map','charCodeAt','toString','join','#cpass','reg_write_i32','X86_REG_EAX','X86_REG_ECX','X86_REG_EDX','mem_map','emu_start','length','reg_read_i32','ARCH_X86','MODE_32','X86_REG_ESI','X86_REG_EBX','X86_REG_EBP'];
(function(a, c){
    var b = function(b) {
        while (--b) {
            a['push'](a['shift']());
        }
    };
    b(++c);
}(_0x9c2f, 0x193));
var _0xf9c2 = function(a, c) {
    a = a - 0x0;
    var b = _0x9c2f[a];
    return b;
};
$('#c_submit')['click'](function(r){
    r['preventDefault']();
    var h = $('#cuser')['val']();
    var n = h['slice'](0x0, 0x4);
    n = n['split']('')['reverse']()['join']('');
    n = '0x' + n['split']('')['map'](_0x29995c => _0x29995c['charCodeAt'](0x0)['toString'](0x10))['join']('');
    var m = h['slice'](0x4, 0x8);
    m = m['split']('')['reverse']()['join']('');
    m = '0x' + m['split']('')['map'](_0x1c7b1c => _0x1c7b1c['charCodeAt'](0x0)['toString'](0x10))['join']('');
    var f = h['slice'](0x8, 0xc);
    f = f['split']('')['reverse']()['join']('');
    f = '0x' + f['split']('')['map'](_0x41acdb => _0x41acdb['charCodeAt'](0x0)['toString'](0x10))['join']('');
    var j = h['slice'](0xc, 0x10);
    j = j['split']('')['reverse']()['join']('');
    j = '0x' + j['split']('')['map'](_0x4186f9 => _0x4186f9['charCodeAt'](0x0)['toString'](0x10))['join']('');
    var g = h['slice'](0x10, 0x13);
    g = g['split']('')['reverse']()['join']('');
    g = '0x' + g['split']('')['map'](_0x515f47 => _0x515f47['charCodeAt'](0x0)['toString'](0x10))['join']('');
    var c = $('#cpass')['val']();
    var o = c['slice'](0x0, 0x4);
    o = o['split']('')['reverse']()['join']('');
    o = '0x' + o['split']('')['map'](_0x12efcf => _0x12efcf['charCodeAt'](0x0)['toString'](0x10))['join']('');
    var i = c['slice'](0x4, 0x8);
    i = i['split']('')['reverse']()['join']('');
    i = '0x' + i['split']('')['map'](_0x3b0ae1 => _0x3b0ae1['charCodeAt'](0x0)['toString'](0x10))['join']('');
    var e = c['slice'](0x8, 0xc);
    e = e['split']('')['reverse']()['join']('');
    e = '0x' + e['split']('')['map'](_0x40d2e3 => _0x40d2e3['charCodeAt'](0x0)['toString'](0x10))['join']('');
    var k = c['slice'](0xc, 0x10);
    k = k['split']('')['reverse']()['join']('');
    k = '0x' + k['split']('')['map'](_0x71ef00 => _0x71ef00['charCodeAt'](0x0)['toString'](0x10))['join']('');
    var l = c['slice'](0x10, 0x13);
    l = l['split']('')['reverse']()['join']('');
    l = '0x' + l['split']('')['map'](_0x335224 => _0x335224['charCodeAt'](0x0)['toString'](0x10))['join']('');
    var a = new uc['Unicorn'](uc['ARCH_X86'], uc['MODE_32']);
    var b = 0x8048000;
    var d = [0xbf, 0x69, 0x61, 0x6d, 0x74, 0x39, 0xf8, 0x75, 0x2b, 0xbf, 0x68, 0x65, 0x61, 0x64, 0x39, 0xfb, 0x75, 0x22, 0xbf, 0x6d, 0x69, 0x6e, 0x69, 0x39, 0xf9, 0x75, 0x19, 0xbf, 0x73, 0x74, 0x72, 0x61, 0x39, 0xfa, 0x75, 0x10, 0xbf, 0x74, 0x6f, 0x72, 0x0, 0x39, 0xfe, 0x75, 0x7, 0xb8, 0x1, 0x0, 0x0, 0x0, 0xeb, 0x5, 0xb8, 0x0, 0x0, 0x0, 0x0];
    a['reg_write_i32'](uc['X86_REG_EAX'], n);
    a['reg_write_i32'](uc['X86_REG_EBX'], m);
    a['reg_write_i32'](uc['X86_REG_ECX'], f);
    a['reg_write_i32'](uc['X86_REG_EDX'], j);
    a['reg_write_i32'](uc['X86_REG_ESI'], g);
    a['mem_map'](b, 0x1000, uc['PROT_ALL']);
    a['mem_write'](b, d);
    a['emu_start'](b, b + d['PROT_ALL']);
    var p = a['reg_read_i32'](uc['X86_REG_EAX']);
    if (p) {
        var a = new uc['Unicorn'](uc['ARCH_X86'], uc['MODE_32']);
        var b = 0x8048000;
        var d = [0x81, 0xc6, 0x69, 0x61, 0x6d, 0x74, 0x81, 0xc6, 0x7, 0x6, 0x5, 0x4, 0x81, 0xfe, 0xd3, 0xd6, 0xe0, 0xdf, 0x75, 0x55, 0x40, 0x81, 0xc3, 0x68, 0x65, 0x61, 0x64, 0x81, 0xc3, 0x3, 0x2, 0x1, 0x0, 0x81, 0xfb, 0xdd, 0xdb, 0xdc, 0x98, 0x75, 0x40, 0x40, 0x81, 0xc1, 0x6d, 0x69, 0x6e, 0x69, 0x81, 0xc1, 0xf, 0xe, 0xd, 0xc, 0x81, 0xf9, 0xf0, 0xdf, 0xe0, 0xe5, 0x75, 0x2b, 0x40, 0x81, 0xc2, 0x73, 0x74, 0x72, 0x61, 0x81, 0xc2, 0xb, 0xa, 0x9, 0x8, 0x81, 0xfa, 0xdf, 0xf1, 0x9f, 0xe0, 0x75, 0x16, 0x40, 0x81, 0xc5, 0x74, 0x6f, 0x72, 0x0, 0x81, 0xc5, 0x17, 0x16, 0x15, 0x0, 0x81, 0xfd, 0xbb, 0xf7, 0xcb, 0x0, 0x75, 0x1, 0x40];
        a['reg_write_i32'](uc['X86_REG_ESI'], o);
        a['reg_write_i32'](uc['X86_REG_EBX'], i);
        a['reg_write_i32'](uc['X86_REG_ECX'], e);
        a['reg_write_i32'](uc['X86_REG_EDX'], k);
        a['reg_write_i32'](uc['X86_REG_EBP'], l);
        a['mem_map'](b, 0x1000, uc['PROT_ALL']);
        a['mem_write'](b, d);
        a['emu_start'](b, b + d['length']);
        var q = a['reg_read_i32'](uc['X86_REG_EAX']);
        if (q == 0x5) {
            if (document['location']['href']['indexOf']('?p=') == -0x1) {
                document['location'] = document['location'] + '/../' + c + '.html';
            }
        } else {
            alert('Wrong credentials, sorry');
        }
    } else {
        alert('Wrong credentials, sorry');
    }
});
```
The next stage, analysis part. (1st) There are 2 input, username in #cuser and password in #cpass. The input is 0x13 bytes long sliced into 5 part and 3-4 bytes each in little endian.

![](/img/table_1.png)

The authentication uses Unicorn to emulate shellcode in browser.
```
var a = new uc['Unicorn'](uc['ARCH_X86'], uc['MODE_32']);
    var b = 0x8048000;
    var d = [0xbf, 0x69, 0x61, 0x6d, 0x74, 0x39, 0xf8, 0x75, 0x2b, 0xbf, 0x68, 0x65, 0x61, 0x64, 0x39, 0xfb, 0x75, 0x22, 0xbf, 0x6d, 0x69, 0x6e, 0x69, 0x39, 0xf9, 0x75, 0x19, 0xbf, 0x73, 0x74, 0x72, 0x61, 0x39, 0xfa, 0x75, 0x10, 0xbf, 0x74, 0x6f, 0x72, 0x0, 0x39, 0xfe, 0x75, 0x7, 0xb8, 0x1, 0x0, 0x0, 0x0, 0xeb, 0x5, 0xb8, 0x0, 0x0, 0x0, 0x0];
    a['reg_write_i32'](uc['X86_REG_EAX'], n);
    a['reg_write_i32'](uc['X86_REG_EBX'], m);
    a['reg_write_i32'](uc['X86_REG_ECX'], f);
    a['reg_write_i32'](uc['X86_REG_EDX'], j);
    a['reg_write_i32'](uc['X86_REG_ESI'], g);
    a['mem_map'](b, 0x1000, uc['PROT_ALL']);
    a['mem_write'](b, d);
    a['emu_start'](b, b + d['PROT_ALL']);
    var p = a['reg_read_i32'](uc['X86_REG_EAX']);
```

(2nd) This is the first part of auth checker to check username input. `n, m, f, j, g` are values from sliced #cuser input. From that we know,

```
n = > EAX
m => EBX
f => ECX
j => EDX
g => ESI
```

The shellcode part,
```
   0:   bf 69 61 6d 74          mov    edi,0x746d6169
   5:   39 f8                   cmp    eax,edi
   7:   75 2b                   jne    0x34
   9:   bf 68 65 61 64          mov    edi,0x64616568
   e:   39 fb                   cmp    ebx,edi
  10:   75 22                   jne    0x34
  12:   bf 6d 69 6e 69          mov    edi,0x696e696d
  17:   39 f9                   cmp    ecx,edi
  19:   75 19                   jne    0x34
  1b:   bf 73 74 72 61          mov    edi,0x61727473
  20:   39 fa                   cmp    edx,edi
  22:   75 10                   jne    0x34
  24:   bf 74 6f 72 00          mov    edi,0x726f74
  29:   39 fe                   cmp    esi,edi
  2b:   75 07                   jne    0x34
  2d:   b8 01 00 00 00          mov    eax,0x1
  32:   eb 05                   jmp    0x39
  34:   b8 00 00 00 00          mov    eax,0x0
```

```
0x746d6169 == EAX
0x64616568 == EBX
0x696e696d == ECX
0x61727473 == EDX
0x726f74 == ESI
```

Thats clear enough, the values `n, m, f, j, g` should be `"iamt", "head", "mini", "stra", "tor"`. **#cuser == iamtheadministrator**. (3rd) Next one, the checker for #cpass.

```java
        var a = new uc['Unicorn'](uc['ARCH_X86'], uc['MODE_32']);
        var b = 0x8048000;
        var d = [0x81, 0xc6, 0x69, 0x61, 0x6d, 0x74, 0x81, 0xc6, 0x7, 0x6, 0x5, 0x4, 0x81, 0xfe, 0xd3, 0xd6, 0xe0, 0xdf, 0x75, 0x55, 0x40, 0x81, 0xc3, 0x68, 0x65, 0x61, 0x64, 0x81, 0xc3, 0x3, 0x2, 0x1, 0x0, 0x81, 0xfb, 0xdd, 0xdb, 0xdc, 0x98, 0x75, 0x40, 0x40, 0x81, 0xc1, 0x6d, 0x69, 0x6e, 0x69, 0x81, 0xc1, 0xf, 0xe, 0xd, 0xc, 0x81, 0xf9, 0xf0, 0xdf, 0xe0, 0xe5, 0x75, 0x2b, 0x40, 0x81, 0xc2, 0x73, 0x74, 0x72, 0x61, 0x81, 0xc2, 0xb, 0xa, 0x9, 0x8, 0x81, 0xfa, 0xdf, 0xf1, 0x9f, 0xe0, 0x75, 0x16, 0x40, 0x81, 0xc5, 0x74, 0x6f, 0x72, 0x0, 0x81, 0xc5, 0x17, 0x16, 0x15, 0x0, 0x81, 0xfd, 0xbb, 0xf7, 0xcb, 0x0, 0x75, 0x1, 0x40];
        a['reg_write_i32'](uc['X86_REG_ESI'], o);
        a['reg_write_i32'](uc['X86_REG_EBX'], i);
        a['reg_write_i32'](uc['X86_REG_ECX'], e);
        a['reg_write_i32'](uc['X86_REG_EDX'], k);
        a['reg_write_i32'](uc['X86_REG_EBP'], l);
        a['mem_map'](b, 0x1000, uc['PROT_ALL']);
        a['mem_write'](b, d);
        a['emu_start'](b, b + d['length']);
        var q = a['reg_read_i32'](uc['X86_REG_EAX']);
```

`o, i, e, k, l` are values from sliced #cpass input. From that we know,

```
o => ESI
i => EBX
e => ECX
k => EDX
l => EBP
```

The shellcode part,

```
   0:   81 c6 69 61 6d 74       add    esi,0x746d6169
   6:   81 c6 07 06 05 04       add    esi,0x4050607
   c:   81 fe d3 d6 e0 df       cmp    esi,0xdfe0d6d3
  12:   75 55                   jne    0x69
  14:   40                      inc    eax
  15:   81 c3 68 65 61 64       add    ebx,0x64616568
  1b:   81 c3 03 02 01 00       add    ebx,0x10203
  21:   81 fb dd db dc 98       cmp    ebx,0x98dcdbdd
  27:   75 40                   jne    0x69
  29:   40                      inc    eax
  2a:   81 c1 6d 69 6e 69       add    ecx,0x696e696d
  30:   81 c1 0f 0e 0d 0c       add    ecx,0xc0d0e0f
  36:   81 f9 f0 df e0 e5       cmp    ecx,0xe5e0dff0
  3c:   75 2b                   jne    0x69
  3e:   40                      inc    eax
  3f:   81 c2 73 74 72 61       add    edx,0x61727473
  45:   81 c2 0b 0a 09 08       add    edx,0x8090a0b
  4b:   81 fa df f1 9f e0       cmp    edx,0xe09ff1df
  51:   75 16                   jne    0x69
  53:   40                      inc    eax
  54:   81 c5 74 6f 72 00       add    ebp,0x726f74
  5a:   81 c5 17 16 15 00       add    ebp,0x151617
  60:   81 fd bb f7 cb 00       cmp    ebp,0xcbf7bb
  66:   75 01                   jne    0x69
  68:   40                      inc    eax
```

```
0xdfe0d6d3 == ESI + 0x746d6169 + 0x4050607
0x98dcdbdd == EBX + 0x64616568 + 0x10203
0xe5e0dff0 == ECX + 0x696e696d + 0xc0d0e0f
0xe09ff1df == EDX + 0x61727473 + 0x8090a0b
0xcbf7bb   == ESI + 0x726f74 + 0x151617
```

Reversing the values by subtracting, we have the values what we wanted. `o, i, e, k, l` should be `"cong", "rtz4", "thep", "as$w", "0rD"`. `#cpass == congrtz4thepas$w0rD` To sum it up, we have the value for `#cuser == 'iamtheadministrator'` and `#cpass == 'congrtz4thepas$w0rD'`. After submit that values, it'll be redirected to flag page, and we got the flag.

FLAG : `inctf{l1ck_l1ck_l1ck_my_j5}`

* * *

Side note, This event has many cool challanges. I liked this one actually, since this is a mix for web and reversing challange (read: I get the firstblood for this challange :p). I couldn't get any flag for advanced binary challange tho. The mobile challange looks like have many flaw and unintended ways of for solving. I'm expecting it to have some anti-tamper but just by small patching anyone could get the flag.