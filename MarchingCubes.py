import bpy
from bpy.types import (Panel, Operator)
from bpy.props import (StringProperty)
import os


class MarchingCubesPanel(Panel):
    bl_idname = "OBJECT_PT_marching_cubes"
    bl_label = "Marching Cubes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Create"  # creates the addon panel in the create tab in tools region

    path = ""

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Construct 3D model from 2D scans")  # TODO add icon

        row = layout.row()
        row.label(text="Select a directory with CT/MRI images")

        row = layout.row()
        row.prop(context.scene, "images_dir_prop")

        row = layout.row()
        row.operator("object.marching_cubes")  # TODO check this line


class MarchingCubes(Operator):
    bl_idname = "object.marching_cubes"
    bl_label = "Marching Cubes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene

        print(scene.images_dir_prop)

        if os.path.isdir(scene.images_dir_prop):
            img_list = [f for f in os.listdir(
                scene.images_dir_prop) if f.endswith('.dcm')]
            # Got image list
            for img in img_list:
                print(img)
                # Do something to each image?
            print("Got %d images" % (len(img_list)))
        return {'FINISHED'}


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
