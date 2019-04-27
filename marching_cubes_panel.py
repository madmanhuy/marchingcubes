import bpy
from bpy.types import (Operator)


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
        row.operator("object.marching_cubes")
