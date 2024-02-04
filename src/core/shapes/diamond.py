"""
diamond.py

Make Jagged so they slot into each other?
"""

from ...ext.pyMultiD.vector import Vector2f, Vector3f

from ...ext.pyGraphics.shape import Shape
from ...ext.pyGraphics.shapes.box import generate_box


def generate_diamond(tiers, block_size=1.0):
    """
    parameters
        int
        (optional)
            float
    """

    if not isinstance(tiers, int) or tiers < 1:
        raise ValueError("Tiers must be an int > 0.")
    elif not isinstance(block_size, float) or block_size <= 0.0:
        raise ValueError("Block Size must be a float > 0.0.")

    shape = Shape()

    half_block = Vector3f(block_size * 0.5, block_size * 0.5, block_size * 0.5)

    current_tier = 1
    while current_tier <= tiers:
        block_count = current_tier + current_tier - 1
        tier_offset = 1 - current_tier

        for z in range(block_count):
            for x in range(block_count):
                # Center our Box
                block = Vector3f(
                    float(x + tier_offset), float(current_tier), float(z + tier_offset)
                )

                shape.add(
                    generate_box(
                        block - half_block,
                        block + half_block,
                        [Vector2f(0.0, 0.0)] * 6,
                        Vector2f(1.0, 1.0),
                    )
                )

        current_tier += 1

    return shape
