"""
https://github.com/Mindwerks/worldengine

import rawpy
import imageio

path = 'assets/heightmap.raw'
with rawpy.imread(path) as raw:
    rgb = raw.postprocess()
imageio.imsave('default.tiff', rgb)
"""
