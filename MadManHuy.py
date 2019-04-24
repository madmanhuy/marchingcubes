bl_info = {
        "name": "MadManHuy",
        "category": "Object",
}

import bpy

class ObjectMoveX(bpy.types.Operator):
    bl_idname = "object.madmanhuy"
    bl_label = "MadManHuy"
    bl_options = { 'REGISTER' , 'UNDO' }

    def execute(self,context):
        scene = context.scene
        for obj in scene.objects:
            obj.location.x += 1.0

        # Let Blender know you finished
        # running the operation
        return {'FINISHED'} 

def register():
    bpy.utils.register_class(ObjectMoveX)

def unregister():
    bpy.utils.unregister_class(ObjectMoveX)

# Run script in blender text editor without
# installing the module
if __name__ == "__main__":
    register()
