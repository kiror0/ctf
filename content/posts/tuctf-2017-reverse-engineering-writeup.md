+++
title = "TUCTF 2017 - Reverse Engineering Writeup"
date = "2017-11-27 18:01:11"
categories = ["rev", "writeup"]
+++

# Funmail

> One of our employees has locked himself out of his account. can you help 'john galt' recover his password? And no snooping around his emails you hear.

Upon  running the binary given, user will be prompted to input username and password. The hints basically tells you everything. Use `john galt` as Username, then for password, use `ltrace ./funmail` to trace strcmp.

```
strcmp("idontknow", "this-password-is-a-secret-to-eve"...)       = -1
```

ugh. Only small chunk of string is printed. To solve this use strings and grep for the password.

```
$ strings ./funmail|grep password
*Incorrect password
this-password-is-a-secret-to-everyone!
password
```

So, `this-password-is-a-secret-to-everyone!` is the password. Now, run binary again.
```
--Please login--
Username: john glat
*We have no users with the username: 'john glat'
--Please login--
Username: john galt
Password: this-password-is-a-secret-to-everyone!
Welcome john galt!
You have 1 unread email.
1) Read Email
2) Quit
>\> 1
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-
From:   Leeroy Jenkins
To:     whoisjohngalt
Subject: RE: I need a flag

Hey John it's Leeroy.
You were asking about a fun flag to use in your next challenge
and I think I got one. Tell me what you think of:
TUCTF{d0n7\_h4rdc0d3\_p455w0rd5}
Get back to me as soon as you can. Thanks!
\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-

Flag : `TUCTF{d0n7_h4rdc0d3_p455w0rd5}`
```

# Funmail2.0

> john galt is having some problems with his email again. But this time it's not his fault. Can you help him?

This challange is quite same with the first challange, except its tricky because even after input the right username and password, program will force exit. After sometime, I just realized that the sym.printFlag function is still there in the binary, but didnt get invoked. Solution, put break at the start then set rip (eip) to sym.printF;ag then continue. In radare2,

```
[0xf7739030]> db sym.main
[0xf775ab24]> is ~Flag
vaddr=0xf775a785 paddr=0x00000785 ord=053 fwd=NONE sz=302 bind=GLOBAL type=FUNC name=printFlag
[0xf775ab24]> dr eip=0xf775a785
0xf775ab24 ->0xf775a785
[0xf775ab24]> dc
TUCTF{l0c4l_<\_r3m073\_3x3cu710n}
```

Flag : `TUCTF{l0c4l_<_r3m073_3x3cu710n}`

# Unknown

> Diggin through some old files we discovered this binary. Although despite our inspection we can't figure out what it does. Or what it wants...

Input hashed per character and check if character hash same with some constant. Solution, drop the character hash when its being compared. Recover the flag from constant and known hash from dropped hash.
```python
import sys

# defacto lib
try:
    import r2pipe
except ImportError as err:
    print("Error while importing module r2pipe: %s" % str(err))
    sys.exit(1)

unk_401DAC = [
    0xFDFAB57A,0x032449A7,0x5F383821,0xFDFAB57A,
    0x25435E02,0x59E2EB0D,0x5ED756D7,0x5CFFF023,
    0x9239BDF3,0xF62C7F9B,0x63E13F5F,0xD6338E84,
    0x5CFFF023,0xFF20BDEF,0xC51F928E,0x63E13F5F,
    0xFF20BDEF,0xC51F928E,0xB59D1071,0xF62C7F9B,
    0xC51F928E,0x388D9870,0xFF20BDEF,0xCEECC5BA,
    0xA952136B,0x96710841,0xFF20BDEF,0xC51F928E,
    0xF536DFFD,0xCEECC5BA,0xA952136B,0xC5D7DAC4,
    0xFF20BDEF,0x12A92A61,0x63E13F5F,0xB59D1071,
    0xFF20BDEF,0x388D9870,0x63E13F5F,0xCD78354E,
    0xFF20BDEF,0xF2184419,0xCEECC5BA,0xCD78354E,
    0xC51F928E,0x3CA8BFDC,0xF62C7F9B,0x3CA8BFDC,
    0xF2184419,0xCEECC5BA,0xC51F928E,0x3CA8BFDC,
    0xA952136B,0x2FF35144,0xBA165EA7,0xEF1B84CD
]

'''
# Stage 1 -- Recover the hashes --
alpha = [ 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123', '456789!()[]_-,.PADPADPADPADPADPADPADPADPADPADPADPADPADPA' ]

for key in alpha:
    r2 = r2pipe.open('./unknown')
    r2.cmd('ood ' + key)
    r2.cmd('db 0x401f20') # break on \`cmp eax, ecx\`
    for i in key:
        r2.cmd('dc')
        regs = r2.cmdj('drj')
        # dump the hash into table
        print '[\\'' + i + '\\' ,' + hex(regs['rax']) + ']'
    r2.quit()

'''

# Stage 2 -- Recover the flag using known character hashes table --
hashes = [ ['0' ,0x63e13f5f],
['1' ,0x3ca8bfdc],
['2' ,0xdd0e6ec0],
['3' ,0x5cfff023],
['4' ,0xceecc5ba],
['5' ,0xcc1be317],
['6' ,0x2ff35144],
['7' ,0xc51f928e],
['8' ,0xb6705910],
['9' ,0x26552da4],
['A' ,0x65d4bb53],
['B' ,0x62fe8700],
['C' ,0x5f383821],
['D' ,0x70e9ce39],
['E' ,0x5f9b4d91],
['F' ,0x25435e02],
['G' ,0x51beb40a],
['H' ,0x82d03951],
['I' ,0x1bd78865],
['J' ,0x81d23ebf],
['K' ,0xb8aa7c13],
['L' ,0x8e29337c],
['M' ,0x960c851a],
['N' ,0x9aecf4a0],
['O' ,0x3d5214b8],
['P' ,0xcab235fd],
['Q' ,0x9c417714],
['R' ,0x010ef83b],
['S' ,0x87befa83],
['T' ,0xfdfab57a],
['U' ,0x032449a7],
['V' ,0xe67efe4f],
['W' ,0x3b957ccc],
['X' ,0xce39daba],
['Y' ,0x69844214],
['Z' ,0xcece4054],
['a' ,0x3893db85],
['b' ,0x0faf7ec1],
['c' ,0xf62c7f9b],
['d' ,0x96710841],
['e' ,0xb623c6c1],
['f' ,0x388d9870],
['g' ,0x382136b4],
['h' ,0xf536dffd],
['i' ,0x67258d77],
['j' ,0x5019d530],
['k' ,0xc5d7dac4],
['l' ,0x9239bdf3],
['m' ,0xd6338e84],
['n' ,0xa952136b],
['o' ,0x408a2c4b],
['p' ,0xf2184419],
['q' ,0x2c6485d5],
['r' ,0xcd78354e],
['s' ,0x98605ae6],
['t' ,0xc863df45],
['u' ,0xb59d1071],
['v' ,0xa4f459d3],
['w' ,0x5ed756d7],
['x' ,0x965ae173],
['y' ,0x12a92a61],
['z' ,0xe630810a],
['_' ,0xff20bdef],
['{' ,0x59e2eb0d],
['}' ,0xef1b84cd],
['!' ,0xba165ea7] ]

flag = ""

for u in unk_401DAC:
    for k in hashes:
        if k[1] == u:
            flag += k[0]
            break

print flag

```

Flag : `TUCTF{w3lc0m3_70_7uc7f_4nd_7h4nk_y0u_f0r_p4r71c1p471n6!}`

# Future

> Future me gave me this and told me to add it to TUCTF. I dunno, he sounded crazy. Anyway, Let's see what's so special about it.

```C
#include 
#include 
#include 

void genMatrix(char mat[5][5], char str[]) {
    for (int i = 0; i < 25; i++) {
        int m = (i * 2) % 25;
        int f = (i * 7) % 25;
        mat[m/5][m%5] = str[f];
    }
}

void genAuthString(char mat[5][5], char auth[]) {
    auth[0] = mat[0][0] + mat[4][4];
    auth[1] = mat[2][1] + mat[0][2];
    auth[2] = mat[4][2] + mat[4][1];
    auth[3] = mat[1][3] + mat[3][1];
    auth[4] = mat[3][4] + mat[1][2];
    auth[5] = mat[1][0] + mat[2][3];
    auth[6] = mat[2][4] + mat[2][0];
    auth[7] = mat[3][3] + mat[3][2] + mat[0][3];
    auth[8] = mat[0][4] + mat[4][0] + mat[0][1];
    auth[9] = mat[3][3] + mat[2][0];
    auth[10] = mat[4][0] + mat[1][2];
    auth[11] = mat[0][4] + mat[4][1];
    auth[12] = mat[0][3] + mat[0][2];
    auth[13] = mat[3][0] + mat[2][0];
    auth[14] = mat[1][4] + mat[1][2];
    auth[15] = mat[4][3] + mat[2][3];
    auth[16] = mat[2][2] + mat[0][2];
    auth[17] = mat[1][1] + mat[4][1];
}

int main() {
    char flag[26];
    printf("What's the flag: ");
    scanf("%25s", flag);
    flag[25] = 0;

    if (strlen(flag) != 25) {
        puts("Try harder.");
        return 0;
    }

    // Setup matrix
    char mat[5][5];// Matrix for a jumbled string
    genMatrix(mat, flag);
    // Generate auth string
    char auth[19]; // The auth string they generate
    auth[18] = 0; // null byte
    genAuthString(mat, auth);
    char pass[19] = "\\x8b\\xce\\xb0\\x89\\x7b\\xb0\\xb0\\xee\\xbf\\x92\\x65\\x9d\\x9a\\x99\\x99\\x94\\xad\\xe4\\x00";

    // Check the input
    if (!strcmp(pass, auth)) {
        puts("Yup thats the flag!");
    } else {
        puts("Nope. Try again.");
    }

    return 0;
}
```

In this challange, program will calculate our input and check if its same with `pass` constant. I'm using Z3 smt solver to solve this and add TUCTF flag format as a constraint, because if it isn't Z3 will give another uintended solution.

```python
#!/usr/bin/env python
from z3 import *
import string

s = Solver()

const = [0x8b, 0xce, 0xb0, 0x89, 0x7b, 0xb0, 0xb0, 0xee, 0xbf, 0x92, 0x65, 0x9d, 0x9a, 0x99, 0x99, 0x94, 0xad, 0xe4]

str = [BitVec(i, 8) for i in xrange(25)]

alpha = string.letters + string.digits + string.punctuation

for i in xrange(25):
    for x in xrange(0xFF):
        if chr(x) not in alpha:
            s.add(str[i] != x)

s.add(str[0] == ord('T'))
s.add(str[1] == ord('U'))
s.add(str[2] == ord('C'))
s.add(str[3] == ord('T'))
s.add(str[4] == ord('F'))
s.add(str[5] == ord('{'))
s.add(str[24] == ord('}'))

s.add(str[0] + str[9] == const[0])
s.add(str[1] + str[7] == const[1])
s.add(str[2] + str[11] == const[2])
s.add(str[3] + str[6] == const[3])
s.add(str[4] + str[12] == const[4])
s.add(str[5] + str[8] == const[5])
s.add(str[24] + str[10] == const[6])
s.add(str[13] + str[22] + str[23] == const[7])
s.add(str[14] + str[20] + str[16] == const[8])
s.add(str[13] + str[10] == const[9])
s.add(str[20] + str[12] == const[10])
s.add(str[14] + str[11] == const[11])
s.add(str[23] + str[7] == const[12])
s.add(str[15] + str[10] == const[13])
s.add(str[19] + str[12] == const[14])
s.add(str[18] + str[8] == const[15])
s.add(str[17] + str[7] == const[16])
s.add(str[21] + str[11] == const[17])

if s.check() == sat:
    model = s.model()
    flag = [chr(model[x].as_long()) for x in str]
    print ''.join(flag)
else:
    print 'Nope :('

'''
mat[0][0] = str[0]
mat[2][1] = str[1]
mat[4][2] = str[2]
mat[1][3] = str[3]
mat[3][4] = str[4]
mat[1][0] = str[5]
mat[3][1] = str[6]
mat[0][2] = str[7]
mat[2][3] = str[8]
mat[4][4] = str[9]
mat[2][0] = str[10]
mat[4][1] = str[11]
mat[1][2] = str[12]
mat[3][3] = str[13]
mat[0][4] = str[14]
mat[3][0] = str[15]
mat[0][1] = str[16]
mat[2][2] = str[17]
mat[4][3] = str[18]
mat[1][4] = str[19]
mat[4][0] = str[20]
mat[1][1] = str[21]
mat[3][2] = str[22]
mat[0][3] = str[23]
mat[2][4] = str[24]
'''
```

Flag : `TUCTF{5y573m5_0f_4_d0wn!}`