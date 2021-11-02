"""
    BigWorldDreams Tests
"""

import os

from src.atlas import Atlas
from src.heightmap import create_heightmap

atlas = Atlas("./files", size=1024)
atlas.add_image("grass_top.png", "grass_top")
atlas.add_image("grass_sides_and_bottom.png", "grass_sides_and_bottom")
# print(atlas.get_json())
# print(atlas.get_texture_coords("test.png"))
atlas.save("./")

path_to_store = "./tests"

if not os.path.exists(path_to_store):
    os.mkdir(path_to_store)

create_heightmap(2, 4, "chunk", atlas, path_to_store)
