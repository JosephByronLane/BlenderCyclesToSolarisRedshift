import bpy
import json
import os
from ..structs.RSIRNode import IRNode

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

    def execute(self, context):
        print("execuring material parser")
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'ERROR'}, "No objects selected.")
            return {'CANCELLED'}

        base_path = context.scene.custom_folder_path
        tex_path = os.path.join(base_path, "tex")
        os.makedirs(tex_path, exist_ok=True)

        exported_materials = set()

        for obj in selected_objects:
            if obj.type != 'MESH':
                continue
            for mat in obj.data.materials:
                if mat and mat.use_nodes and mat.name not in exported_materials:
                    exported_materials.add(mat.name)
        
                    ir_nodes = []

                    blender_node_to_id = {}

                    def new_id(base_name):
                        new_id.counter += 1
                        return f"{base_name}_{new_id.counter}"
                    new_id.counter = 0

                    #  nodes
                    for node in mat.node_tree.nodes:
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

                            isNonUniform = False
                            if node.data_type == 'FLOAT':
                                mixType = "RSMathMix"

                            elif node.data_type == 'VECTOR':                        
                                mixType = "RSMathMixVector"
                                if(node.factor_mode == "NON_UNIFORM"):
                                    isNonUniform = True

                            elif node.data_type == 'ROTATION':
                                #throw blender error cause idfk what rotation mix type is and idk if redshift has an equivalent lmao

                                #TODO: investigate what rotation mix type is
                                self.report({'ERROR'}, "Rotation mix type not supported in vector mix node")
                                return {'CANCELLED'}
                            
                            elif node.data_type == 'RGBA':
                                if node.blend_type=='MIX':
                                    mixType = "RSColorMix"
                                else:
                                    #we use colorLayer rather than colorComposite because ColorComposite doesn't support mask blending.
                                    mixType = "RSColorLayer"
                            

                            ir_node = IRNode(node_id=new_id("Mix"),
                                                node_type=mixType)
                            
                            inputA = node.inputs["A"].default_value
                            inputB = node.inputs["B"].default_value

                            if node.data_type in ('RGBA', 'VECTOR'):
                                if mixType != "RSColorLayer":
                                    ir_node.properties["input1"] = tuple(inputA)
                                    ir_node.properties["input2"] = tuple(inputB)
                                else:
                                    ir_node.properties["base_color"] = tuple(inputA)
                                    ir_node.properties["layer1_color"] = tuple(inputB)
                            else:
                                ir_node.properties["input1"] = inputA
                                ir_node.properties["input2"] = inputB


                            if mixType != "RSColorLayer":
                                if (isNonUniform):
                                    ir_node.properties["mixAmount"] = tuple(node.inputs["Factor"].default_value)
                                else:
                                    default_val = node.inputs["Factor"].default_value
                                    ir_node.properties["mixAmount"] = (default_val, default_val, default_val)
                            else:
                                ir_node.properties["layer1_mask"] = node.inputs["Factor"].default_value

                            #composite nodes
                            if node.blend_type != 'MIX':

                                if node.blend_type == 'DARKEN':
                                    blendType = "7"
                                elif node.blend_type == 'MULTIPLY':
                                    blendType = "4"
                                elif node.blend_type == 'BURN':
                                    blendType = "11"
                                    
                                elif node.blend_type == 'LIGHTEN':
                                    blendType = "6"
                                elif node.blend_type == 'SCREEN':
                                    blendType = "8"
                                elif node.blend_type == 'DODGE':
                                    blendType = "12"
                                elif node.blend_type == 'ADD':
                                    blendType = "2"

                                elif node.blend_type == 'OVERLAY':
                                    blendType = "13"
                                elif node.blend_type == 'SOFT_LIGHT':
                                    blendType = "10"
                                #linear light doesn't exist in redshift

                                elif node.blend_type == 'DIFFERENCE':
                                    blendType = "5"
                                elif node.blend_type == 'EXCLUSION':
                                    blendType = "14"
                                elif node.blend_type == 'SUBTRACT':
                                    blendType = "3"
                                elif node.blend_type == 'DIVIDE':
                                    blendType = "15"

                                #hue doesnt exist in redshift
                                #saturation doesnt exist in redshift
                                #color doesnt exist in redshift
                                #value doesnt exist in redshift lmao what the fuck

                                else:
                                    self.report({'ERROR'}, f"Color composite mode selected not supported {node.blend_type}")
                                    return {'CANCELLED'}     

                                ir_node.properties["layer1_blend_mode"] = blendType


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

                        #normal map
                        elif node.bl_idname == 'ShaderNodeNormalMap':
                            ir_node = IRNode(node_id=new_id("BumpMap"),
                                            node_type="BumpMap")
                            print(node.space)
                            if node.space != 'TANGENT' and node.space != 'OBJECT':
                                self.report({'ERROR'}, "Normal map node only supports tangent/object space")
                                return {'CANCELLED'}

                            ir_node.properties["scale"] = node.inputs["Strength"].default_value
                            if(node.space == 'TANGENT'):
                                space=1
                            elif(node.space == 'OBJECT'):
                                space=2
                            else:
                                space=0
                            #houdini wants a string for the input type
                            ir_node.properties["inputType"] = str(space)

                            ir_nodes.append(ir_node)
                            blender_node_to_id[node] = ir_node.id

                        #HSV node
                        elif node.bl_idname == 'ShaderNodeHueSaturation':
                            ir_node = IRNode(node_id=new_id("HueSaturation"),
                                            node_type="RSColorCorrection")
                            ir_node.properties["hue"] = node.inputs["Hue"].default_value
                            ir_node.properties["saturation"] = node.inputs["Saturation"].default_value
                            ir_node.properties["level"] = node.inputs["Value"].default_value

                            ir_nodes.append(ir_node)
                            blender_node_to_id[node] = ir_node.id

                        #gamma node
                        elif node.bl_idname == 'ShaderNodeGamma':
                            ir_node = IRNode(node_id=new_id("Gamma"),
                                            node_type="RSColorCorrection")
                            ir_node.properties["gamma"] = node.inputs["Gamma"].default_value

                            ir_nodes.append(ir_node)
                            blender_node_to_id[node] = ir_node.id

                        #range node
                        elif node.bl_idname == 'ShaderNodeMapRange':
                            ir_node = IRNode(node_id=new_id("MapRange"),
                                            node_type="RSMathRange")
                            
                            if node.data_type=='FLOAT_VECTOR':
                                self.report({'ERROR'}, "Vector Map Range isn't supported")
                                return {'CANCELLED'}
                            
                            ir_node.properties["input"] = node.inputs["Value"].default_value
                            ir_node.properties["old_min"] = node.inputs[1].default_value
                            ir_node.properties["old_max"] = node.inputs[2].default_value
                            ir_node.properties["new_min"] = node.inputs[3].default_value
                            ir_node.properties["new_max"] = node.inputs[4].default_value
                            

                            ir_nodes.append(ir_node)
                            blender_node_to_id[node] = ir_node.id

                        #math node
                        elif node.bl_idname == 'ShaderNodeMath':
                            if node.operation == 'ADD':
                                node_type = "RSMathAdd"
                            elif node.operation == 'SUBTRACT':
                                node_type = "RSMathSub"
                            elif node.operation == 'MULTIPLY':
                                node_type = "RSMathMul"
                            elif node.operation == 'DIVIDE':
                                node_type = "RSMathDiv"
                            else:
                                self.report({'ERROR'}, "Unsupported math node operation")
                                return {'CANCELLED'}
                            
                            ir_node = IRNode(node_id=new_id("Math"),
                                            node_type=node_type)
                            #we use numbered outputs here since blender doesn't have a way to name them
                            ir_node.properties["input1"] = node.inputs[0].default_value
                            ir_node.properties["input2"] = node.inputs[1].default_value

                            ir_nodes.append(ir_node)
                            blender_node_to_id[node] = ir_node.id

                        #texture node
                        elif node.bl_idname == 'ShaderNodeTexImage':
                            ir_node = IRNode(node_id=new_id("Texture"),
                                            node_type="TextureSampler")
                            ir_node.properties["tex0"] = node.image.filepath

                            if node.image.colorspace_settings.name == 'Non-Color':
                                ir_node.properties["tex0_colorSpace"] = "Raw"
                            if node.image.colorspace_settings.name == 'sRGB':
                                ir_node.properties["tex0_colorSpace"] = "AgX Base sRGB"

                            ir_nodes.append(ir_node)
                            blender_node_to_id[node] = ir_node.id


                        #value node
                        elif node.bl_idname == 'ShaderNodeValue':
                            ir_node = IRNode(node_id=new_id("Value"),
                                            node_type="RSScalarConstant")
                            ir_node.properties["val"] = node.outputs[0].default_value

                            ir_nodes.append(ir_node)
                            blender_node_to_id[node] = ir_node.id
                            
                        #rgb node
                        elif node.bl_idname == 'ShaderNodeRGB':
                            ir_node = IRNode(node_id=new_id("RGB"),
                                            node_type="RSColorConstant")
                            ir_node.properties["color"] = tuple(node.outputs[0].default_value)

                            ir_nodes.append(ir_node)
                            blender_node_to_id[node] = ir_node.id

                                  

                        elif node.bl_idname == 'ShaderNodeOutputMaterial':
                            pass

                        else:
                            self.report({'INFO'}, "Unsupported detected: " + node.bl_idname)
                            pass


                    # TODO: make sure that it errors on speuclar nodes, i dont wanna deal with it.
                    # connections
                    for node in mat.node_tree.nodes:
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
                    file_path = os.path.join(tex_path, f"{mat.name}.json")
                    try:
                        with open(file_path, 'w') as f:
                            json.dump(data_to_save, f, indent=2)
                        self.report({'INFO'}, f"Exported {mat.name} to {file_path}")
                    except Exception as e:
                        self.report({'ERROR'}, f"Failed to export {mat.name}: {e}")

        return {'FINISHED'}
    

def register():
    bpy.utils.register_class(RFXUTILS_OT_MaterialParser)

def unregister():
    bpy.utils.unregister_class(RFXUTILS_OT_MaterialParser)