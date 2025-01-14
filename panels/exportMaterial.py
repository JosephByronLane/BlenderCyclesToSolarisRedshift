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

        layout.prop(context.scene , "ignore_invert_nodes", text="Ignore Invert Nodes")
        layout.prop(context.scene , "move_textures_over", text="Move Textures Over")
        layout.prop(context.scene , "include_osl_shaders", text="Move Textures Over")

        layout.operator("rfxutils.material_parser", text="Export Materials")

def register():
    bpy.utils.register_class(VIEW3D_PT_MaterialExporter)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_MaterialExporter)
