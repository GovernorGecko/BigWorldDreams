"""
blender obj to fbx

blender --background --python ...\\bpy_obj_to_fbx.py -- ...\\results
"""

import bpy
import os
import sys

name = "Collection"
remove_collection_objects = True

coll = bpy.data.collections.get(name)

if coll:
    if remove_collection_objects:
        obs = [o for o in coll.objects if o.users == 1]
        while obs:
            bpy.data.objects.remove(obs.pop())

    bpy.data.collections.remove(coll)

argv = sys.argv
# get all args after "--"
argv = argv[argv.index("--") + 1:]

base_path_obj = argv[0]

for filename in os.listdir(base_path_obj):
    if filename.endswith(".obj"):

        path_to_obj = os.path.join(base_path_obj, filename)
        path_to_fbx = os.path.join(
            base_path_obj, f"{os.path.splitext(filename)[0]}.fbx"
        )

        bpy.ops.import_scene.obj(
            filepath=path_to_obj, axis_forward='-Z', axis_up='Y'
        )
        bpy.ops.export_scene.fbx(
            filepath=path_to_fbx, axis_forward='-Z', axis_up='Y'
        )
