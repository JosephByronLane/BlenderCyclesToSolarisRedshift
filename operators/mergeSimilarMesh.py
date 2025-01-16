import bpy # type: ignore

class RFX_OT_MergeSimilarMeshes(bpy.types.Operator):
    bl_idname = "rfxutils.merge_meshes"
    bl_label = "Merge Similar Meshes"
    bl_description = "Merges all similar meshes into a single one.  (All _mat into a single one, all _sho to a single one, etc)" 
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
    bpy.utils.register_class(RFX_OT_MergeSimilarMeshes)

def unregister():
    bpy.utils.register_class(RFX_OT_MergeSimilarMeshes)
