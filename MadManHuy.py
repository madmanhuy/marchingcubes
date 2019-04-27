import bpy
from bpy.props import (StringProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )
import os
# import marching_cubes

bl_info = {
    "name": "Marching Cubes",
    "location": "View3D > Toolshelf > Marching Cubes",
    "description": "Takes a directory of CT/MRI scans and converts them into a 3d Mesh",
    "category": "Add Mesh",
}


class MarchingCubes(bpy.types.Operator):
    bl_idname = "object.marchingcubes"
    bl_label = "Marching Cubes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        col = layout.column(align=True)
        col.prop(scene.my_tool, "path", text="")

        # print the path to the console
        print(scene.my_tool.path)

        img_list = [f for f in os.listdir(
            scene.my_tool.path) if f.endswith('.dcm')]

        for img in img_list:
            print(os.path.join(scene.my_tool.path, img))

        return {'FINISHED'}


class MySettings(bpy.types.PropertyGroup):
    path = StringProperty(
        name="",
        description="Path to Directory",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')


def register():
    bpy.utils.register_class(MarchingCubes)
    bpy.utils.register_class(MySettings)
    bpy.types.Scene.my_tool = PointerProperty(type=MySettings)


def unregister():
    bpy.utils.unregister_class(MarchingCubes)
    bpy.utils.unregister_class(MySettings)
    del bpy.types.Scene.my_tool


# Run script in blender text editor without
# installing the module
if __name__ == "__main__":
    register()
