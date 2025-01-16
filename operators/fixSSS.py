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
                                #we dont want to half it  f its already 0.05, since 0.025 would be quite  phisically accurate (if a little high)
                                if node.inputs["Subsurface Scale"].default_value > 0.05:
                                    node.inputs["Subsurface Scale"].default_value = node.inputs["Subsurface Scale"].default_value * .1

                                if node.inputs["Subsurface Scale"].is_linked:

                                    inputShaderNodeMath = node.inputs["Subsurface Scale"].links[0].from_node

                                    isConnectingNodeShaderMath = inputShaderNodeMath.bl_idname == "ShaderNodeMath" 
                                    
                                    if isConnectingNodeShaderMath and inputShaderNodeMath.operation == "MULTIPLY" and inputShaderNodeMath.inputs[1].default_value <= .11:
                                        self.report({'INFO'}, "SSS doesn't need fixing.")
                                    else:
                                        multiplyNode = nodeTree.nodes.new(type="ShaderNodeMath")
                                        multiplyNode.operation = "MULTIPLY"
                                        multiplyNode.inputs[1].default_value = .1

                                        originalInput = node.inputs["Subsurface Scale"].links[0].from_socket
                                        nodeTree.links.new(multiplyNode.outputs[0], node.inputs["Subsurface Scale"])
                                        nodeTree.links.new(originalInput, multiplyNode.inputs[0])
                                        self.report({'INFO'}, "SSS Scale successfully fixed.")
                                parsedMaterials.append(mat.name)
        return {"FINISHED"}
                                


def register():
    bpy.utils.register_class(RFX_OT_FixSss)

def unregister():
    bpy.utils.register_class(RFX_OT_FixSss)
