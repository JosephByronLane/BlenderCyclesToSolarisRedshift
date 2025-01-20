import bpy # type: ignore
from bpy.types import Panel, Operator # type: ignore


class VIEW3D_PT_ApplyMekRig(Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Apply Mektools Rig"
    bl_idname = "RFXUTILS_PT_apply_mektools_rigs"
    bl_space_type = 'VIEW_3D'     
    bl_region_type = 'UI'         
    bl_category = "RuneFX Utils" 

    def draw(self, context):
        layout = self.layout
        layout.label(text="MekTools is required for this panel to work.")

        layout.operator("wm.url_open", text="Support them on Patreon!", icon="URL").url = "https://www.patreon.com/MekuuMaki"
        layout.operator("wm.url_open", text="Join their Discord! (18+ only)", icon="URL").url = "https://www.discord.gg/98DqcKE"
        
        layout.separator()
        layout.label(text="Rigs")
        split = layout.split(factor=0.5, align=True)
        split.popover("MEKTOOLS_PT_MaleRigs", text="Male", icon_value=0)
        split.popover("MEKTOOLS_PT_FemaleRigs", text="Female", icon_value=0)

def register():
    bpy.utils.register_class(VIEW3D_PT_ApplyMekRig)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_ApplyMekRig)


