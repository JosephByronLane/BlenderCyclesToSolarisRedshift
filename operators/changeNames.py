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
            "fac": "face",
            "w": "weapon",
            "til": "tail",
            "e000_top": "bra",
            "e000_dwn": "panties",
        }
        
        parsedMaterials = []
        for object in selectedObjects:
            if object.type == "MESH":
                meshFullName = object.name

                #gear might be as in c0801h0148_hir_0_mt_c0201h0148_hir_a_hair_5FB0AC65.0;atr_top
                #so we split by _'s, and then we take the 3rd to the 8th element
                #leaving us with hir_0_mt_c0201h0148_hir_a_hair
                #which wont contain doubles of another class, for example the example above contains _top in it.
                wasNameChanged = False
                meshPrunedName = meshFullName.split("_")[3:8]
                for key in mapRenaming:
                    if key in meshPrunedName:
                        toNameMesh = f"{mapRenaming[key]}_geo"
                        object.name = toNameMesh
                        wasNameChanged = True

                #we cant quite rename the tail programaticaly since it has a different name in the exported files
                #so if a mesh isn't renamed, we can assme its the tail
                if not wasNameChanged:
                    toNameMesh = "tail_geo"
                    object.name = toNameMesh    

                wasNameChanged = False

                #then we rename the materials aswell
                materials = object.data.materials
                for mat in  materials:
                    if mat.name not in parsedMaterials:
                        matName = mat.name
                        matPrunedName = matName.split("_")[2:4]
                        if "w" in matPrunedName[0]:
                            mat.name = "weapon_mat"

                        manRejoinedName = "_".join(matPrunedName)
                        for key in mapRenaming:
                            if key in manRejoinedName:
                                toNameMat = f"{mapRenaming[key]}_mat"
                                mat.name = toNameMat
                                wasNameChanged = True
                                #edge cases, my favorite
                                if mat.name == "body_mat.001":
                                    mat.name = "neck_mat CHECK IF I NEED DELETING"
                                elif mat.name == "brows_mat.001":
                                    mat.name = "eye_shadow_mat"
                        if not wasNameChanged:
                            toNameMat = "tail_mat"
                            mat.name = toNameMat
                        parsedMaterials.append(mat.name)
                
                
        return {"FINISHED"}


                
def register():
    bpy.utils.register_class(RFX_OT_ChangeMeshNames)

def unregister():
    bpy.utils.register_class(RFX_OT_ChangeMeshNames)
