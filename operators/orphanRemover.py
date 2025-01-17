import bpy # type: ignore

class RFX_OT_OrphanRemover(bpy.types.Operator):
    bl_idname = "rfxutils.child_remover"
    bl_label = "Orphan Node Remover"
    bl_description = "Removes orphaned nodes (nodes that are not connected to any other node) from selected objects' shader graph."
    bl_options = {"REGISTER", "UNDO"}

    def parse_node(self, node, parsedNodes):
        
        #if the node has already been parsed, we return because we dont want to parse it again
        if node.name in parsedNodes:            
            return
        print("Parsing node: ", node.name)
        parsedNodes.append(node.name)        

        #we go over each input
        for input in node.inputs:
            #check if its linked
            if input.is_linked:

                #if it is, we go over each link
                for link in input.links:
                    #we call the function again with the node that is connected to the input
                    self.parse_node(link.from_node, parsedNodes)

    def execute(self, context):
        selectedObjects = bpy.context.selected_objects

        parsedMaterials = []
        for object in selectedObjects:
            if object.type == "MESH":
                for mat in object.data.materials:
                    parsedNodes= []
                    print("-----------------------------------------------------------")
                    print("Parsing material: ", mat.name)
                    print("-----------------------------------------------------------")

                    if mat and mat.name not in parsedMaterials:
                        parsedMaterials.append(mat.name)

                        for node in mat.node_tree.nodes:
                            #if the node is the output node, we call the parse_node function with it
                            if node.bl_idname == "ShaderNodeOutputMaterial" and node.inputs["Surface"].is_linked:                                    
                                print("Found materlai output!")
                                materialOutput = node
                                break
                                #we call a recursive function to check each node of the node [0] which is the output material node
                                #i wasn't sure how to check all nodes whose outputs are not connected to anything, so i just check the first node
                                #and go from there, saving all nodes in the pasedNodes list and removing those that dont appear.
                        if materialOutput == None:
                            print("Node is not output material")
                            return {"FINISHED"}
                        

                        self.parse_node(node, parsedNodes) 

                        #if a node isn't in the parsed nodes
                        #aka its output doesn't affect the final material, we nuke it to oblivion
                        for node in mat.node_tree.nodes: 
                            if node.name not in parsedNodes:
                                mat.node_tree.nodes.remove(node)


                         
        return {"FINISHED"}


def register():
    bpy.utils.register_class(RFX_OT_OrphanRemover)

def unregister():
    bpy.utils.register_class(RFX_OT_OrphanRemover)
