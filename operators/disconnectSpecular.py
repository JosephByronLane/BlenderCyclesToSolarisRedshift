import bpy # type: ignore

class RFX_OT_DisconnectSpecular(bpy.types.Operator):
    bl_idname = "rfxutils.disconnect_specular"
    bl_label = "Disconnect Specular Nodes (!!!!)"
    bl_description = "Disconnects all specular nodes from the principled BSDF Node."
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        return {"FINISHED"}


def register():
    bpy.utils.register_class(RFX_OT_DisconnectSpecular)

def unregister():
    bpy.utils.register_class(RFX_OT_DisconnectSpecular)
