from src.ext.pyGraphics.objfile import objfile
from src.ext.pyHelpers.files import create_or_delete
from src.ext.pyHelpers.math import get_max_and_min_from_list
from src.ext.pyMultiD.vector import Vector2f, Vector3f

from src.core.characters.complex.human import generate_human
from src.core.shapes.boxes import generate_boxes
from src.core.shapes.heightmap import (
    generate_heightmap,
    generate_heightmap_json,
    get_slice_from_heightmap,
)

create_or_delete("./results")


human = generate_human()
human.set_root(human.get("head_human_large"))


human.create_frame("idle1")

human.export("chrono_animations", path="../aDream/Content/Objects")

objfile(
    human.get("head_human_large").render(Vector2f(0.0, 0.0), False),
    "c",
    path="./results",
)


"""
heightmap_json = generate_heightmap_json(20, 20)

heightmap = generate_heightmap(
    heightmap_json,
    Vector2f(0.0, 0.0),
    Vector2f(0.0, 0.0625),
    Vector2f(0.0625, 0.0625),
)
heightmap.center_on_origin()
objfile(
    heightmap,
    "heightmap_0",
    path="../aDream/Content/Models",
)

sliced = get_slice_from_heightmap(heightmap_json, 1)

max_min = get_max_and_min_from_list(sliced)

print(max_min)
print(len(sliced))
print(sliced)
"""

"""
# BOXES
boxes = generate_boxes(
    2,
    1.0,
    [
        Vector2f(0.0, 0.0625),
        Vector2f(0.0, 0.0),
        Vector2f(0.0, 0.0),
        Vector2f(0.0, 0.0),
        Vector2f(0.0, 0.0),
        Vector2f(0.0, 0.0),
    ],
    Vector2f(0.0625, 0.0625),
)
boxes.center_on_origin()
# boxes.cull_vertices()
objfile(
    boxes,
    "heightmap_0",
    path="./results",
)
"""


"""
# ATLAS
from src.ext.pyGraphics.atlas import Atlas

a = Atlas("../_files/")
a.add_image("grass_sides_and_bottom.png")
a.add_image("grass_top.png")
a.save("./results")
"""
