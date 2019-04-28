import bpy
from bpy.types import (Panel, Operator)
from bpy.props import (StringProperty)
import os
import sys
# import cv2
# import pydicom

def read_dicom_image(path):
    if(os.path.isfile(path)):
        print('Reading file {}'.format(path))
        ds = pydicom.dcmread(path, force=True)
        ds.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
        img = ds.pixel_array
        # creating png
        cv2.imwrite(path.replace('.dcm', '.png'), img)
        return path.replace('.dcm', '.png')
    else:
        print('invalid path!')


def process_image(path):
    return -1  # TODO


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
        scene.render.engine = 'CYCLES'

        print(scene.images_dir_prop)

        if os.path.isdir(scene.images_dir_prop):
            img_list = [f for f in os.listdir(
                scene.images_dir_prop) if f.endswith('.dcm')]

            print("Got %d images" % (len(img_list)))
            layer_depth = 0.01  # TODO allow user to change this

            # For each image
            for i in range(1, len(img_list)):
                id = img_list[i-1]
                print('Doing {}'.format(id))

                mat = bpy.data.materials.new(name=id)
                bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, layer_depth*i), layers=(
                    True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
                obj = context.active_object
                # add texture to material
                node_tree = bpy.data.materials[id].node_tree
                node = node_tree.nodes.new("ShaderNodeTexImage")

                # read the dicom image, generate a png of it
                png_path = read_dicom_image(id)
                bpy.data.images.load(png_path, check_existing=True)

                # use png as image texture
                segmented_img = bpy.data.images[os.path.split(png_path)[1]]
                node.image = segmented_img

                # set texture to active
                node.select = True
                node_tree.nodes.active = node

                if obj.data.materials:
                    obj.data.materials[0] = mat
                else:
                    obj.data.materials.append(mat)

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
