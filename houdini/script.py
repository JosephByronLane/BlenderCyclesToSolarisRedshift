import hou
import json
import os, stat

def import_ir_json(filepath, matlibNode=None):
    """Create Redshift nodes under parent_node from IR JSON."""
            
    if matlibNode is None:
        raise RuntimeError("Error getting material library node")

    
    # Read JSON
    with open(filepath, 'r') as f:
        ir_data = json.load(f)  

    matname = filepath.split("/")[-1].split(".")[0]
    parent_node = matlibNode.createNode('rs_usd_material_builder', node_name=matname)

    created_nodes = {}
    
    for node_info in ir_data:
        node_id   = node_info["id"]
        node_type = node_info["type"]
        props     = node_info["properties"]
        
        
        #first we handle the nodes which require special handling (E.g RSRamp/ColorRamp)
        
        
        #RSRamp
        if node_type == "RSRamp":

            new_node = parent_node.createNode("redshift::RSRamp", node_name=node_id)
            
            stops = props.get("stops", [])
            interpolationValue = props.get("interpolation", "CONSTANT")  
            
            interpolation = {
                "LINEAR":    hou.rampBasis.Linear,
                "EASE":      hou.rampBasis.CatmullRom,  
                "CONSTANT":  hou.rampBasis.Constant,
                "CARDINAL":  hou.rampBasis.Bezier,
                "B_SPLINE":  hou.rampBasis.BSpline
            }            

            ramp_basis = interpolation.get(interpolationValue)
            
            positions = []
            values = []
            for stop in stops:
                positions.append(stop["position"])
                r, g, b, a = stop["color"]  # ignoring alpha
                values.append((r, g, b))
                
            num_stops = len(stops)
            bases = tuple(ramp_basis for _ in range(num_stops))
            
            
            ramp_data = hou.Ramp(bases, tuple(positions), tuple(values))      
            
            # For interpolation, if Redshift ramp has a parameter for that:
            # new_node.parm("interpolation").set(interpolation)
            rampParm = new_node.parm('ramp')
            rampParm.set(ramp_data)
            created_nodes[node_id] = new_node

        

        #StandardMaterial
        #we need a separate function for the standard material because we aren't creating a new one, rather simply referencing the existing one
        elif node_type == "StandardMaterial":


            #TODO: use relative paths for this
            new_node = hou.node('/stage/' + matlibNode.name() + '/' + matname + '/StandardMaterial1')
            if not new_node:
                print("didnt fid base material")                
            print("found base material")
            
            for name, value in props.items():
                try:
                    if isinstance(value, (list, tuple)) and len(value) == 4:
                        # Assume RGBA; set only RGB
                        rgb = (value[0], value[1], value[2])
                        parm = new_node.parmTuple(name)
                        if parm:
                            parm.set(rgb)
                        else:
                            print(f"Parameter '{name}' not found on node '{node_type}'.")
                    else:
                        # Single value parameter
                        parm = new_node.parm(name)
                        if parm:
                            parm.set(value)
                        else:
                            print(f"Parameter '{name}' not found on node '{node_type}'.")
                            
                except Exception as e:
                    print(f"Failed to set parameter '{name}' on node '{node_type}': {e}")
            
          
            created_nodes[node_id] = new_node
        
        #RSMathMixVector
        #for some fucking reason you can set the node's iputs as a tuple,  instead needing to set them per-element
        elif node_type == "RSMathMixVector":
            node_to_create_type = "redshift::" + node_type
            print("Creating node of type", node_to_create_type)
            new_node = parent_node.createNode(node_to_create_type, node_name=node_id)
            for name, value in props.items():
                try:
                    for i in range(1, 4):
                        parm_name = f"{name}{i}"  # 'input11', 'input12', 'input13'
                        parm = new_node.parm(parm_name)
                        if parm:
                            parm.set(value[i-1])
                        else:
                            print(f"Parameter '{parm_name}' not found on node '{node_id}'.")

                except Exception as e:
                    print(f"Failed to set parameter '{name}' on node '{node_id}': {e}")
            
            created_nodes[node_id] = new_node
        
        
        #Generic node handler    
        else:
            node_to_create_type = "redshift::" + node_type
            print("Creating node of type", node_to_create_type)
            new_node = parent_node.createNode(node_to_create_type, node_name=node_id)
            
            for name, value in props.items():
                try:
                    if isinstance(value, (list, tuple)) and len(value) == 4:
                        parm = new_node.parmTuple(name)
                        if parm:
                            parm.set(value)
                        else:
                            print(f"Parameter '{name}' not found on node '{node_id}'.")
                    else:
                        parm = new_node.parm(name)
                        if parm:
                            parm.set(value)
                        else:
                            print(f"Parameter '{name}' not found on node '{node_id}'.")
                            
                except Exception as e:
                    print(f"Failed to set parameter '{name}' on node '{node_id}': {e}")
            
            created_nodes[node_id] = new_node
            print(f"Created node {new_node} with id {node_id}")
    

    for node_info in ir_data:
        node_id  = node_info["id"]
        conns    = node_info["connections"]  # e.g. {"Base Color": "ColorRamp_2:Color"}        
        
        if node_id not in created_nodes:
            continue  # skip unimplemented node types
        
        for input_name, from_str in conns.items():            
         
            # from_str might look like "ColorRamp_2:Color"
            
            from_id, from_output_name = from_str.split(":")
            
            if from_id not in created_nodes:
                print(f"Connection from {from_id} not found in created nodes.")
                continue
            
            this_node = created_nodes[node_id]
            from_node = created_nodes[from_id]

            print(f"Iterating over connections: {input_name} -> {from_str} on {from_node} -> {this_node}")

            #INPUTS
            if this_node.type().name() == "redshift::StandardMaterial":
               
                Input_mapping= {
                    "Base Color":         "base_color",
                    "Metallic":           "metalness",  
                    "Roughness":          "refl_roughness",
                    "Diffuse Roughness":  "diffuse_roughness",
                    "Alpha":              "opacity_color",
                    "Normal": "bump_input",
                    "Subsurface Weight": "ms_amount",
                    "Subsurface Radius": "ms_radius",
                    "Subsurface Anisotropy": "ms_phase",
                    "Transmission Weight": "refr_weight",
                    "Coat Weight": "coat_weight",
                    "Coat Roughness": "coat_roughness",
                    "Coat IOR": "coat_ior",
                    "Coat Tint": "coat_color",
                    "Coat Normal": "coat_bump_input",
                    "Sheen Weight": "sheen_weight",
                    "Sheen Roughness": "sheen_roughness",
                    "Sheen Tint": "sheen_color",
                    "Emission Color": "emission_color",
                    "Thin Film Thickness": "thinfilm_thickness",
                    "Thin Film IOR": "thinfilm_ior"                    
                }


            elif this_node.type().name() == "redshift::RSRamp":
                Input_mapping= {
                    "Fac": "input"
                }

            elif this_node.type().name() == "redshift::RSMathMixVector" or this_node.type().name() == "redshift::RSColorMix" or this_node.type().name() == "redshift::RSMathMix":
                Input_mapping= {
                    "A": "input1",
                    "B": "input2",
                    "Factor": "mixAmount"
                }


            elif this_node.type().name() == "redshift::RSColorMaker":
                Input_mapping= {
                    "Red": "red",
                    "Green": "green",
                    "Blue": "blue",
                }

            elif this_node.type().name() == "redshift::RSColorSplitter":
                Input_mapping= {
                    "Color": "input",
                }
            
            elif this_node.type().name() == "redshift::BumpMap":
                Input_mapping= {
                    "Color": "input",
                    "Strength": "scale",
                }

            #math nodes
            elif this_node.type().name() == "redshift::RSMathMul" or this_node.type().name() == "redshift::RSMathAdd" or this_node.type().name() == "redshift::RSMathSub" or this_node.type().name() == "redshift::RSMathDiv":
                Input_mapping= {
                    "input1": "input1",
                    "input2": "input2",
                }

            elif this_node.type().name() == "redshift::RSScalarConstant":
                Input_mapping= {
                    "Value": "val",
                }





            #OUTPUTS
            if from_node.type().name() == "redshift::StandardMaterial":
                output_mapping={
                    "Color": "outColor",
                }

            elif from_node.type().name() == "redshift::BumpMap":
                output_mapping={
                    "Normal": "out",
                }
            
            elif from_node.type().name() == "redshift::RSRamp":              
                output_mapping={
                    "Color": "outColor"
                }

            elif from_node.type().name() == "redshift::RSColorMix" :
                output_mapping = {
                    "Result": "outColor" 
                }
            elif from_node.type().name() == "redshift::RSMathMix" or  from_node.type().name() =="redshift::RSMathMixVector":
                output_mapping = {
                    "Result": "out" 
                }

            elif from_node.type().name() == "redshift::RSColorMaker":
                output_mapping={
                    "Color": "outColor"
                }
            elif from_node.type().name() == "redshift::RSColorSplitter":
                output_mapping={
                    "Red": "outR",
                    "Green": "outG",
                    "Blue": "outB"
                }

            elif from_node.type().name() == "redshift::RSMathMul" or from_node.type().name() == "redshift::RSMathAdd" or from_node.type().name() == "redshift::RSMathSub" or from_node.type().name() == "redshift::RSMathDiv":
                output_mapping={
                    "Value": "out"
                }

            elif from_node.type().name() == "redshift::TextureSampler":
                output_mapping={
                    "Color": "outColor"
                }

            elif from_node.type().name() == "redshift::RSScalarConstant":
                output_mapping={
                    "Value": "out"
                }

            if input_name in Input_mapping:
                print(f"Connecting {from_node.name()}'s {from_output_name} to {this_node.name()}'s {input_name}")
                print(f"{Input_mapping[input_name]}, {from_node.name()}, {output_mapping[from_output_name]}")

                #setNamedInput("refl_roughness", inputNode, "outColor")
                this_node.setNamedInput(Input_mapping[input_name], from_node, output_mapping[from_output_name])
            
            else:
                print(f"Input {input_name} not found in Redshift's equivalent node")
                   


            pass

    parent_node.layoutChildren()
    matlibNode.layoutChildren()
    
    print(f"Imported {len(created_nodes)} IR nodes into {parent_node.path()}")

def has_hidden_attribute(filepath):
    return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)

def autoDetectFolder(autoDetectDrive='H:/'):
    try: 
        if not os.path.exists(autoDetectDrive):
            raise Exception("Auto Detect directory doesn't exist") 
    
        visible_folders = []
        
        for entry in os.listdir(autoDetectDrive):
            full_path = os.path.join(autoDetectDrive, entry)
            if not has_hidden_attribute(full_path) and os.path.isdir(full_path):
                visible_folders.append(full_path)
        
        if not visible_folders:
            raise Exception( "No visible folders found in H: drive.")
        
        #select the first folder, since there should one be one ($ACTIVE) 
        selected_folder = visible_folders[0]
        return selected_folder
    
    except Exception as e:
        raise Exception(f"Error during auto-detection: {e}")

def findAllJson(projectDirectory):
    foundFiles=[]
    for root, dirs, files in os.walk(projectDirectory + '/tex/'):
    # select file name
        for file in files:
            # check the extension of files
            if file.endswith('.json'):
                foundFiles.append(os.path.join(root, file))

    return foundFiles

projectFolder = autoDetectFolder()
jsonFiles = findAllJson(projectFolder)
stage = hou.node("/stage")
if not stage:
    raise RuntimeError("Could not find /stage!")  

matlibNode = stage.createNode('materiallibrary', node_name='RuneMatLib')

for file in jsonFiles:
    import_ir_json(file, matlibNode)

