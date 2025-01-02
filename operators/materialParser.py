import bpy
import json
from ..structs.irData import IRNode

class RFXUTILS_OT_MaterialParser(bpy.types.Operator):
    """Export the active material's node tree to IR JSON."""
    bl_idname = "rfxutils.material_parser"
    bl_label = "Export Selected Material"

    # Optional: Let the user pick a file path via Blender's file browser
    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Where to save the IR JSON file",
        default="my_material.json",
        subtype='FILE_PATH'
    )

    def execute(self, context):
        print("execuring material parser")
        mat = context.object.active_material
        if not mat or not mat.use_nodes:
            self.report({'ERROR'}, "No active material or no node tree found.")
            return {'CANCELLED'}
        
        node_tree = mat.node_tree
        ir_nodes = []

        blender_node_to_id = {}

        def new_id(base_name):
            new_id.counter += 1
            return f"{base_name}_{new_id.counter}"
        new_id.counter = 0

        #  nodes

        # generic node handler
        for node in node_tree.nodes:
            if node.bl_idname == 'ShaderNodeBsdfPrincipled':

                # "Base Color":         "base_color",
                # "Metallic":           "metalness",  
                # "Roughness":          "refl_roughness",
                # "Diffuse Roughness":  "diffuse_roughness",
                # "Alpha":              "opacity_color",
                # "Normal": "bump_input",
                # "Subsurface Weight": "ms_amount",
                # "Subsurface Radius": "ms_radius",
                # "Subsurface Anisotropy": "ms_phase",
                # "Transmission Weight": "refr_weight",
                # "Coat Weight": "coat_weight",
                # "Coat Roughness": "coat_roughness",
                # "Coat IOR": "coat_ior",
                # "Coat Tint": "coat_color",
                # "Coat Normal": "coat_bump_input",
                # "Sheen Weight": "sheen_weight",
                # "Sheen Roughness": "sheen_roughness",
                # "Sheen Tint": "sheen_color",
                # "Emission Color": "emission_color",
                # "Thin Film Thickness": "thinfilm_thickness",
                # "Thin Film IOR": "thinfilm_ior"     

                ir_node = IRNode(node_id=new_id("PrincipledBSDF"),  node_type="StandardMaterial")

                ir_node.properties["base_color"] = tuple(node.inputs["Base Color"].default_value)
                ir_node.properties["metalness"] = node.inputs["Metallic"].default_value
                ir_node.properties["refl_roughness"] = node.inputs["Roughness"].default_value
                ir_node.properties["diffuse_roughness"] = node.inputs["Diffuse Roughness"].default_value
                ir_node.properties["opacity_color"] = (
                    node.inputs["Alpha"].default_value,
                    node.inputs["Alpha"].default_value,
                    node.inputs["Alpha"].default_value
                )
                ir_node.properties["ms_amount"] = node.inputs["Subsurface Weight"].default_value
                ir_node.properties["ms_radius"] = tuple(node.inputs["Subsurface Radius"].default_value)
                ir_node.properties["ms_phase"] = node.inputs["Subsurface Anisotropy"].default_value
                ir_node.properties["refr_weight"] = node.inputs["Transmission Weight"].default_value
                ir_node.properties["coat_weight"] = node.inputs["Coat Weight"].default_value
                ir_node.properties["coat_roughness"] = node.inputs["Coat Roughness"].default_value
                ir_node.properties["coat_ior"] = node.inputs["Coat IOR"].default_value
                ir_node.properties["coat_color"] = tuple(node.inputs["Coat Tint"].default_value)
                ir_node.properties["sheen_weight"] = node.inputs["Sheen Weight"].default_value
                ir_node.properties["sheen_roughness"] = node.inputs["Sheen Roughness"].default_value
                ir_node.properties["sheen_color"] = tuple(node.inputs["Sheen Tint"].default_value)
                ir_node.properties["emission_color"] = tuple(node.inputs["Emission Color"].default_value)
                ir_node.properties["thinfilm_thickness"] = node.inputs["Thin Film Thickness"].default_value
                ir_node.properties["thinfilm_ior"] = node.inputs["Thin Film IOR"].default_value 

                ir_nodes.append(ir_node)
                blender_node_to_id[node] = ir_node.id

            #special function
            #color ramp node
            elif node.bl_idname == 'ShaderNodeValToRGB':
                ir_node = IRNode(node_id=new_id("ColorRamp"),
                                 node_type="RSRamp")
                color_ramp = node.color_ramp
                stops = []
                for elt in color_ramp.elements:
                    stops.append({
                        "position": elt.position,
                        "color": tuple(elt.color),  # RGBA
                    })
                ir_node.properties["interpolation"] = color_ramp.interpolation
                ir_node.properties["stops"] = stops

                ir_nodes.append(ir_node)
                blender_node_to_id[node] = ir_node.id

            elif node.bl_idname == 'ShaderNodeCombineColor':

                if(node.mode != 'RGB'):
                    self.report({'ERROR'}, "Color combine node only supports RGB mode")
                    return {'CANCELLED'}

                ir_node = IRNode(node_id=new_id("CombineColor"),
                                 node_type="RSColorMaker")
                ir_node.properties["red"] = node.inputs["Red"].default_value
                ir_node.properties["green"] = node.inputs["Green"].default_value
                ir_node.properties["blue"] = node.inputs["Blue"].default_value
                ir_node.properties["alpha"] = 1 #blender node doesn't have an alpha input

                ir_nodes.append(ir_node)
                blender_node_to_id[node] = ir_node.id

            #mix node
            elif node.bl_idname == 'ShaderNodeMix':

                tupleMix = False
                mixType = "RSColorMix" #RBGA default
                if node.data_type == 'FLOAT':
                    mixType = "RSMathMix"

                elif node.data_type == 'VECTOR':                        
                    mixType = "RSMathMixVector"
                    if(node.factor_mode == "NON_UNIFORM"):
                        tupleMix = True

                elif node.data_type == 'ROTATION':
                    #throw blender error cause idfk what rotation mix type is and idk if redshift has an equivalent lmao

                    #TODO: investigate what rotation mix type is
                    self.report({'ERROR'}, "Rotation mix type not supported in vector mix node")
                    return {'CANCELLED'}
                ir_node = IRNode(node_id=new_id("Mix"),
                                    node_type=mixType)
                if node.data_type == 'RGBA' or node.data_type == 'VECTOR':
                    ir_node.properties["input1"] = tuple(node.inputs["A"].default_value)
                    ir_node.properties["input2"] = tuple(node.inputs["B"].default_value)

                else:
                    ir_node.properties["input1"] = node.inputs["A"].default_value
                    ir_node.properties["input2"] = node.inputs["B"].default_value

                if (tupleMix):
                    ir_node.properties["mixAmount"] = tuple(node.inputs["Factor"].default_value)
                else:
                    ir_node.properties["mixAmount"] = node.inputs["Factor"].default_value

                ir_nodes.append(ir_node)
                blender_node_to_id[node] = ir_node.id

            #separate color
            elif node.bl_idname == 'ShaderNodeSeparateColor':
                if(node.mode != 'RGB'):
                    self.report({'ERROR'}, "Color separate node only supports RGB mode")
                    return {'CANCELLED'}

                ir_node = IRNode(node_id=new_id("SeparateColor"),
                                 node_type="RSColorSplitter")
                ir_node.properties["input"] = tuple(node.inputs["Color"].default_value)

                ir_nodes.append(ir_node)
                blender_node_to_id[node] = ir_node.id


            else:
                pass

        # TODO: make sure that it errors on speuclar nodes, i dont wanna deal with it.
        # connections
        for node in node_tree.nodes:
            if node in blender_node_to_id:
                ir_node_id = blender_node_to_id[node]
                for input_socket in node.inputs:
                    if input_socket.is_linked:
                        link = input_socket.links[0]
                        from_node = link.from_node
                        from_socket = link.from_socket
                        if from_node in blender_node_to_id:
                            input_name = input_socket.name
                            from_id = blender_node_to_id[from_node]
                            from_output_name = from_socket.name
                            for irn in ir_nodes:
                                if irn.id == ir_node_id:
                                    irn.connections[input_name] = f"{from_id}:{from_output_name}"

        # JSON
        data_to_save = [n.to_dict() for n in ir_nodes]
        try:
            with open(self.filepath, 'w') as f:
                json.dump(data_to_save, f, indent=2)

            self.report({'INFO'}, f"Exported {len(ir_nodes)} node(s) to {self.filepath}")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to export: {e}")
            return {'CANCELLED'}

        return {'FINISHED'}
    

def register():
    bpy.utils.register_class(RFXUTILS_OT_MaterialParser)

def unregister():
    bpy.utils.unregister_class(RFXUTILS_OT_MaterialParser)