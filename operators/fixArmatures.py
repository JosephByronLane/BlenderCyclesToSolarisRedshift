import bpy  # type: ignore
from bpy.props import StringProperty  # type: ignore
from bpy_extras.io_utils import ImportHelper  # type: ignore

class RFXUTILS_OT_FixArmatures(bpy.types.Operator, ImportHelper):
    """Select a folder using Blender's file browser"""
    bl_idname = "rfxutils.fix_armatures"
    bl_label = "Select Folder"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    
    def execute(self, context):
        return {'FINISHED'}
    
  

def register():
    bpy.utils.register_class(RFXUTILS_OT_FixArmatures)

def unregister():
    bpy.utils.register_class(RFXUTILS_OT_FixArmatures)

