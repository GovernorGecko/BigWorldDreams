"""
    BigWorldDreams Tests
"""

import os
import shutil

from src.atlas import Atlas
from src.heightmap import create_heightmap

paths = {
    "blender": "C:/Program Files/Blender Foundation/Blender 2.91/blender.exe",
    "script": "c:/repos/BigWorldDreams/src/bpy_obj_to_fbx.py",
    "results": "c:/repos/BigWorldDreams/results/",
}

area_size = 4
tile_size = 16

atlas = Atlas("./files", size=1024)
atlas.add_image("grass_top.png", "grass_top")
atlas.add_image("grass_sides_and_bottom.png", "grass_sides_and_bottom")
print(atlas.get_json())
# print(atlas.get_texture_coords("test.png"))
atlas.save("./")

if not os.path.exists(paths["results"]):
    os.mkdir(paths["results"])
else:
    for root, dirs, files in os.walk(paths["results"]):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

create_heightmap(
    area_size,
    tile_size,
    "tile",
    atlas,
    paths["results"]
)

# blender_path = input("Blender Path: ")
# script_path = input("Script Path: ")
# results_path = input("Results Path: ")

stream = os.popen(
    f'cd "{paths["results"]}" && '
    f'"{paths["blender"]}" --background '
    f'--python "{paths["script"]}" '
    f'-- "./"'
)
output = stream.read()
# print(output)


def move_results_to_subfolder(file_type, subfolder):
    """
    Searches our results folder for the given file type to
    the given subfolder.
    """

    files_to_move = os.listdir(paths["results"])
    for file in files_to_move:
        if file.endswith(file_type):
            if not os.path.exists(
                os.path.join(
                    paths["results"], subfolder
                )
            ):
                os.mkdir(
                    os.path.join(
                        paths["results"], subfolder
                    )
                )
            shutil.move(
                os.path.join(
                    paths["results"], file
                ),
                os.path.join(
                    paths["results"], subfolder, file
                )
            )


move_results_to_subfolder("obj", "obj")
move_results_to_subfolder("mtl", "obj")
move_results_to_subfolder("fbx", "fbx")
move_results_to_subfolder("json", "json")

# shutil.copy(
#   os.path.join(
#       paths["results"], "atlas.png"
#   ), os.path.join(
#       paths["results"], "obj", "atlas.png"
#   )
# )
