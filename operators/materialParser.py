import bpy
from ..nodes import nodeRegistry 
from ..nodes.nodeRegistry import getRegistry
from ..data.tempStorage import GLOBAL_DATA_STORE
import uuid
from ..utils.uniqueDict import resetNodeNames 
class RFXUTILS_OT_MaterialParser(bpy.types.Operator):
    """Export the active material's node tree to IR JSON."""
    bl_idname = "rfxutils.material_parser"
    bl_label = "Export Selected Material"

    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Where to save the IR JSON file",
        default="my_material.json",
        subtype='FILE_PATH'
    )


    def clearErrorsFromCustomList(self):
        scn = bpy.context.scene
        scn.custom.clear()
        scn.custom_index = 0

    def addErrorsToCustomList(self, errorString, material):
        """Adds each string in `errors` as a new item to the custom list."""
        scn = bpy.context.scene
        new_item = scn.custom.add()
        new_item.mat = material
        new_item.name = errorString
        new_item.coll_id = len(scn.custom)  # or some other logic for coll_id
        scn.custom_index = len(scn.custom) - 1  # Make sure the last one is selected

    def execute(self, context):
        print("execuring material parser")
        selectedObjects = context.selected_objects
        if not selectedObjects:
            self.report({'ERROR'}, "No objects selected.")
            return {'CANCELLED'}

        uniqueId = ""
        allErrors = []
        parsedNodes = []
        #used to verify if a material has already been exported
        alreadyExportedMmaterials = set()

        for obj in selectedObjects:

            if obj.type != 'MESH':
                continue
            for mat in obj.data.materials:
                resetNodeNames()
                if mat and mat.use_nodes and mat.name not in alreadyExportedMmaterials:
                    alreadyExportedMmaterials.add(mat.name)
        
                    RSIRGraphs= []
                    self.clearErrorsFromCustomList()
                    errors = []

                    #TODO: rewrite error handling cause its really finnicky and not very good
                    #  nodes
                    for node in mat.node_tree.nodes:
                        errors = []

                        nodeRegistry = getRegistry(node.bl_idname)
                        if nodeRegistry:
                            #errors is  passed by reference
                            misc = []
                            nodeFunction = nodeRegistry(node, errors)

                            print("Parsing node", node.bl_idname)

                            RSIRGraphs.append(nodeFunction) 
                            
                            if errors:           
                                for error in errors:
                                    allErrors.append(error)
                                    print(f"Found error in node {node.name}: {error}")
                                    self.addErrorsToCustomList(error, mat.name)        

                                continue
                            print(f"Node {node.name} parsed successfully")
                            parsedNodes.append(node.name)
                            uniqueId = mat.name  #uuid because why not lmao       
                            GLOBAL_DATA_STORE[uniqueId] = {
                                "mat": mat,
                                "RSIRGraphs": RSIRGraphs,
                            }

                        else:
                            error = f"Node {node.bl_idname} not supported "
                            self.addErrorsToCustomList(error, mat.name)  
                            allErrors.append(error)
                            continue

                    # now we fil out the inputConnections field
                    for node in mat.node_tree.nodes:                        
                        if node.name in parsedNodes:
                            print("Parsing connections for node", node.name)
                            #since RSIRGraphs is a list of  custom objects and not data, we cant just use the .index() function, we need to manually search it
                            currentNodeRSIRGraph = None
                            for rsirGraph in RSIRGraphs:
                                if rsirGraph.uId == node.name:
                                    currentNodeRSIRGraph = rsirGraph
                                    break
                                    
                            if currentNodeRSIRGraph is None:
                                self.report({'ERROR'}, "There was an error hooking up node conections: Couldnt find current node's RSIRGraph")
                                return {'CANCELLED'}

                            
                            for input_socket in node.inputs:
                                if input_socket.is_linked:
                                    try:
                                        # These are in RS nodes, since they're pased to the houdini parser.
                                        # 
                                        # To find these connectors, its going to query the blender node and ask:
                                        # "Hey, I see you are connected to my ShaderNodeMix input A through your Texture1 color output,
                                        # My actual ShaderNodeMix input A is actually inboundConnectors["ShaderNodeMix:A"] (RScolorMix1:input1), 
                                        # and I see your Texture1 color output is actually inputNode.outboundConnectors["Texture1:Color"] (RSColorMaker1:outColor)
                                        # and so it writes them for the parser.
                                        #
                                        # "RSMathRange1:input" : "RSColorSplitter1:outA",

                                        connectingNode = input_socket.links[0].from_node     

                                        connectingNodeRSIRGraph = None
                                        for rsirGraph in RSIRGraphs:
                                            if rsirGraph.uId == connectingNode.name:
                                                if rsirGraph.uId in parsedNodes:
                                                    connectingNodeRSIRGraph = rsirGraph
                                                    break

                                        #if the RSIRGraph is not found, in the connecting inputs, means its graph was never greated, and thus never parsed. AKA isn't supported
                                        if connectingNodeRSIRGraph is None:

                                            #these errors can be ignored, as they are already reported in the node parsing stage

                                            # self.addErrorsToCustomList(f"Unsuported node {connectingNode.name} found. Will be ignored", mat.name)  
                                            # allErrors.append(f"Unsuported node {connectingNode.name} found. Will be ignored")
                                            continue


                                        connectingGraphOutboundConnectors = connectingNodeRSIRGraph.outboundConnectors                                    
                                        
                                        #we get the connectors to do the  blender -> redshift name translation
                                        currentGraphInboundConnectors = currentNodeRSIRGraph.inboundConnectors
                                        currentGraphInputConnections = currentNodeRSIRGraph.inputConnections

                                        currentNodeBlId = node.bl_idname
                                        currentNodeConnectedSocketName = input_socket.name

                                        currentNodeRedshiftTranslatedSocket = currentGraphInboundConnectors.get(f"{currentNodeBlId}:{currentNodeConnectedSocketName}")
                                        
                                        connectingNodeBlId = connectingNode.bl_idname
                                        inputNodeSocketName = input_socket.links[0].from_socket.name
                                        inputNodeRedshiftTranslatedSocket = connectingGraphOutboundConnectors.get(f"{connectingNodeBlId}:{inputNodeSocketName}")

                                        if currentNodeRedshiftTranslatedSocket is None or inputNodeRedshiftTranslatedSocket is None:
                                            error = f"Error hooking up node connections: Couldnt find redshift translated socket for {currentNodeBlId}"
                                            self.addErrorsToCustomList(error, mat.name)  
                                            allErrors.append(error)
                                        else:
                                            currentGraphInputConnections[inputNodeRedshiftTranslatedSocket] = f"{currentNodeRedshiftTranslatedSocket}"
                                        continue
                                    except Exception as e:
                                        self.report({'ERROR'}, f"Error hooking up node connections: {e}")
                                        return {'CANCELLED'}

                    if allErrors:
                        print("Errors found")
                        bpy.ops.rfxutils.call_popup('INVOKE_DEFAULT', key=uniqueId)

                    else:
                        print("No errors found")
                        bpy.ops.rfxutils.json_saver('INVOKE_DEFAULT', key=uniqueId)

        return {'FINISHED'}
    

def register():
    bpy.utils.register_class(RFXUTILS_OT_MaterialParser)

def unregister():
    bpy.utils.unregister_class(RFXUTILS_OT_MaterialParser)