import bpy # type: ignore
from bpy.types import Panel, Operator # type: ignore


class VIEW3D_PT_MaterialExporter(Panel):
    """TODO: add description"""
    bl_label = "Material Parser"
    bl_idname = "RFXUTILS_PT_panel"
    bl_space_type = 'VIEW_3D'     
    bl_region_type = 'UI'         
    bl_category = "RuneFX Utils" 

    def draw(self, context):
        layout = self.layout

        #we split it into a row in order to have more control of the text:enum ratio
        row = layout.split(factor=0.45)
        row.label(text="Render Engine")  # Label occupies one part
        row.prop(context.scene, "render_engine", text="")


        layout.operator("rfxutils.material_parser", text="Export Materials")

def register():
    bpy.utils.register_class(VIEW3D_PT_MaterialExporter)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_MaterialExporter)
