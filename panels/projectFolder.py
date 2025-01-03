import bpy
from bpy.types import Panel, Operator


class VIEW3D_PT_ProjectFolder(Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Set Houdini Project folder"
    bl_idname = "RFXUTILS_PT_project_folder"
    bl_space_type = 'VIEW_3D'     
    bl_region_type = 'UI'         
    bl_category = "RuneFX Utils" 

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.label(text="Set Houdini Project folder")
        row = layout.row()
        row.prop(scene, "custom_folder_path", text="Folder Path", icon='FILE_FOLDER')
        
        row = layout.row()
        row.operator("rfxutils.auto_detect_folder", text="Auto Detect")

def register():
    bpy.utils.register_class(VIEW3D_PT_ProjectFolder)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_ProjectFolder)


