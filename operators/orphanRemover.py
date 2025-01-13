import bpy # type: ignore

class RFX_OT_OrphanRemover(bpy.types.Operator):
    bl_idname = "rfxutils.orphan_remover"
    bl_label = "Orphan Node Remover"
    bl_description = "Removes orphaned nodes (nodes that are not connected to any other node) from selected objects' shader graph."
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        return {"FINISHED"}


def register():
    bpy.utils.register_class(__name__)

def unregister():
    bpy.utils.register_class(__name__)
