import bpy # type: ignore

class RFX_OT_ImportGLTF(bpy.types.Operator):
    bl_idname = "rfxutils.import_gltf_operator"
    bl_label = "Import GLTF scene"
    bl_description = "Import GLTF scene" 
    bl_options = {"REGISTER", "UNDO"}


    def execute(self, context):
        
                                      
        return {"FINISHED"}


def register():
    bpy.utils.register_class(RFX_OT_ImportGLTF)

def unregister():
    bpy.utils.register_class(RFX_OT_ImportGLTF)
