# BigWorldDreams
Open World Generator

Generates Tiles of X by X, infinite height.
These can be Top Only, or filled in
Each Tile comes with a JSON file that is list of array of heights (if caves)

# TODO
- Simple Collision Json Output
- Atlas Tweaks
    - 0,0 starts at bottom left of image
    - need slice off a pinch from each side to make it look better
    - We pass Atlas to create_heightmap, generator also copies the texture file used
- Shapes
    - Cube
    - Half Cube
    - Wedge