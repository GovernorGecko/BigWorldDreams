"""
x	pad byte	        no value
c	char	            bytes of length     1	1
b	signed char	        integer	            1	(1),(3)
B	unsigned char	    integer	            1	(3)
?	_Bool	            bool	            1	(1)
h	short	            integer	            2	(3)
H	unsigned short	    integer	            2	(3)
i	int	                integer	            4	(3)
I	unsigned int	    integer	            4	(3)
l	long	            integer	            4	(3)
L	unsigned long	    integer	            4	(3)
q	long long	        integer	            8	(2), (3)
Q	unsigned long long	integer         	8	(2), (3)
n	ssize_t	            integer	 	            (4)
N	size_t	            integer	 	            (4)
f	float	            float	            4	(5)
d	double	            float	            8	(5)
s	char[]	            bytes
p	char[]	            bytee
P	void *	            integer	 	            (6)

accessors -> componentType
5123    UNSIGNED_SHORT
5126    FLOAT

bufferViews -> target (optional)
34962   GL_ARRAY_BUFFER
34963   GL_ELEMENT_ARRAY_BUFFER

i: 0, 1, 2, 1, 2, 3
(0,1,0)
(1,0,0)
(1,1,0)
(0,0,0)

fout = open('simpleTriangle.bin', 'wb')

# Unsigned Short 2 Bytes
for i in [0, 1, 2]:
    fout.write(struct.pack('>H', i))

# Float 4 Bytes
for i in [0, 1, 0, 1, 0, 0, 1, 1, 0]:
    fout.write(struct.pack('>f', i))

fout.close()
"""
# import struct

from src.gltf.generator import Generator

g = Generator()
g.add_attribute_sequence((0.0, 1.0, 0.0))
g.add_attribute_sequence((0.0, 1.0, 0.0))
print(g)
