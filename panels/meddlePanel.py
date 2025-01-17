import bpy # type: ignore
from bpy.types import Panel, Operator # type: ignore


class VIEW3D_PT_MeddleReminderPanel(Panel):
    """TODO: add description"""
    bl_label = "Go apply meddle materials"
    bl_idname = "RFXUTILS_PT_meddle_reminder_panel"
    bl_space_type = 'VIEW_3D'     
    bl_region_type = 'UI'         
    bl_category = "RuneFX Utils" 

    def draw(self, context):
        layout = self.layout
        layout.label(text="Go apply Meddle materials")


def register():
    bpy.utils.register_class(VIEW3D_PT_MeddleReminderPanel)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_MeddleReminderPanel)
