import os
import shutil
import bpy  # type: ignore
from bpy.props import StringProperty  # type: ignore
from bpy_extras.io_utils import ImportHelper  # type: ignore

class RFXUTILS_OT_FileMover(bpy.types.Operator, ImportHelper):
    """Moves files between directories"""
    bl_idname = "rfxutils.move_files"
    bl_label = "Moves files"
    bl_options = {'REGISTER', 'UNDO'}
    
    fromPath = StringProperty(subtype='FILE_PATH')
    toPath = StringProperty(subtype='FILE_PATH')

 
    
    def execute(self, context):
        basePath = context.scene.custom_folder_path

        fullToPath = basePath + self.toPath
        shutil.move(self.fromPath, fullToPath)



def register():
    bpy.utils.register_class(RFXUTILS_OT_FileMover)

def unregister():
    bpy.utils.register_class(RFXUTILS_OT_FileMover)




