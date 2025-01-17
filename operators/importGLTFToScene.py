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
        
        autoDetectGLTF = context.scene.auto_detect_gltf



        if autoDetectGLTF:
            #gets the GLTF from the custom folder path
            houdiniProjectPath = context.scene.custom_folder_path
            if houdiniProjectPath == "":
                self.report({'ERROR'}, "No folder selected.  Pleasethe  Houdini Project or try to auto-detect it.")
                return {"CANCELLED"}

            #gets the GLTF file from houdini path + /gltf/ + the first gltf file in the folder
            gltfPath = houdiniProjectPath + "/gltf/"

            if not os.path.exists(gltfPath):
                self.report({'ERROR'}, "No GLTF folder found in the Houdini Project folder.")
                return {"CANCELLED"}
            
            gltfFiles = [f for f in os.listdir(gltfPath) if f.endswith(".gltf")]
         
            if len(gltfFiles) == 0:
                self.report({'ERROR'}, "No GLTF files found in the Houdini Project folder.")
                return {"CANCELLED"}

            gltfFile = gltfFiles[0]

            #using blenders build in GLTF importer with the gltfFile
            bpy.ops.import_scene.gltf(filepath=gltfPath + gltfFile)
        
        else:
            #if we dont want to auto detect, we can open a file browser and use that tp set the gltf file
            try:
                bpy.ops.import_scene.gltf(filepath=self.filepath)
                self.report({'INFO'}, f"Imported: {self.filepath}")
            except Exception as e:
                self.report({'ERROR'}, str(e))
            return {'FINISHED'}

        return {"FINISHED"}

    def invoke(self, context, event):
        autoDetectGLTF = context.scene.auto_detect_gltf
        if autoDetectGLTF:
            return self.execute(context)
        context.window_manager.fileselect_add(self)
        self.filepath = ""  #ensure its a string
        return {'RUNNING_MODAL'}
    

def register():
    bpy.utils.register_class(RFX_OT_ImportGLTF)

def unregister():
    bpy.utils.register_class(RFX_OT_ImportGLTF)
