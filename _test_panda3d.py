"""Writes a 256x256 grayscale simplex noise texture file in pgm format
(see http://netpbm.sourceforge.net/doc/pgm.html)


import sys
from noise import pnoise2, snoise2
from PIL import Image


if len(sys.argv) not in (2, 3) or '--help' in sys.argv or '-h' in sys.argv:
    print('2dtexture.py FILE [OCTAVES]')
    print()
    print(__doc__)
    raise SystemExit

"""

"""
f = open(sys.argv[1] + ".raw", 'wt')
if len(sys.argv) > 2:
    octaves = int(sys.argv[2])
else:
    octaves = 1
freq = 16.0 * octaves
f.write('P2\n')
f.write('256 256\n')
f.write('255\n')
for y in range(256):
    for x in range(256):
        f.write("%s\n" % int(snoise2(x / freq, y / freq, octaves) * 127.0 + 128.0))
f.close()
"""

"""
arr = []
for y in range(256):
    for x in range(256):
        f.write("%s\n" % int(snoise2(x / freq, y / freq, octaves) * 127.0 + 128.0))
im = Image.fromarray(arr)
im.show()
"""

from direct.showbase.ShowBase import ShowBase


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Load the environment model.
        self.scene = self.loader.loadModel("assets/triangle.gltf")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(0, 0, 0)


app = MyApp()
app.run()