import bpy # type: ignore
from bpy.types import Panel, Operator # type: ignore


class VIEW3D_PT_MaterialExporterSettings(Panel):
    """TODO: All the settings for the material exporter"""
    bl_label = "Export Settings"
    bl_idname = "RFXUTILS_PT_export_material_settings"
    bl_parent_id = "RFXUTILS_PT_panel"
    bl_space_type = 'VIEW_3D'     
    bl_region_type = 'UI'         
    bl_category = "RuneFX Utils" 

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene , "ignore_invert_nodes", text="Ignore Invert Nodes")
        layout.prop(context.scene , "move_textures_over", text="Move Textures Over")
        layout.prop(context.scene , "include_osl_shaders", text="Allow OSL Shaders")

        row = layout.row()
        row.enabled = context.scene.include_osl_shaders
        row.prop(context.scene , "move_osl_shaders", text="Move OSL Shaders")

def register():
    bpy.utils.register_class(VIEW3D_PT_MaterialExporterSettings)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_MaterialExporterSettings)
