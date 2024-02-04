"""
boxes.py

boxes piled on top of each other and beside each other
in the form of a bigger box.
"""


from ...ext.pyGraphics.shape import Shape
from ...ext.pyGraphics.shapes.box import generate_box
from ...ext.pyGraphics.vertex import VertexPositionNormalTexture
from ...ext.pyMultiD.vector import Vector2f, Vector3f


def generate_boxes(
    count,
    size=1.0,
    texture_minimums=[Vector2f(0.0, 0.0)] * 6,
    texture_size=Vector2f(1.0, 1.0),
):
    """
    parameters
        int
    returns
        Shape
    """

    # Validate
    if not isinstance(count, int) or count <= 0:
        raise ValueError("Count must be an int and greater than 0.")
    elif not isinstance(size, float) or size <= 0.0:
        raise ValueError("Size must be an float and greater than 0.0")

    # Shape to Return
    shape = Shape(VertexPositionNormalTexture)

    box_size = Vector3f(size, size, size)

    for x in range(count):
        for y in range(count):
            for z in range(count):
                box_minimum = Vector3f(float(x), float(y), float(z)) * box_size
                box_maximum = box_minimum + box_size

                shape.add(
                    generate_box(
                        box_minimum,
                        box_maximum,
                        texture_minimums,
                        texture_size,
                    )
                )

    return shape
