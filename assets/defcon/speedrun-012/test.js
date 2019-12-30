var a = new OOOBufferOOO(64);
print(a.readUInt8(66));
a.writeUInt32LE(99, 66);
print(a.readUInt8(66));