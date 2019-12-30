from PIL import Image
from struct import unpack

u32 = lambda x : unpack("<I", x)[0]
u8 = lambda x : unpack("<B", x)[0]
uRGB = lambda x : unpack("<BBB", x)

with open('flag.png.kpk', 'rb') as f:
    data = f.read()
    length = len(data)

assert(data[0:4] == "\x7FKPK")

width = u32(data[4:8])
height = u32(data[8:12])

pos = 12

pixels = []

while len(pixels) < width * height:
    rl = u8(data[pos:pos+1])
    for _ in range(rl):
        pixels.append(uRGB(data[pos+1:pos+4]))
    pos += 4

img = Image.new('RGB', (width, height))
img.putdata(pixels)
img.save('flag_recovered.png')