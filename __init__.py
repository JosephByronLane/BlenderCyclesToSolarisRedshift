bl_info = {
    "name": "RFXUtils",
    "author": "Rune",
    "version": (0, 1),
    "blender": (4, 3, 0), 
    "location": "3D View > Sidebar",
    "description": "Utils for RFX workflow",
    "warning": "",
    "doc_url": "",
    "category": "3D View",
}

import bpy

class MYEXAMPLEADDON_PT_panel(bpy.types.Panel):
    """Creates a Panel in the 3D View's Sidebar (N-Panel)"""
    bl_label = "RuneFX Utils"
    bl_idname = "RFXUTILS_PT_panel"
    bl_space_type = 'VIEW_3D'     
    bl_region_type = 'UI'          
    bl_category = "RuneFX Utils" 

    def draw(self, context):
        layout = self.layout
        layout.label(text="Helasdfasdfasdfasdflo World from My Addon!")
        layout.operator("mesh.primitive_cube_add", text="Add Cube")

def register():
    bpy.utils.register_class(MYEXAMPLEADDON_PT_panel)

def unregister():
    bpy.utils.unregister_class(MYEXAMPLEADDON_PT_panel)

if __name__ == "__main__":
    register()
