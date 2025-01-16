import bpy # type: ignore

class RFX_OT_ChangeMeshNames(bpy.types.Operator):
    bl_idname = "rfxutils.change_mesh_names"
    bl_label = "Change mesh names"
    bl_description = "Change mesh names to conform to the RuneFX Pipeline nomenclature" 
    bl_options = {"REGISTER"}

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
    bpy.utils.register_class(RFX_OT_ChangeMeshNames)

def unregister():
    bpy.utils.register_class(RFX_OT_ChangeMeshNames)
