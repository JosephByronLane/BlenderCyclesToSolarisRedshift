import bpy
from ..nodes import nodeRegistry 
from ..nodes.nodeRegistry import getRegistry
from ..data.tempStorage import GLOBAL_DATA_STORE
import uuid
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

    def addErrorsToCustomList(self, errors, misc):
        """Adds each string in `errors` as a new item to the custom list."""
        scn = bpy.context.scene
        for err, mat in zip(errors, misc):
            new_item = scn.custom.add()
            new_item.mat = mat
            new_item.name = err
            new_item.coll_id = len(scn.custom)  # or some other logic for coll_id
        scn.custom_index = len(scn.custom) - 1  # Make sure the last one is selected

    def execute(self, context):
        print("execuring material parser")
        selectedObjects = context.selected_objects
        if not selectedObjects:
            self.report({'ERROR'}, "No objects selected.")
            return {'CANCELLED'}

        uniqueId = ""


        #used to verify if a material has already been exported
        alreadyExportedMmaterials = set()

        for obj in selectedObjects:
            if obj.type != 'MESH':
                continue
            for mat in obj.data.materials:
                if mat and mat.use_nodes and mat.name not in alreadyExportedMmaterials:
                    alreadyExportedMmaterials.add(mat.name)
        
                    RSIRGraphs= []
                    self.clearErrorsFromCustomList()
                    errors = []
                    nodesToParse = mat.node_tree.nodes
                    
                    #  nodes
                    for node in mat.node_tree.nodes:
                        totalErrors = []
                        errors = []

                        nodeRegistry = getRegistry(node.bl_idname)
                        if nodeRegistry:
                            #errors is  passed by reference
                            misc = []
                            nodeFunction = nodeRegistry(node, errors)

                            print("Parsing node", node.bl_idname)

                            RSIRGraphs.append(nodeFunction) 
                            
                            if errors:           
                                print("Errors founaaaaad")
                                for _ in errors:
                                    print("Iterating over error")
                                    misc.append(mat.name)     

                                print("Errors found within material", mat.name)
                                print(errors)
                                print(f"total errors before extended", totalErrors)
                                totalErrors.extend(errors)

                                print(f"total errors after extended", totalErrors)

                                self.addErrorsToCustomList(totalErrors, misc)                         
                                continue

                            uniqueId = mat.name  #uuid because why not lmao       
                            GLOBAL_DATA_STORE[uniqueId] = {
                                "mat": mat,
                                "RSIRGraphs": RSIRGraphs,
                            }

                        else:
                            totalErrors = []
                            totalErrors.extend([f"Node {node.bl_idname} not supported "])
                            misc.append(mat.name)

                            self.addErrorsToCustomList(totalErrors, misc)                         

                            print("errors found with not supported node")
                            print("total errors before extended", totalErrors)
                            print(totalErrors)
                            print("total errors after extended", totalErrors)

                            print(misc)
                            continue

                    if totalErrors:
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