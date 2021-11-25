"""
    BigWorldDreams Tests
"""

import os

from src.atlas import Atlas
from src.heightmap import create_heightmap

paths = {
    "blender": "C:/Program Files/Blender Foundation/Blender 2.91/blender.exe",
    "script": "c:/repos/BigWorldDreams/src/bpy_obj_to_fbx.py",
    "results": "c:/repos/BigWorldDreams/results/",
}

area_size = 8
tile_size = 4

atlas = Atlas("./files", size=1024)
atlas.add_image("grass_top.png", "grass_top")
atlas.add_image("grass_sides_and_bottom.png", "grass_sides_and_bottom")
print(atlas.get_json())
# print(atlas.get_texture_coords("test.png"))
atlas.save("./")

path_to_store = "./results"

if not os.path.exists(path_to_store):
    os.mkdir(path_to_store)
else:
    for file in os.scandir(path_to_store):
        os.remove(file.path)

create_heightmap(area_size, tile_size, "tile", atlas, path_to_store)

# blender_path = input("Blender Path: ")
# script_path = input("Script Path: ")
# results_path = input("Results Path: ")

stream = os.popen(
    f'"{paths["blender"]}" --background '
    f'--python "{paths["script"]}" '
    f'-- "{paths["results"]}"'
)
output = stream.read()
