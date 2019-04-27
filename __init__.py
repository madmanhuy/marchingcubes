bl_info = {
    "name": "MarchingCubes",
    'author': 'Mandeep Bhutani, Maddy Placik, Huy Ha',
    "location": "View3D > Tools > Create",
    "category": "3D View"
}

if "bpy" in locals():
    import imp
    imp.reload(MarchingCubes)
    imp.reload(MarchingCubesPanel)
    imp.reload(read_dicom_image)
    imp.reload(os)
    print("Reloaded multifiles")
else:
    import bpy
    from bpy.types import (Panel, Operator)
    from bpy.props import (StringProperty)
    import os
    from madmanhuy import read_dicom_image
    from marching_cubes import MarchingCubes
    from marching_cubes_panel import MarchingCubesPanel


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.images_dir_prop = bpy.props.StringProperty(
        name="Image Directory",
        description="Filepath to folder containing CT/MRI scans for Marching Cube operator",
        default=""
    )


def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.images_dir_prop


if __name__ == "__main__":
    register()
