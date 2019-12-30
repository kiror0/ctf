---
title: JOINTS 2018 - Simple VM WriteUp
categories:
- rev
- writeup
date: 2018-05-07 18:14:01
---

_psst: Post ini akan banyak sisipan rant dan commentary saat sesi Final JOINTS 2018._ Hasil decompile binary ELF di IDA pro agak cukup berantakan, Jadi, saya buka di graph view untuk analisa opcode. Hasilnya, agak terhambat di bagian byte 0xD1 - 0xD5. Tapi, akhirnya source code soal dibagikan saat menjelang akhir lomba. btw, kalau bisa ada hint yang di keluarkan tolong diumumkan langusng, ehe. cc: panitia Source code soal _redacted_,
```C
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

char *reg;
char data[60];
char *ins = "\
\xc3\x01\x00\x64\
\xc3\x01\x01\x5b\
\xc3\x01\x02\x1b\
\xc3\x01\x03\x5a\
\xc3\x01\x04\x71\
\xc3\x01\x05\x6f\
\xc3\x01\x06\x71\
\xc3\x01\x07\x7d\
\xc3\x01\x08\x47\
\xc3\x01\x09\x43\
\xc3\x01\x0a\x5e\
\xc3\x01\x0b\x42\
\xc3\x01\x0c\x4b\
\xc3\x01\x0d\x71\
\xc3\x01\x0e\x61\
\xc3\x01\x0f\x5e\
\xc3\x01\x10\x4d\
\xc3\x01\x11\x1e\
\xc3\x01\x12\x4a\
\xc3\x01\x13\x1d\
\xc3\x01\x14\x24\
\xc3\x01\x15\x2e\
\
\xc3\x00\x05\x01\
\xc3\x00\x00\x14\
\xc3\x00\x01\x2a\
\
\xc3\x02\x03\x01\
\
\x70\x01\x03\x2e\
\
\xc3\x02\x04\x00\
\
\xcf\x00\x03\x04\
\
\xd1\x0e\
\xac\x00\x01\
\xac\x00\x00\
\xd5\xe8\
\xc3\x00\x05\x00\
\xff";

int vm(){
    int i = 0;
    int temp;
    char flag;
    reg = malloc(5);
    while(1){
        if( ins[i] == (char)0xc3 ){ // mov
            if( ins[i+1] == '\x01' ){
                data[ (int)ins[i+2] ] = ins[i+3];
            }
            else if(ins[i+1] == '\x00' ){
                reg[ (int)ins[i+2] ] = ins[i+3];

            }
            else if(ins[i+1] == '\x03'){
                temp = (int)reg[ (int)ins[i+2] ];
                data[temp] = ins[i+3];
            }
            else if(ins[i+1] == '\x04'){
                data[ (int)ins[i+2] ] = reg[ (int)ins[i+3] ];
            }
            else if(ins[i+1] == '\x02'){
                temp = reg[ (int)ins[i+3] ];
                reg[ (int)ins[i+2] ] = data[ temp ];
            }
            else if(ins[i+1] == '\x06'){
                reg[ (int)ins[i+2] ] = data[ (int)ins[i+3] ];
            }
            i += 4;
            continue;
        }
        if( ins[i] == (char)0xab){
            if( ins[i+1] == (char)0x01)
                flag = (data[ (int)ins[i+2] ] += (char) 1);
            else if( ins[i+1] == (char)0x00)
                flag = (reg[ (int)ins[i+2] ] += (char) 1);
            else if( ins[i+1] == '\x03' ){
                temp = (int)reg[ (int)ins[i+2] ];
                data[temp] += (char) 1;
                flag = data[temp];
            }
            i += 3;
            continue;
        }
        if( ins[i] == (char)0xac){
            if( ins[i+1] == (char)0x01)
                flag = (data[ (int)ins[i+2] ] -= (char) 1);
            else if( ins[i+1] == (char)0x00)
                flag = (reg[ (int)ins[i+2] ] -= (char) 1);
            else if( ins[i+1] == '\x03' ){
                temp = (int)reg[ (int)ins[i+2] ];
                data[temp] -= (char) 1;
                flag = data[temp];
            }
            i += 3;
            continue;
        }
        if( ins[i] == (char)0xcf){ // cmp
            if( ins[i+1] == (char)0x00){
                flag = (char)(reg[ (int)ins[i+2] ] - reg[ (int)ins[i+3] ]);
            }
            else if( ins[i+1] == '\x01'){
                flag = (char)(reg[ (int)ins[i+2] ] - ins[i+3] );
            }
            else if( ins[i+1] == '\x02'){
                flag = (char)(data[ (int)ins[i+2] ] - ins[i+3] );
            }
            else if( ins[i+1] == '\x03'){
                flag = (char)(data[ (int)ins[i+2] ] - reg[(int)ins[i+3]]);
            }
            else if( ins[i+1] == '\x04'){
                flag = (char)(reg[ (int)ins[i+2] ] - data[(int)ins[i+3]]);
            }
            else if( ins[i+1] == '\x05'){
                temp = (int)reg[ (int)ins[i+2] ];
                flag = (char)( data[temp] - reg[ (int)ins[i+3]]);
            }
            i += 4;
            continue;
        }
        if((ins[i] == (char)0xd0 && flag == 0) ||
           (ins[i] == (char)0xd1 && flag != 0) ||
           (ins[i] == (char)0xd2 && flag < 0 ) ||
           (ins[i] == (char)0xd3 && flag <= 0) ||
           (ins[i] == (char)0xd4 && flag > 0 ) ||
           (ins[i] == (char)0xd5 && flag >= 0) ||
           (ins[i] == (char)0xd6)){
            i = (char)i + ins[i+1];
            continue;
        }else{
            if((uint8_t)ins[i] >= 0xd0 && (uint8_t)ins[i] <= 0xd5){
                i += 2;
                continue;
            }
        }
        if( ins[i] == 0x70 ){
            if( ins[i+1] == '\x00' ){
                flag = (reg[ (int)ins[i+2] ] ^= (char) reg[ (int)ins[i+3] ]);
            }
            else if( ins[i+1] == '\x01'){
                flag = (reg[ (int)ins[i+2] ] ^= (char) ins[i+3]);
            }
            else if( ins[i+1] == '\x02'){
                flag = (reg[ (int)ins[i+2] ] ^= data[ (int)ins[i+3] ]);
            }
            else if( ins[i+1] == '\x03'){
                flag = (data[ (int)ins[i+2] ] ^= (char) ins[i+3]);
            }
            else if( ins[i+1] == '\x04'){
                temp = (int) reg[ (int)ins[i+2] ];
                flag = (data[temp] ^= (char) ins[i+3] );
            }
            else if( ins[i+1] == '\x05'){
                temp = (int) reg[ (int)ins[i+2] ];
                flag = (data[temp] ^= (char) reg[ (int)ins[i+3]] );
            }
            i += 4;
            continue;
        }
        if( ins[i] == (char)0xff ) break;
    }

    return (int)reg[5];
}

int main(void){
    printf("Simple VM\n");
    printf("Masukkan password : ");
    fgets((char*)data+22,23,stdin);
    if( vm() != 0){
        printf("Password Salah\n");
        return -1;
    }
    printf("Password Benar\n");
}
```
Pada awal fungsi vm(), ada pemanggilan malloc() untuk alokasi reg[]. Dari ini, bisa dipastikan ada 5 local register dengan Instruction Pointer pada [rbp - 4], instruksi/opcode-nya sendiri ada pada ins[] di data section, memang, sudah dijelaksan, pada judul soalnya, tidak muluk-muluk, benar-benar _simpel_. Untuk analisa opcode, saya buat parser seadanya dengan python. Berikut scriptnya,

```python
from struct import unpack

opcode = "\
\xc3\x01\x00\x64\
\xc3\x01\x01\x5b\
\xc3\x01\x02\x1b\
\xc3\x01\x03\x5a\
\xc3\x01\x04\x71\
\xc3\x01\x05\x6f\
\xc3\x01\x06\x71\
\xc3\x01\x07\x7d\
\xc3\x01\x08\x47\
\xc3\x01\x09\x43\
\xc3\x01\x0a\x5e\
\xc3\x01\x0b\x42\
\xc3\x01\x0c\x4b\
\xc3\x01\x0d\x71\
\xc3\x01\x0e\x61\
\xc3\x01\x0f\x5e\
\xc3\x01\x10\x4d\
\xc3\x01\x11\x1e\
\xc3\x01\x12\x4a\
\xc3\x01\x13\x1d\
\xc3\x01\x14\x24\
\xc3\x01\x15\x2e\
\xc3\x00\x05\x01\
\xc3\x00\x00\x14\
\xc3\x00\x01\x2a\
\xc3\x02\x03\x01\
\x70\x01\x03\x2e\
\xc3\x02\x04\x00\
\xcf\x00\x03\x04\
\xd1\x0e\
\xac\x00\x01\
\xac\x00\x00\
\xd5\xe8\
\xc3\x00\x05\x00\
\xff"

i = 0
cnt = 0

u1 = lambda x: unpack('b', x)[0]

while i < len(opcode):
    if opcode[i] == '\xc3':
        mode = opcode[i + 1]
        if mode == '\x00':
            print str(i).zfill(3), "reg[{}] = {}".format(u1(opcode[i + 2]), u1(opcode[i + 3]))
        elif mode == '\x01':
            print str(i).zfill(3), "data[{}] = {}".format(u1(opcode[i + 2]), u1(opcode[i + 3]))
        elif mode == '\x02':
            print str(i).zfill(3), "reg[{}] = data[reg[{}]]".format(u1(opcode[i + 2]), u1(opcode[i + 3]))
        i += 4
        cnt += 1
    elif opcode[i] == '\x70':
        mode = opcode[i + 1]
        if mode == '\x01':
            print str(i).zfill(3), "flag = reg[{}] ^= {}".format(u1(opcode[i + 2]), u1(opcode[i + 3]))
        i += 4
        cnt += 1
    elif opcode[i] == '\xcf':
        mode = opcode[i + 1]
        if mode == '\x00':
            print str(i).zfill(3), "flag = reg[{}] - reg[{}]".format(u1(opcode[i + 2]), u1(opcode[i + 3]))
        i += 4
        cnt += 1
    elif opcode[i] == '\xd1':
        print str(i).zfill(3), "jmp +{}, if flag != 0".format(u1(opcode[i + 1]))
        i += 2
        cnt += 1
    elif opcode[i] == '\xd5':
        print str(i).zfill(3), "jmp {}, if flag >= 0".format(u1(opcode[i + 1]))
        i += 2
        cnt += 1
    elif opcode[i] == '\xac':
        print str(i).zfill(3), "flag = (reg[{}] -= 1)".format(u1(opcode[i + 2]))
        i += 3
        cnt += 1
    elif opcode[i] == '\xff':
        print str(i).zfill(3), "break"
        i += 1
    else:
        print "Unhandled opcode", repr(opcode[i])
        break

print "total", cnt, "ins"
```

Output dari parser,

```
000 data[0] = 100
004 data[1] = 91
008 data[2] = 27
012 data[3] = 90
016 data[4] = 113
020 data[5] = 111
024 data[6] = 113
028 data[7] = 125
032 data[8] = 71
036 data[9] = 67
040 data[10] = 94
044 data[11] = 66
048 data[12] = 75
052 data[13] = 113
056 data[14] = 97
060 data[15] = 94
064 data[16] = 77
068 data[17] = 30
072 data[18] = 74
076 data[19] = 29
080 data[20] = 36
084 data[21] = 46
088 reg[5] = 1
092 reg[0] = 20
096 reg[1] = 42
100 reg[3] = data[reg[1]]
104 flag = reg[3] ^= 46
108 reg[4] = data[reg[0]]
112 flag = reg[3] - reg[4]
116 jmp +14, if flag != 0
118 flag = (reg[1] -= 1)
121 flag = (reg[0] -= 1)
124 jmp -24, if flag >= 0
126 reg[5] = 0
130 break
total 34 ins
```

pada bytes 000 - 084 ada inisialisasi data yang sepertinya akan dijadikan sebuah konstanta cek. Oh iya, perlu diperhatikan juga, data[22] sampai data[44] digunakan untuk user input.

```
088 reg[5] = 1
092 reg[0] = 20
096 reg[1] = 42
100 reg[3] = data[reg[1]]
104 reg[3] ^= 46
108 reg[4] = data[reg[0]]
112 flag = reg[3] - reg[4]
116 jmp +14, if flag != 0
118 flag = (reg[1] -= 1)
121 flag = (reg[0] -= 1)
124 jmp -24, if flag >= 0
126 reg[5] = 0
130 break
```

Ugh.. nani!?!?! Ubah ke pseudo-C agar lebih mudah dibaca,

```
reg[5] = 1;
reg[0] = 20;
reg[1] = 42;
_loop:
if (data[reg[1]--] ^ 46 != data[reg[0]])
    goto _exit;
else
    goto _loop;
reg[5] = 0;
_exit:
    break;
```

Setidaknya hasilnya lebih nyaman dibaca. Terus, Apasih yang dilakukan? reg[0] dan reg[1] jadi counter untuk loop. Awal reg[1] => 42, daerah user input, reg[0] => 20, daerah data yang diinisialisasi sebelumnya. So, ini cuma xor data di user input dengan 46 dan mengeceknya dengan konstan data yang diinisialisasi sebelumnya. Boom. Buat solver-nya,

```
data = [100,91,27,90,113,111,113,125,71,67,94,66,75,113,97,94,77,30,74,29,36,46]
raw = map(chr, map(lambda x: x ^ 46, data))
print ''.join(raw)
```

Output dari solver-nya dan check pada soal:

```
λ › python solve.py
Ju5t_A_Simple_Opc0d3

λ › python ./vm
Simple VM
Masukkan password : Ju5t_A_Simple_Opc0d3
Password Benar
```

FLAG : `JOINTS18{Ju5t_A_Simple_Opc0d3}`

* * *

Ada sedikit cerita dramatis pas solve soal ini karena baru bisa solve pas **_banget_** waktu untuk submit flag baru ditutup. Yep, setidaknya sempet ngerjain soal yang unik satu ini :v. Kudos untuk siapapun yang buat soal. Gud juga. Kerad. Sangad.