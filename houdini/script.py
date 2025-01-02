# houdini_import.py

import hou
import json

def import_ir_json():
    """Create Redshift nodes under parent_node from IR JSON."""
    
    filepath = "E:\Steam\steamapps\common\Blender\my_material.json"
    
    # Read JSON
    with open(filepath, 'r') as f:
        ir_data = json.load(f)
    stage = hou.node("/stage")
    if not stage:
        raise RuntimeError("Could not find /stage node!")
    
    matlib = stage.createNode('materiallibrary', node_name="CharaMatlib")
    parent_node = matlib.createNode('rs_usd_material_builder', node_name="test2")

    # Build a dictionary: node_id -> the newly created Hou node
    created_nodes = {}
    
    for node_info in ir_data:
        node_id   = node_info["id"]
        node_type = node_info["type"]
        props     = node_info["properties"]
        
        
        #first we handle the nodes which require special handling (E.g RSRamp/ColorRamp)
        
        
        #RSRamp
        if node_type == "RSRamp":
            # Create a Redshift Ramp node
            # Redshift has a couple of ramp-like nodes, such as "RSColorRamp" or "Redshift::TextureRamp"
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
            new_node = hou.node('/stage/CharaMatlib/test2/StandardMaterial1')
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
                            print(f"Parameter '{name}' not found on node '{node_id}'.")
                    else:
                        # Single value parameter
                        parm = new_node.parm(name)
                        if parm:
                            parm.set(value)
                        else:
                            print(f"Parameter '{name}' not found on node '{node_id}'.")
                            
                except Exception as e:
                    print(f"Failed to set parameter '{name}' on node '{node_id}': {e}")
            
          
            created_nodes[node_id] = new_node
        
        #RSMathMixVector
        #for some fucking reason you can address the node's iputs as a tuple,  instead needing to set them per-element
        elif node_type == "RSMathMixVector":
            node_to_create_type = "redshift::" + node_type
            print("Creating node of type", node_to_create_type)
            new_node = parent_node.createNode(node_to_create_type, node_name=node_id)
            for name, value in props.items():
                try:
                    for j in range(1, 3):
                        for i in range(1, 4):
                            parm = new_node.parm(f"input{j}{i}")
                            if parm:
                                parm.set(value[(i-1)])
                            else:
                                print(f"Parameter '{name}' not found on node '{node_id}'.")

                except Exception as e:
                    print(f"Failed to set parameter '{name}' on node '{node_id}': {e}")
            
            created_nodes[node_id] = new_node
        
            
        #Generic node handler    
        else:
            # Create a generic Redshift node
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
    
    # Now handle connections
    # We'll do a second pass to read node_info["connections"] and wire them up
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

            if this_node.type().name() == "redshift::StandardMaterial":

               
                mapping= {
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
                
                if input_name in mapping:
                    out_name = from_node.outputNames()[0]   
                    this_node.setNamedInput(mapping[input_name], from_node, out_name)
                else:
                    print(f"Input {input_name} not found in Redshift's equivalent node")
                   

            if from_node.type().name() == "Redshift::TextureRamp":
                # the output might be "outColor" or "out"
                pass

            # The exact approach to hooking up is heavily dependent on how Redshift nodes
            # are exposed in Houdini’s interface. 
            # For now, we'll just do a placeholder:
            pass

    # Layout the nodes so they’re not all stacked
    print("aaa")
    parent_node.layoutChildren()
    print(f"Imported {len(created_nodes)} IR nodes into {parent_node.path()}")


# Example usage in Houdini's Python shell (assuming you have a Material Network node at /mat):
# matnet = hou.node("/mat")
import_ir_json()
