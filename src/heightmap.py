"""
    heightmap
"""

import json
import os

from perlin_noise.perlin_noise import PerlinNoise

from .chunk import Chunk
from .MultiD.src.vector import Vector2


def create_heightmap(chunk_count, chunk_size, name, atlas, path="."):
    """
    parameters
        int
            Number of chunks to generate
        int
            Size of each chunk (#x#)
        string
            Name to prefix data with.
        (optional)
        string
            Path to store everything.
    """

    # Json
    json_data = {
        "name": name,
        "chunk_count": chunk_count,
        "chunk_size": chunk_size,
        "chunks": [],
    }

    # Noise Base
    noise = PerlinNoise(octaves=1, seed=1)

    # Heightmap Size
    heightmap_size = chunk_count * chunk_size

    # Build Heightmap Data
    height_data = [
        [
            noise(
                [i/heightmap_size, j/heightmap_size]
            ) for j in range(heightmap_size)
        ] for i in range(heightmap_size)
    ]
    minimum_height = min(min(height_data))

    # Iterate Height Data, building chunks.
    i = 0
    for x in range(0, chunk_count):
        for y in range(0, chunk_count):

            # Chunk Start Position
            chunk_start = Vector2(
                float(x * chunk_size),
                float(y * chunk_size)
            )

            # Chunk End Position
            chunk_end = Vector2(
                float(chunk_start.X + chunk_size),
                float(chunk_start.Y + chunk_size)
            )

            # Chunk Data, pulled from Heightmap
            chunk_data = [
                height_data[i][
                    int(chunk_start.X):int(chunk_end.X)
                ] for i in range(
                    int(chunk_start.Y), int(chunk_end.Y))
            ]

            # Chunk Name
            chunk_name = f"chunk_{i}"

            # Build the chunk
            chunk = Chunk(
                chunk_name, chunk_data, atlas,
                minimum_height=minimum_height,
                top_only=False
            )

            # Store the obj file
            chunk.save(path)

            # Add to json
            json_data["chunks"].append(
                {
                    "x": x,
                    "y": y,
                    "name": chunk_name
                }
            )

            # Chunk count
            i += 1

    # Dump the data!
    path_to_store = os.path.join(path, f"{name}.json")
    with open(path_to_store, 'w') as outfile:
        json.dump(json_data, outfile, indent=4)
    # print(json_data)
