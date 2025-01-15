import bpy # type: ignore

class VIEW3D_PT_cleanUpNodeGraph(bpy.types.Panel):
    """Cleans up the selected object's node graph to be properly exported"""
    bl_label = "Node Graph Cleanup"
    bl_idname = "RFXUTILS_PT_nodegraphcleaner"
    bl_space_type = 'VIEW_3D'     
    bl_region_type = 'UI'         
    bl_category = "RuneFX Utils" 

    def draw(self, context):
        layout = self.layout
        layout.label(text="Cleanup and export and shit")

        layout.operator("rfxutils.ungroup_scene_modal", text="Remove Group Nodes")
        layout.operator("rfxutils.child_remover", text="Remove Orphaned Nodes")

def register():
    bpy.utils.register_class(VIEW3D_PT_cleanUpNodeGraph)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_cleanUpNodeGraph)
