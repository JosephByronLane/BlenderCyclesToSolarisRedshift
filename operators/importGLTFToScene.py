import bpy # type: ignore
import os
class RFX_OT_ImportGLTF(bpy.types.Operator):
    bl_idname = "rfxutils.import_gltf_operator"
    bl_label = "Import GLTF scene"
    bl_description = "Import GLTF scene" 
    bl_options = {"REGISTER", "UNDO"}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    
    filter_glob: bpy.props.StringProperty(default="*.gltf;*.glb", options={'HIDDEN'}) # type: ignore

    def execute(self, context):
        
        separateBodyAndGear = context.scene.separate_col_gear_gltf
        meddlePath = context.scene.meddle_export_folder
        selectedCharacter = context.scene.character_name
        characterOutfitName = context.scene.character_outfit
        characterBodyName = context.scene.body_type

        
        if meddlePath == "":
            self.report({'ERROR'}, "No Meddle folder selected.")
            return {"CANCELLED"}

        #gets the GLTF directory
        gearGltfPath = os.path.join(meddlePath + (f"gear_{selectedCharacter}_{characterOutfitName}_raw"))
        bodyGltfPath = os.path.join(meddlePath + (f"character_{selectedCharacter}_{characterBodyName}_raw"))

        print("Gear GLTF path: ", gearGltfPath)
        print("Body GLTF path: ", bodyGltfPath)

        if not os.path.exists(gearGltfPath):
            self.report({'ERROR'}, "No gear GLTF directory found.")
            return {"CANCELLED"}
        
        if not os.path.exists(bodyGltfPath):
            self.report({'ERROR'}, "No character GLTF directory found.")
            return {"CANCELLED"}
                    
        gearGltfFile = os.path.join(gearGltfPath, "character.gltf")
        bodyGltfFile = os.path.join(bodyGltfPath, "character.gltf")

        print("Gear GLTF file: ", gearGltfFile)
        print("Body GLTF file: ", bodyGltfFile)

        if not os.path.exists(gearGltfFile):
            self.report({'ERROR'}, "No gear GLTF file found.")
            return {"CANCELLED"}
        
        if not os.path.exists(bodyGltfFile):
            self.report({'ERROR'}, "No body GLTF file found.")
            return {"CANCELLED"}

        if separateBodyAndGear:
            
            #since we cant assign imported files to a file and iterate over them
            #what we do instead is take note of all of the existing meshes before the import, import the mesh then compare which ones are new
            #to determine which ones are the imported meshes
            existingObjects = set(bpy.context.scene.objects)

            bpy.ops.import_scene.gltf(filepath=gearGltfFile)

            importedMeshes = [obj for obj in bpy.context.scene.objects if obj not in existingObjects]

            #once imported we check which meshes contain character information and we delete them
            #we need to delete them since we're importing the gear and body separately
            bodyPartKeywords  = ["skin", "hair", "etc", "iri", "bibo"]

            for mesh in importedMeshes:
                if mesh.type == 'MESH':  
                    for keyword in bodyPartKeywords:
                        if keyword in mesh.name:
                            bpy.data.objects.remove(mesh)
                            break


            #since we still need to set the armature to 'rest position' well do a hacky thing rather than keeping and reorganizing what meshes we got
            #after we import it, the last imported mesh (in this case the body) will be the active object
            #so we can iterate over every selected object and if its an armature we set it to rest pose
            for obj in bpy.context.selected_objects:
                if obj.type == 'ARMATURE':
                    obj.name = f"gear_{selectedCharacter}_{characterOutfitName}_armature"
                    obj.data.pose_position = 'REST'
                    break


            #next we import the body
            #we dont need to determine what objects were imported since we generally want to keep the whole body itself
            bpy.ops.import_scene.gltf(filepath=bodyGltfFile)
            for obj in bpy.context.selected_objects:
                if obj.type == 'ARMATURE':
                    obj.name = f"character_{selectedCharacter}_{characterBodyName}_armature"
                    obj.data.pose_position = 'REST'
                    break

            self.report({'INFO'}, f"Imported: {gearGltfFile} and {bodyGltfFile}")
            return {'FINISHED'}
        else:
            #if the user is importing a single mesh as the object, there isn't really much preprocessing needed lmao, its mostly just importing it and calling it a day
            #we simply import the gear, keep its body components and thats it. No need to import the body since the gear already has it (though its not the full body)
            bpy.ops.import_scene.gltf(filepath=gearGltfFile)
            self.report({'INFO'}, f"Imported: {gearGltfFile} and {bodyGltfFile}")
            for obj in bpy.context.selected_objects:
                if obj.type == 'ARMATURE':
                    obj.name = f"gear_{selectedCharacter}_{characterOutfitName}_armature"
                    obj.data.pose_position = 'REST'
                    break
            return {'FINISHED'}

def register():
    bpy.utils.register_class(RFX_OT_ImportGLTF)

def unregister():
    bpy.utils.register_class(RFX_OT_ImportGLTF)
