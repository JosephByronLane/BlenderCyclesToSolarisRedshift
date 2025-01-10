import bpy  # type: ignore
from bpy.props import StringProperty  # type: ignore
from bpy_extras.io_utils import ImportHelper  # type: ignore

class RFXUTILS_OT_SelectFolder(bpy.types.Operator, ImportHelper):
    """Select a folder using Blender's file browser"""
    bl_idname = "rfxutils.select_folder"
    bl_label = "Select Folder"
    bl_options = {'REGISTER', 'UNDO'}
    
    filename = StringProperty(subtype='FILE_PATH')
    
    filter_folder = True  
    
    def execute(self, context):
        folder_path = self.filepath
        context.scene.custom_folder_path = folder_path
        self.report({'INFO'}, f"Selected folder: {folder_path}")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def register():
    bpy.utils.register_class(RFXUTILS_OT_SelectFolder)

def unregister():
    bpy.utils.register_class(RFXUTILS_OT_SelectFolder)

