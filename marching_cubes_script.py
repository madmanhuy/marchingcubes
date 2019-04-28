import bpy
from bpy.types import (Panel, Operator)
from bpy.props import (StringProperty)
import os
import sys
import cv2
import pydicom
import numpy as np


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
        ds = pydicom.dcmread(path, force=True)
        ds.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
        img = ds.pixel_array
        # creating png
        cv2.imwrite(path.replace('.dcm', '.png'), img)
        return path.replace('.dcm', '.png')
    else:
        print('invalid path: ' + path)


def process_image(path):
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
    image[np.all(image == [0, 0, 0, 255], axis=2)] = [0, 0, 0, 0]
    cv2.imwrite(path,image)
    return path

def main():
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'

    # insert path here!
    path = "C:/Users/Huy/programming/school/madmanhuy/Toshiba_Aquilion"
    # change seperation of planes here!
    layer_depth = 0.01

    # get all dicom images in path
    if os.path.isdir(path):
        img_list = [f for f in os.listdir(path) if f.endswith('.dcm')]

    print("Got %d images" % (len(img_list)))

    # For each image
    for i in range(0, len(img_list)):
        id = img_list[i]
        
        #create a plane
        bpy.ops.mesh.primitive_plane_add(size=2.0,calc_uvs=True,view_align=False,enter_editmode=False,location=(0.0,0.0,layer_depth * i),rotation=(0.0,0.0,0.0))
        
        # create new material
        mat = bpy.data.materials.new(name=id) #TODO change name of material so only take text before .dcm
        mat.use_nodes = True

        # add texture to material
        node_tree = bpy.data.materials[id].node_tree
        node = node_tree.nodes.new("ShaderNodeTexImage")

        # read the dicom image, generate a png of it
        png_path = read_dicom_image( os.path.join(path,id))
        segmented_img_path = process_image(png_path)

        # load into blender
        bpy.data.images.load(segmented_img_path, check_existing=True)

        # use png as image texture
        segmented_img = bpy.data.images[os.path.split(png_path)[1]]
        node.image = segmented_img

        # # set texture to active
        node.select = True
        node_tree.nodes.active = node
        nodes = mat.node_tree.nodes

        # set up node hierarch
        BSDF_node = node_tree.nodes['Principled BSDF']
        nodes.remove(BSDF_node)
        
        texture_node = nodes['Image Texture']

        transparent_node = nodes.new('ShaderNodeBsdfTransparent')
        diffuse_node = nodes.new('ShaderNodeBsdfDiffuse')
        mix_node = nodes.new('ShaderNodeMixShader')
        output_node = mat.node_tree.nodes['Material Output']

        node_tree.links.new(texture_node.outputs['Color'],diffuse_node.inputs['Color'])
        mat.node_tree.links.new(texture_node.outputs['Alpha'],mix_node.inputs['Fac'])
        mat.node_tree.links.new(transparent_node.outputs['BSDF'],mix_node.inputs[1])
        mat.node_tree.links.new(diffuse_node.outputs['BSDF'],mix_node.inputs[2])
        mat.node_tree.links.new(mix_node.outputs['Shader'],output_node.inputs['Surface'])

        mat.blend_method = 'BLEND'
        mat.shadow_method = 'CLIP'


        obj = bpy.context.selected_objects[0]

        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

if __name__ == "__main__":
    main()

# for blender eevvee bpy.ops.texture.new()
# bpy.ops.image.open(filepath="C:\\temp\\test (1).png", directory="C:\\temp\\", files=[{"name":"test (1).png", "name":"test (1).png"}], relative_path=True, show_multiview=False)
# bpy.data.textures["TestTexture1"].name = "TestTexture1"
