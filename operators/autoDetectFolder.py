import os, stat
import bpy # type: ignore


class RFX_OT_AutoDetectFolder(bpy.types.Operator):
    """Automatically detect a visible folder in H: drive"""
    bl_idname = "rfxutils.auto_detect_folder"
    bl_label = "Auto Detect Folder"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        h_drive = "H:\\"
        if not os.path.exists(h_drive):
            self.report({'ERROR'}, "H: drive does not exist.")
            return {'CANCELLED'}
        
        try:
            visible_folders = []
            
            for entry in os.listdir(h_drive):
                full_path = os.path.join(h_drive, entry)
                if not self.has_hidden_attribute(full_path) and os.path.isdir(full_path):
                    visible_folders.append(full_path)
            
            if not visible_folders:
                self.report({'WARNING'}, "No visible folders found in H: drive.")
                return {'CANCELLED'}
            
            #select the first folder, since there should one be one ($ACTIVE) 
            selected_folder = visible_folders[0]
            context.scene.custom_folder_path = selected_folder
            self.report({'INFO'}, f"Auto-detected folder: {selected_folder}")
            return {'FINISHED'}
        
        except Exception as e:
            self.report({'ERROR'}, f"Error during auto-detection: {e}")
            return {'CANCELLED'}    
    
    #from https://stackoverflow.com/questions/284115/cross-platform-hidden-file-detection
    def has_hidden_attribute(self, filepath):
        return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
    
def register():
    bpy.utils.register_class(RFX_OT_AutoDetectFolder)

def unregister():
    bpy.utils.unregister_class(RFX_OT_AutoDetectFolder)