import bpy
from bpy.types import (Panel, Operator)
from bpy.props import (StringProperty)
import os
import sys
import cv2
import pydicom

bl_info = {
    "name" : "Marching Cubes",
    "author" : "Huy Ha, Maddy Placik, Mandeep Bhutani",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Object"
}

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
        print('invalid path: ' + path)


def process_image(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # threshold to segment
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # open image
    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    open = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, se)
    open = (255-open)
    image = cv2.cvtColor(open, cv2.COLOR_BGR2RGBA)
    image[np.all(image == [0, 0, 0, 255], axis=2)] = [0, 0, 0, 0]
    cv2.imwrite(path, image)
    return path


class PANEL_PT_marching_cubes_panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_idname = "OBJECT_PT_marching_cubes"
    bl_label = "Marching Cubes"
    bl_context = "objectmode"
    bl_category = "Marching Cubes"

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

# following naming convention outlined in 
# https://wiki.blender.org/wiki/Reference/Release_Notes/2.80/Python_API/Addons
class OBJECT_OT_marching_cubes(Operator):
    bl_idname = "object.marching_cubes"
    bl_label = "Marching Cubes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        scene.render.engine = 'CYCLES'

        if os.path.isdir(scene.images_dir_prop):
            img_list = [f for f in os.listdir(
                scene.images_dir_prop) if f.endswith('.dcm')]

            print("Got %d images" % (len(img_list)))
            layer_depth = 0.01  # TODO allow user to change this

            # For each image
            for i in range(0, len(img_list)):
                id = img_list[i]
                print('Doing {}'.format(id))

                
                obj = bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, layer_depth*i), layers=(
                    True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
                
                #create new material
                mat = bpy.data.materials.new(name=id)
                mat.use_nodes = True

                # add texture to material
                node_tree = bpy.data.materials[id].node_tree
                node = node_tree.nodes.new("ShaderNodeTexImage")

                # read the dicom image, generate a png of it
                png_path = read_dicom_image( os.path.join(scene.images_dir_prop,id))
                print('Got png path:' + png_path)
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
    bpy.utils.register_class(OBJECT_OT_marching_cubes)
    bpy.utils.register_class(PANEL_PT_marching_cubes_panel)
    bpy.types.Scene.images_dir_prop = bpy.props.StringProperty(
        name="Image Directory",
        description="Filepath to folder containing CT/MRI scans for Marching Cube operator",
        default=""
    )


def unregister():
    bpy.utils.unregister_class(PANEL_PT_marching_cubes_panel)
    bpy.utils.unregister_class(OBJECT_OT_marching_cubes)
    del bpy.types.Scene.images_dir_prop


if __name__ == "__main__":
    register()
