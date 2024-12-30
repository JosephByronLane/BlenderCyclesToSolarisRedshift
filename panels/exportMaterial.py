import bpy
from bpy.types import Panel, Operator


class VIEW3D_PT_MaterialExporter(Panel):
    """TODO: add description"""
    bl_label = "RuneFX Utils"
    bl_idname = "RFXUTILS_PT_panel"
    bl_space_type = 'VIEW_3D'     
    bl_region_type = 'UI'         
    bl_category = "RuneFX Utils" 

    def draw(self, context):
        layout = self.layout

        layout.label(text="omg asdfasdf please appear.")

        layout.operator("rfxutils.material_parser", text="test")

def register():
    bpy.utils.register_class(VIEW3D_PT_MaterialExporter)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_MaterialExporter)
