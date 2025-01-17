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


        #right now as it stands in this current version of meddle the eye shadow material is broken, giving white eye shadows.
        #to fix it we simply disconnect the base color from the principled shader and set it to black.
        for object in selectedObjects:
            if object.type == "MESH":
                for mat in object.data.materials:
                    if mat.name == "eye_shadow_mat":
                        for node in mat.node_tree.nodes:
                            if node.bl_idname == "ShaderNodeBsdfPrincipled":
                                for input in node.inputs:
                                    if input.name == "Base Color":
                                        for link in input.links:
                                            mat.node_tree.links.remove(link)
                                            node.inputs["Base Color"].default_value = (0, 0, 0, 1)
                                            rgbNode = mat.node_tree.nodes.new(type="ShaderNodeRGB")
                                            mat.node_tree.links.new(node.inputs["Base Color"], rgbNode.outputs[0])
                                            mat.node_tree.nodes[-1].outputs[0].default_value = (0, 0, 0, 1)


                                      
        return {"FINISHED"}


def register():
    bpy.utils.register_class(RFX_OT_Fix_Eye_Shadow)

def unregister():
    bpy.utils.register_class(RFX_OT_Fix_Eye_Shadow)
