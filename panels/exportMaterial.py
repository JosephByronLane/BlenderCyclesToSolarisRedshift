import bpy
from bpy.types import Panel, Operator


class VIEW3D_PT_MaterialExporter(Panel):
    """TODO: add description"""
    bl_label = "Material Parser"
    bl_idname = "RFXUTILS_PT_panel"
    bl_space_type = 'VIEW_3D'     
    bl_region_type = 'UI'         
    bl_category = "RuneFX Utils" 

    def draw(self, context):
        layout = self.layout


        layout.operator("rfxutils.material_parser", text="Export Materials")

def register():
    bpy.utils.register_class(VIEW3D_PT_MaterialExporter)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_MaterialExporter)
