"""
heightmap
"""

from perlin_noise import PerlinNoise

from .MultiD.src.vector import Vector2
from .ObjFile.src.generator import Generator

from .chunk import Chunk


class Heightmap:
    """
    """

    __slots__ = ["__chunks"]

    def __init__(self, chunk_count, chunk_size):

        # Chunks!
        self.__chunks = []

        # Noise Base
        noise = PerlinNoise(octaves=1, seed=1)

        # Heightmap Size
        heightmap_size = chunk_count * chunk_size

        # Build Heightmap Data
        height_data = [
            [noise(
                    [i/heightmap_size, j/heightmap_size]
                ) for j in range(heightmap_size)
            ] for i in range(heightmap_size)
        ]
        minimum_height = min(min(height_data))

        # Iterate Height Data, building chunks.
        for x in range(0, chunk_count):
            for y in range(0, chunk_count):
                chunk_start = x * chunk_size
                chunk_end_x = chunk_start + chunk_size
                chunk_data = [height_data[i][chunk_start:chunk_end] for i in range(chunk_start,chunk_end)]
                self.__chunks.append(Chunk(chunk_data, minimum_height=minimum_height, top_only=True))
        
        """
        # Obj Generator
        generator = Generator("test")

        for triangle in chunk.get_triangles():
            generator.add_triangle(triangle.get_positions())
        generator.save("./tests")
        """
        
