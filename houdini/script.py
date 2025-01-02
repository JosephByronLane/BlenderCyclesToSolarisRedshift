import hou
import json

def import_ir_json():
    """Create Redshift nodes under parent_node from IR JSON."""
    
    filepath = "E:\Steam\steamapps\common\Blender\my_material.json"
    
    # JSON
    with open(filepath, 'r') as f:
        ir_data = json.load(f)
    stage = hou.node("/stage")
    if not stage:
        raise RuntimeError("Could not find /stage node!")
    
    matlib = stage.createNode('materiallibrary', node_name="CharaMatlib")
    parent_node = matlib.createNode('rs_usd_material_builder', node_name="test2")

    created_nodes = {}
    
    for node_info in ir_data:
        node_id   = node_info["id"]
        node_type = node_info["type"]
        props     = node_info["properties"]
        
        if node_type == "PrincipledBSDF":
           
            new_node = hou.node('/stage/CharaMatlib/test2/StandardMaterial1')
            if not new_node:
                print("didnt fid base material")                
            print("found base material")
            
            for name, value in props.items():
                try:
                    if isinstance(value, (list, tuple)) and len(value) == 4:
                        # RGBA; set to RGB
                        rgb = (value[0], value[1], value[2])
                        parm = new_node.parmTuple(name)
                        if parm:
                            parm.set(rgb)
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

        elif node_type == "ColorRamp":

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
            
            
            print(bases, tuple(positions), tuple(values))
            ramp_data = hou.Ramp(bases, tuple(positions), tuple(values))      
            

            rampParm = new_node.parm('ramp')
            rampParm.set(ramp_data)
            created_nodes[node_id] = new_node

        else:
            print(f"Skipping node type: {node_type} (not implemented)")
    

    for node_info in ir_data:
        node_id  = node_info["id"]
        conns    = node_info["connections"]        
        print("bbb")
        
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
                    this_node.setNamedInput(mapping[input_name], from_node, "outColor")
                else:
                    print(f"Input {input_name} not found in Redshift's equivalent node")
                   
            


            if from_node.type().name() == "Redshift::TextureRamp":
                # the output might be "outColor" or "out"
                pass


            pass

    # Layout the nodes so they’re not all stacked
    parent_node.layoutChildren()
    print(f"Imported {len(created_nodes)} IR nodes into {parent_node.path()}")



import_ir_json()
