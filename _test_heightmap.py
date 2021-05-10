"""
Perlin Noise Learning/Tests
"""

from perlin_noise import PerlinNoise

from src.gltf.generator import Generator
from src.world.chunk import Chunk

# Noise Base
noise = PerlinNoise(octaves=1, seed=1)

# Size of our Chunk
size = 16

# Create the height data
height_data = [[noise([i/size, j/size]) for j in range(size)] for i in range(size)]
minimum_height = min(min(height_data))

# Chunkkk!
chunk = Chunk(height_data, minimum_height=minimum_height)
# print(chunk.get_vertex_data())

# Generator?
generator = Generator("heightmap_test", ["POSITION", "NORMAL", "TEXTURE"])

for vertices in chunk.get_vertex_data():
    generator.add_attribute_sequence(vertices)

generator.save("assets")


"""
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

noise = PerlinNoise(octaves=10, seed=1)
xpix, ypix = 100, 100
pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]

plt.imshow(pic, cmap='gray')
plt.show()

"""

"""
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

noise1 = PerlinNoise(octaves=3)
noise2 = PerlinNoise(octaves=6)
noise3 = PerlinNoise(octaves=12)
noise4 = PerlinNoise(octaves=24)

xpix, ypix = 100, 100
pic = []
for i in range(xpix):
    row = []
    for j in range(ypix):
        noise_val =         noise1([i/xpix, j/ypix])
        noise_val += 0.5  * noise2([i/xpix, j/ypix])
        noise_val += 0.25 * noise3([i/xpix, j/ypix])
        noise_val += 0.125* noise4([i/xpix, j/ypix])

        row.append(noise_val)
    pic.append(row)

plt.imshow(pic, cmap='gray')
plt.show()

"""
