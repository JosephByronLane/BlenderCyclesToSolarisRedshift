import bpy # type: ignore
from bpy.types import Panel, Operator # type: ignore


class VIEW3D_PT_ImportGLTFPanel(Panel):
    """TODO: add description"""
    bl_label = "Import GLTF Character"
    bl_idname = "RFXUTILS_PT_importgltf_panel"
    bl_space_type = 'VIEW_3D'     
    bl_region_type = 'UI'         
    bl_category = "RuneFX Utils" 

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene , "auto_detect_gltf", text="Auto Detect GLTF location")
        layout.prop(context.scene , "separate_col_gear_gltf", text="Separate collider and gear GLTF")

        layout.operator( "rfxutils.import_gltf_operator", text="Import GLTF")
        layout.separator()

        layout.prop(context.scene , "only_merge_skin", text="Only skin meshes")
        layout.operator( "rfxutils.merge_meshes", text="Merge Meshes")

        layout.separator()
        layout.operator( "rfxutils.change_mesh_names", text="Rename Meshes and materials")

def register():
    bpy.utils.register_class(VIEW3D_PT_ImportGLTFPanel)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_ImportGLTFPanel)
