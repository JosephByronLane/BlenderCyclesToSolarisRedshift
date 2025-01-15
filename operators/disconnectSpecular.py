import bpy # type: ignore

class RFX_OT_DisconnectSpecular(bpy.types.Operator):
    bl_idname = "rfxutils.disconnect_specular"
    bl_label = "Disconnect Specular Nodes (!!!!)"
    bl_description = "Disconnects all specular nodes from the principled BSDF Node."
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
                                for input in node.inputs:
                                    if input.name == "Specular IOR Level" or input.name == "Specular Tint" or input.name == "Anisotropic" or input.name == "Anisotropic Rotation" or input.name == "Tangent":
                                        for link in input.links:
                                            nodeTree.links.remove(link)

                                      
        return {"FINISHED"}


def register():
    bpy.utils.register_class(RFX_OT_DisconnectSpecular)

def unregister():
    bpy.utils.register_class(RFX_OT_DisconnectSpecular)
