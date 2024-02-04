"""
box.py
"""

from ...pyMultiD.vector import Vector2f, Vector3f
from ...pyHelpers.type_validation import type_validation

from .quadrilateral import generate_quadrilateral
from ..shape import Shape
from ..vertex import VertexPositionNormalTexture


def generate_box(
    minimum,
    maximum,
    texture_minimums=[Vector2f(0.0, 0.0)] * 6,
    texture_size=Vector2f(1.0, 1.0),
    faces_toggle_list=[True, True, True, True, True, True],
):
    """
    parameters
        Vector3f
        Vector3f
        List<Vector2f>
            order y+, x+, x-, z+, z-, y-
        Vector2f
    returns
        Shape

    Textures
        0 = y+ (top)
        1 = x+ (right)
        2 = x- (left)
        3 = z+ (back)
        4 = z- (front)
        5 = y- (bottom)
    """

    type_validation(
        [
            [texture_minimums, faces_toggle_list],
            texture_size,
            [minimum, maximum],
        ],
        [list, Vector2f, Vector3f],
    )

    if (
        not all(isinstance(i, Vector2f) for i in texture_minimums)
        or len(texture_minimums) != 6
    ):
        raise ValueError("Texture Minimums must be a size six Vector2f list.")
    elif (
        not all(isinstance(i, bool) for i in faces_toggle_list)
        or len(faces_toggle_list) != 6
    ):
        raise ValueError("Faces must be a list of size six True/False list.")

    points = [
        # p1
        Vector3f(minimum.X, maximum.Y, maximum.Z),
        # p2
        Vector3f(maximum.X, maximum.Y, maximum.Z),
        # p3
        Vector3f(minimum.X, maximum.Y, minimum.Z),
        # p4
        Vector3f(maximum.X, maximum.Y, minimum.Z),
        # p5
        Vector3f(minimum.X, minimum.Y, maximum.Z),
        # p6
        Vector3f(maximum.X, minimum.Y, maximum.Z),
        # p7
        Vector3f(minimum.X, minimum.Y, minimum.Z),
        # p8
        Vector3f(maximum.X, minimum.Y, minimum.Z),
    ]

    """    
           x
        p1----p2
       /|     /|
      p3----p4 | y
      | p5---|p6
      |/     |/ z
      p7----p8

      p7 = min
      p2 = max

      looking thru front to back, mapping
      tl -> br
      tr -> bl
      br -> tl
      bl -> tr
    """
    faces = {
        # y+ top
        0: [0, 1, 3, 2],
        # x+ (right)
        1: [7, 5, 1, 3],
        # x- (left)
        2: [0, 2, 6, 4],
        # z+ (back)
        3: [5, 4, 0, 1],
        # z- (front)
        4: [2, 3, 7, 6],
        # y- (bottom)
        5: [7, 6, 4, 5],
    }

    # New Shape
    shape = Shape(VertexPositionNormalTexture)

    # Grab Faces, checking if we want the face
    for id, face in faces.items():
        if faces_toggle_list[id]:
            shape.add(
                generate_quadrilateral(
                    points[face[0]],
                    points[face[1]],
                    points[face[2]],
                    points[face[3]],
                    texture_minimums[id],
                    texture_size,
                )
            )

    # Return
    return shape


def generate_box_from_whd(width, height, depth, texture_minimums, texture_size):
    """
    parameters
        float
        float
        float
        List<Vector2f>
        Vector2f
    returns
        Shape
    """

    # No need to validate texture, we'll do that in a following call
    type_validation([width, height, depth], (float, int))

    center = Vector3f()
    offset = Vector3f(width * 0.5, height * 0.5, depth * 0.5)

    return generate_box(
        center - offset, center + offset, texture_minimums, texture_size
    )
