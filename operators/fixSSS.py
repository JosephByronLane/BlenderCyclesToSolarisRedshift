import bpy # type: ignore

class RFX_OT_FixSss(bpy.types.Operator):
    bl_idname = "rfxutils.sss_fixer"
    bl_label = "Subsurface Scatter Scale Fixer"
    bl_description = "Multiplies the scale of the SSS by .1 for more phisically accurate shading."
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selectedObjects = bpy.context.selected_objects

        parsedMaterials = []

        for object in selectedObjects:
            if object.type == "MESH":
                for mat in object.data.materials:
                    if mat and mat.name not in parsedMaterials:
                        nodeTree = mat.node_tree
                        for node in nodeTree.nodes:
                            if node.bl_idname == "ShaderNodeBsdfPrincipled":
                                node.inputs["Subsurface"].default_value = node.inputs["Subsurface"].default_value * .1

                                if node.inputs["Subsurface  Scale"].is_linked:
                                    multiplyNode = nodeTree.nodes.new(type="ShaderNodeMath")
                                    



        return {"FINISHED"}


def register():
    bpy.utils.register_class(RFX_OT_FixSss)

def unregister():
    bpy.utils.register_class(RFX_OT_FixSss)
