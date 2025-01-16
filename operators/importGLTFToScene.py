import bpy # type: ignore

class RFX_OT_ImportGLTF(bpy.types.Operator):
    bl_idname = "rfxutils.import_gltf_operator"
    bl_label = "Import GLTF scene"
    bl_description = "Import GLTF scene" 
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selectedObjects = bpy.context.selected_objects

        parsedMaterials = []
        for object in selectedObjects:
            if object.type == "MESH":
                pass

                                      
        return {"FINISHED"}


def register():
    bpy.utils.register_class(RFX_OT_ImportGLTF)

def unregister():
    bpy.utils.register_class(RFX_OT_ImportGLTF)
