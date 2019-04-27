import bpy
from bpy.types import (Operator)
from bpy.props import (StringProperty)
import os
from madmanhuy import read_dicom_image


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
