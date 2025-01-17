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
                #mesh names are like 
                # c0801f0102_fac_0_mt_c0801f0102_fac_a_skin_nB94ABBFB.4;atr_t.001
                # or
                # c0801f0102_fac_2_mt_c0801f0102_iri_a_iris_n88D124B1.002
                # or 
                # c0201e0000_glv_0_mt_c0201b0001_bibo_skin_n8DF9FD07.005
                
                pass
        return {"FINISHED"}


def register():
    bpy.utils.register_class(RFX_OT_MergeSimilarMeshes)

def unregister():
    bpy.utils.register_class(RFX_OT_MergeSimilarMeshes)
