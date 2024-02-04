"""
    obj generator

    Order of faces position/texcoord/normal

    https://www.loc.gov/preservation/digital/formats/fdd/fdd000508.shtml
    Ka: specifies ambient color, to account for light that is scattered about
    the entire scene.
    Kd: specifies diffuse color, which typically contributes most of the color
    to an object.
    Ks: specifies specular color, the color seen where the surface is shiny
    and mirror-like.
    Ns: defines the focus of specular highlights in the material. Ns values
    normally range from 0 to 1000, with a high value resulting in a tight,
    concentrated highlight.
    Ni: defines the optical density (aka index of refraction) in the current
    material. The values can range from 0.001 to 10. A value of 1.0 means that
    light does not bend as it passes through an object.
    d: specifies a factor for dissolve, how much this material dissolves into
    the background. A factor of 1.0 is fully opaque. A factor of 0.0 is
    completely transparent.
    illum: specifies an illumination model, using a numeric value.
    The value 0 represents the simplest illumination model, relying on the Kd
    for the material modified by a texture map specified in a map_Kd statement
    if present. The compilers of this resource believe that the choice of
    illumination model is irrelevant for 3D printing use and is ignored on
    import by some software applications. For example, the MTL Loader in
    the threejs Javascript library appears to ignore illum statements.
    map_Kd: specifies a color texture file to be applied to the diffuse
    reflectivity of the material. During rendering, map_Kd values are
    multiplied by the Kd values to derive the RGB components.

"""

import os

from shutil import copyfile

from ..pyHelpers.type_validation import type_validation
from ..pyMultiD.vector import Vector3f


def objfile(
    shape,
    name: str,
    image_name: str | None = None,
    image_path: str = "./",
    path: str = "./",
) -> None:
    # Validate Name/Path Type
    type_validation([name, path], str)

    # Path to store the Obj File
    if not os.path.exists(path):
        raise ValueError(f"{path} doesn't exist!")

    # We need a valid image name and path to add a mtl file
    valid_image = isinstance(image_name, str) and os.path.exists(image_path)

    # Set Material Defaults
    ka = Vector3f(1.0, 1.0, 1.0)
    kd = Vector3f(1.0, 1.0, 1.0)
    ks = Vector3f(0.0, 0.0, 0.0)
    ns = 1.0
    ni = 1.0
    d = 1.0
    illum = 1

    #  Write Obj File
    with open(os.path.join(path, name + ".obj"), "w") as file:
        # Base for Obj
        file.writelines(f"o {name}\n")

        # Image?
        if valid_image:
            file.writelines(f"\nmtllib {name}.mtl\n")

        # Positions
        if "vp" in shape.get_order():
            vp_index = shape.get_order().index("vp")
            file.writelines(
                "\nv "
                + "\nv ".join(
                    " ".join(map(str, vp.get_values_as_list()))
                    for vp in shape.get_vertex_by_index(vp_index)
                )
            )

        # Normals
        if "vn" in shape.get_order():
            vn_index = shape.get_order().index("vn")
            file.writelines(
                "\nvn "
                + "\nvn ".join(
                    " ".join(map(str, vn.get_values_as_list()))
                    for vn in shape.get_vertex_by_index(vn_index)
                )
            )

        # TexCoords
        if "vt" in shape.get_order():
            vt_index = shape.get_order().index("vt")
            file.writelines(
                "\nvt "
                + "\nvt ".join(
                    " ".join(map(str, vt.get_values_as_list()))
                    for vt in shape.get_vertex_by_index(vt_index)
                )
            )

        # Add Material
        file.writelines("\n\n")
        if valid_image:
            file.writelines("usemtl material0")
        else:
            file.writelines("usemtl Default")
        file.writelines("\n")

        # Iterate Faces
        file.writelines(
            "f "
            + "\nf ".join(
                [
                    " ".join(
                        [
                            "/".join([str(i + 1) for i in indice])
                            for indice in shape.get_indices()[triangle : triangle + 3]
                        ]
                    )
                    for triangle in range(0, len(shape.get_indices()), 3)
                ]
            )
        )

        file.writelines(f"\n\n# END OF FILE")

    # If we have an image, here we write the mtl
    if valid_image:
        # Copy the image to our path.
        copyfile(
            os.path.join(image_path, image_name),
            os.path.join(path, image_name),
        )

        # Create the mtl file
        with open(os.path.join(path, name + ".mtl"), "w") as file:
            # Base mtl
            file.writelines("newmtl material0\n")

            # Ambience
            file.writelines("Ka " + " ".join(map(str, ka.get_values_as_list())) + "\n")

            # Diffuse
            file.writelines("Kd " + " ".join(map(str, kd.get_values_as_list())) + "\n")

            # Specular
            file.writelines("Ks " + " ".join(map(str, ks.get_values_as_list())) + "\n")

            # The Rest
            file.writelines(
                f"Ns {ns}\n"
                f"Ni {ni}\n"
                f"d {d}\n"
                f"illum {illum}\n"
                f"map_Kd {image_name}"
            )
