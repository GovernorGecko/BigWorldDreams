"""
    Perlin Noise Learning/Tests
"""

import os

# from perlin_noise import PerlinNoise

from src.atlas import Atlas
# from src.chunk import Chunk
# from src.heightmap import create_heightmap

atlas = Atlas("./files", size=300)
atlas.add_image("test.png")
atlas.add_image("test.png")
print(atlas.get_json())
print(atlas.get_texture("test.pn"))

path_to_store = "./tests"

if not os.path.exists(path_to_store):
    os.mkdir(path_to_store)

# create_heightmap(2, 4, "chunk", path_to_store)
