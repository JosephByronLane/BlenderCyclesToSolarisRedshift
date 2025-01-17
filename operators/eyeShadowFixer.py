import bpy # type: ignore

class RFX_OT_Fix_Eye_Shadow(bpy.types.Operator):
    bl_idname = "rfxutils.fix_eye_shadow"
    bl_label = "Fix eye Shadow"
    bl_description = "Fixes the eye shadow being white."
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selectedObjects = bpy.context.selected_objects

        for object in selectedObjects:
            if object.type == "MESH":
                for mat in object.data.materials:
                    if mat.name == "eye_shadow_mat":
                        pass


                                      
        return {"FINISHED"}


def register():
    bpy.utils.register_class(RFX_OT_Fix_Eye_Shadow)

def unregister():
    bpy.utils.register_class(RFX_OT_Fix_Eye_Shadow)
