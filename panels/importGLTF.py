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
        layout.label(text="Set Meddle export folder")

        layout.prop(context.scene, "meddle_export_folder", text="Folder Path", icon='FILE_FOLDER')

        layout.operator("rfxutils.auto_detect_folder", text="Auto Fill")
        layout.separator()
        
        layout.prop(context.scene , "grab_most_recent_meddle_export", text="Use most recent Meddle export")
        layout.prop(context.scene , "separate_col_gear_gltf", text="Separate collider and gear GLTF")

        row = layout.split(factor=0.5)
        row.prop(context.scene, "character_name", text="Name")
        row.prop(context.scene, "body_type", text="Collider")
        layout.prop(context.scene , "character_outfit", text="Outfit")

        layout.operator( "rfxutils.import_gltf_operator", text="Import GLTF")
        layout.separator()

        layout.prop(context.scene , "only_merge_skin", text="Only skin meshes")
        layout.prop(context.scene , "keep_smallclothes_separate", text="Keep smallclothes separate")

        layout.operator( "rfxutils.merge_meshes", text="Merge Meshes")

        layout.separator()
        layout.operator( "rfxutils.change_mesh_names", text="Rename Meshes and materials")

def register():
    bpy.utils.register_class(VIEW3D_PT_ImportGLTFPanel)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_ImportGLTFPanel)
