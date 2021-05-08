"""
i: 0, 1, 2, 1, 2, 3
(0,1,0)
(1,0,0)
(1,1,0)
(0,0,0)

fout = open('simpleTriangle.bin', 'wb')

# Unsigned Short 2 Bytes
for i in [0, 1, 2]:
    fout.write(struct.pack('>H', i))

# Float 4 Bytes
for i in [0, 1, 0, 1, 0, 0, 1, 1, 0]:
    fout.write(struct.pack('>f', i))

fout.close()
"""
# import struct

from src.gltf.generator import Generator
# from src.gltf.accessor import Accessor
# from src.gltf.bufferview import BufferView

# b = BufferView(0, 12, 1)
# print(b)

# a = Accessor(5126, "VEC3", 3)
# print(a.get_byte_stride())
# print(a)

g = Generator("test", ["POSITION", "TEXTURE", "NORMAL"])
g.add_attribute_sequence((0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0))
g.add_attribute_sequence((1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0))
g.add_attribute_sequence((1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0))
# print(g)
g.save("assets")
