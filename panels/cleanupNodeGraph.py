import bpy # type: ignore

class VIEW3D_PT_cleanUpNodeGraph(bpy.types.Panel):
    """Cleans up the selected object's node graph to be properly exported"""
    bl_label = "Node Graph Cleanup"
    bl_idname = "RFXUTILS_PT_panel"
    bl_space_type = 'VIEW_3D'     
    bl_region_type = 'UI'         
    bl_category = "RuneFX Utils" 

    def draw(self, context):
        layout = self.layout
        