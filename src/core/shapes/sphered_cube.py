"""
sphered_cube
"""

from ...ext.pyMultiD.vector import Vector2f, Vector3f

from ...ext.pyGraphics.shape import Shape
from ...ext.pyGraphics.shapes.box import generate_box


def sphered_cube(block_size, radius):
    """
    parameters
        float
        float
    """

    if not isinstance(block_size, (int, float)) or not isinstance(radius, (int, float)):
        raise ValueError("Expected an Int or Float for block size and radius.")

    shape = Shape()

    # The idea is we start at center.  We then go as far along the z axis as we can and
    # begin usign a spiral system to add boxes all the way back along the z axis.
    center = Vector3f(0.0, 0.0, 0.0)

    z_axis_max = 0.0
    while center.distance(Vector3f(0.0, 0.0, z_axis_max)) <= radius:
        z_axis_max += block_size

    # For Box Rendering
    half_block_size = block_size / 2
    half_block = Vector3f(half_block_size, half_block_size, half_block_size)

    # Start at max for moving along the z-axis
    current_z_axis = z_axis_max

    while True:
        # Clear our current offset
        offset_current = 0.0

        # Iterate as long as we have a found a block to add
        found = True
        while found:
            offset_list = []

            # This is for our center z-axis
            if offset_current == 0.0:
                offset_list.append(Vector3f())

            else:
                # x right, y max
                x = -offset_current
                while x < offset_current:
                    offset_list.append(Vector3f(x, offset_current, 0.0))
                    x += block_size

                # y down, x max
                y = offset_current
                while y > -offset_current:
                    offset_list.append(Vector3f(offset_current, y, 0.0))
                    y -= block_size

                # x left, y min
                x = offset_current
                while x > -offset_current:
                    offset_list.append(Vector3f(x, -offset_current, 0.0))
                    x -= block_size

                # y up, x min
                y = -offset_current
                while y < offset_current:
                    offset_list.append(Vector3f(-offset_current, y, 0.0))
                    y += block_size

            found = False
            for v in offset_list:
                current_block = Vector3f(0.0, 0.0, current_z_axis) + v

                # Block in our radius?
                if current_block.distance(center) <= radius:
                    b = generate_box(
                        current_block - half_block,
                        current_block + half_block,
                        [Vector2f(0.0, 0.0)] * 6,
                        Vector2f(1.0, 1.0),
                    )

                    shape.add(b)

                    # Keep our Loop going
                    found = True

            # For Min/Max Spiral
            offset_current += block_size

        # Moving along our z-axis
        current_z_axis -= block_size
        if current_z_axis <= -z_axis_max:
            break

    return shape
