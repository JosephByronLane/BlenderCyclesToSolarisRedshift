import bpy # type: ignore
from bpy.types import Panel, Operator # type: ignore


class VIEW3D_PT_MeshCleanup(Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Mesh Clean up"
    bl_idname = "RFXUTILS_PT_mesh_cleanup"
    bl_space_type = 'VIEW_3D'     
    bl_region_type = 'UI'         
    bl_category = "RuneFX Utils" 

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.label(text="Clean up meshes")

        layout.prop(context.scene , "only_merge_skin", text="Only skin meshes")
        layout.prop(context.scene , "keep_smallclothes_separate", text="Keep smallclothes separate")

        layout.operator( "rfxutils.merge_meshes", text="Merge Meshes")

        layout.separator()
        layout.operator( "rfxutils.change_mesh_names", text="Rename Meshes and materials")

        

def register():
    bpy.utils.register_class(VIEW3D_PT_MeshCleanup)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_MeshCleanup)


