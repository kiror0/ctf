---
title: SharifCTF 2018 - fHash Writeup
categories:
- crypto
- writeup
date: 2018-02-04 16:16:15
---

> fHash.py (https://pastebin.com/tEw7BPtX)

![](https://a.safe.moe/MceKg) Given a custom hash, the task is to create some kind of collision in order to get the flag. At this moment, I don't know what's this second-preimage thing, but the task is clear enough somehow we should get the collision with restriction `hl1 != hl2` and `hr1 != hr2` and `M1 != M2`. `hl` and `hr` **must** be 2 bytes and `M` **must** be 4 bytes. First, analyze the algorithm used.

```python
from hashlib import md5

def foo(h, m):
    return md5(h.encode('utf-8') + m.encode('utf-8')).hexdigest()[:4]

def round(hl, m, hr):
    return foo(hl, m), foo(hr, m)

def fHash(hl, hr, M):
    message = list(map(''.join, zip(*[iter(M)] * 4)))
    for m in message:
        hl, hr = round(hl, m, hr)
    return (hl, hr)

if __name__ == '__main__':
    print(fHash('7575', 'A8A8', '7368617269666374'))
```

`M` length must be the power of 4 so that it can be sliced into parts by 2 bytes. As for example `7368617269666374` => `7368`,`6172`,`6966`, and `6374`. After that, sliced `M` get to concatenated with `hl` or `hr` then the first 2 bytes of md5sum from the concatenated string will be used for next round `hl` or `hr`, repeated until last sliced part of `M`. For example, `7575` and `7368` => `md5sum(75757368)[:4]` => `dcd0` => `dcd0` and `6172` => `md5sum(dcd06172)[:4]` => and so on.. In diagram ![](https://a.safe.moe/gVUMe.png) Attack. Yes, Attacc boi. The flaw is in `foo(h, m)` where the return only the first 2 bytes of `md5sum(h + m)`. At first, my approach was to get all the bytes from `hl`, `hr`, and `M` to be different. That's where the exhausting part, until I just realized, __all of the bytes doesn't needs to be different__ :|. Side story aside, the idea for this is to change the bytes used first round and the return for foo must be same as use in `hl1`, `hr1`, and `M1`. I did this with a crude bruteforce way,

```python
#!/usr/bin/env python
from hashlib import md5
import sys

def foo(h, m):
    return md5(h.encode('utf-8') + m.encode('utf-8')).hexdigest()[:4]

alpha = '0123456789ABCDEF'
# alpha = '0123456789abcdef'

for hex1 in alpha:
    for hex2 in alpha:
        for hex3 in alpha:
            for hex4 in alpha:
                for hex5 in alpha:
                    for hex6 in alpha:
                        for hex7 in alpha:
                            for hex8 in alpha:
                                m =  hex1 + hex2 + hex3 + hex4
                                hl = hex5 + hex6 + hex7 + hex8
                                if foo(hl, m) == 'dcd0':
                                    for hex9 in alpha:
                                        for hex10 in alpha:
                                            for hex11 in alpha:
                                                for hex12 in alpha:
                                                    hr = hex9 + hex10 + hex11 + hex12
                                                    if foo(hr, m) == 'a6ea':
                                                        print hl, m, hr
                                                        sys.exit(0)
```

I put break at the end just to output one result, in fact there are dozens of result if this didn't stopped. It doesn't need to take long to run this bruteforce script, the output,

```
45ED 0007 E19F
```

In diagram, ![](https://a.safe.moe/N08T6.png)
The final answer, `hl2 = 45ED`, `hr2 = E19F`, `M2 = 0007617269666374`.
![](https://a.safe.moe/qBlm0.png)