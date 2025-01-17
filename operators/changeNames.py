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

        #c0201e0023_dwn_1_mt_c0201b0001_a_skin_1562867740.0
        
        # we are really only interested in the 1st and 2nd (Starting at 0) if we separate by _'s


        mapRenaming = {
            "rir": "ring",
            "sho": "feet",
        }

        bodyStrings = ["skin", "bra","panties"]
        
        #if they have skin in the name they get merged into "body"

        for object in selectedObjects:
            if object.type == "MESH":
                meshFullName = object.name
                meshNameParts = meshFullName.split("_")
                meshType = meshNameParts[1]
                
                #this returns the index at where "skin" is found in the mesh name
                #realitically i should of used some sort of thing that returns a boolean if its found or not
                #but oh well
                bodyIndex = meshFullName.find("skin")
                if bodyIndex != -1:
                    meshType = "body"

                
        return {"FINISHED"}


def register():
    bpy.utils.register_class(RFX_OT_ChangeMeshNames)

def unregister():
    bpy.utils.register_class(RFX_OT_ChangeMeshNames)
