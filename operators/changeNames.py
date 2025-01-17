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

        #mappings from their exported names to what their names should be.
        mapRenaming = {
            "skin": "body",
            "hir": "hair",
            "rir": "ring",
            "sho": "feet",
            "nek": "neck",
            "glv": "hands",
            "dwn": "pants",
            "top": "chest",
            "met": "helmet",
            "iri": "iris",
            "etc": "brows",
            "characterocclusion": "eyeShadow",
        }
        

        for object in selectedObjects:
            if object.type == "MESH":
                meshFullName = object.name

                #gear might be as in c0801h0148_hir_0_mt_c0201h0148_hir_a_hair_5FB0AC65.0;atr_top
                #so we split by _'s, and then we take the 3rd to the 8th element
                #leaving us with hir_0_mt_c0201h0148_hir_a_hair
                #which wont contain doubles of another class, for example the example above contains _top in it.

                meshPrunedName = meshFullName.split("_")[3:8]
                for key in mapRenaming:
                    if key in meshPrunedName:
                        toNameMesh = f"{mapRenaming[key]}_geo"
                        object.name = toNameMesh


                
        return {"FINISHED"}


def register():
    bpy.utils.register_class(RFX_OT_ChangeMeshNames)

def unregister():
    bpy.utils.register_class(RFX_OT_ChangeMeshNames)
