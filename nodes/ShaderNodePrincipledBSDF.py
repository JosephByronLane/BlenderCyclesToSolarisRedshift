from .nodeRegistry import registerNode

from ..data.RSIRGraph import RSIRGraph 
from ..data.RSIRNode import RSIRNode

from ..utils.uniqueDict import generateNodeName
from ..utils.redshiftPrefix import prefixRedhisftNode

@registerNode('ShaderNodeBsdfPrincipled')
def definePrincipledBsdf(node, errors, parsedNodes):

    graphChildren = []

    nodeName= generateNodeName("StandardMaterial")

    sssMultName = generateNodeName("RSMathMulVector")

    sssColorName = generateNodeName("RSColorConstant")

    sssMultNode = RSIRNode(node_id=sssMultName, node_type=prefixRedhisftNode("RSMathMulVector"))

    rsirNode = RSIRNode(node_id=nodeName,  node_type=prefixRedhisftNode("StandardMaterial"))

    sssColorNode = RSIRNode(node_id=sssColorName,  node_type=prefixRedhisftNode("RSColorConstant"))


    rsirNode.properties["base_color"] = tuple(node.inputs["Base Color"].default_value[:3])
    rsirNode.properties["metalness"] = node.inputs["Metallic"].default_value
    rsirNode.properties["refl_roughness"] = node.inputs["Roughness"].default_value
    rsirNode.properties["diffuse_roughness"] = node.inputs["Diffuse Roughness"].default_value
    rsirNode.properties["opacity_color"] = (
        node.inputs["Alpha"].default_value,
        node.inputs["Alpha"].default_value,
        node.inputs["Alpha"].default_value
    )
    rsirNode.properties["ms_amount"] = node.inputs["Subsurface Weight"].default_value
    rsirNode.properties["ms_radius"] = tuple(node.inputs["Subsurface Radius"].default_value)

    if node.subsurface_method == 'RANDOM_WALK':
       rsirNode.properties["ms_phase"] = node.inputs["Subsurface Anisotropy"].default_value

    rsirNode.properties["ms_radius_scale"] = node.inputs["Subsurface Scale"].default_value

    if node.subsurface_method != 'RANDOM_WALK':
        errors.append(f"Subsurface method not supported on node: {node.name} will default to Random Walk")

    rsirNode.properties["refr_weight"] = node.inputs["Transmission Weight"].default_value
    rsirNode.properties["coat_weight"] = node.inputs["Coat Weight"].default_value
    rsirNode.properties["coat_roughness"] = node.inputs["Coat Roughness"].default_value
    rsirNode.properties["coat_ior"] = node.inputs["Coat IOR"].default_value
    rsirNode.properties["coat_color"] = tuple(node.inputs["Coat Tint"].default_value[:3])
    rsirNode.properties["sheen_weight"] = node.inputs["Sheen Weight"].default_value
    rsirNode.properties["sheen_roughness"] = node.inputs["Sheen Roughness"].default_value
    rsirNode.properties["sheen_color"] = tuple(node.inputs["Sheen Tint"].default_value[:3])
    rsirNode.properties["emission_color"] = tuple(node.inputs["Emission Color"].default_value[:3])
    rsirNode.properties["thinfilm_thickness"] = node.inputs["Thin Film Thickness"].default_value
    rsirNode.properties["thinfilm_ior"] = node.inputs["Thin Film IOR"].default_value 
    internalConnections = {}

    sssMultNode.properties["input1"] = tuple(node.inputs["Subsurface Radius"].default_value)

    sssColorNode.properties["val"] = tuple(node.inputs["Subsurface Radius"].default_value)

    if node.inputs["Subsurface Scale"].is_linked:
        internalConnections={
            f"{sssMultName}:out":                f"{nodeName}:ms_radius",
            f"{sssColorName}:outColor":           f"{sssMultName}:input1"
        }


    #TODO: if has inbound connections in the specular tab we need to return an error
    inboundConnectors = {
        f"{node.bl_idname}:Base Color":                f"{nodeName}:base_color",
        f"{node.bl_idname}:Metallic":             f"{nodeName}:metalness",  
        f"{node.bl_idname}:Roughness":            f"{nodeName}:refl_roughness",
        f"{node.bl_idname}:IOR":                  f"{nodeName}:refl_ior",
        f"{node.bl_idname}:Diffuse Roughness":    f"{nodeName}:diffuse_roughness",
        f"{node.bl_idname}:Alpha":                f"{nodeName}:opacity_color",
        f"{node.bl_idname}:Normal":               f"{nodeName}:bump_input",
        f"{node.bl_idname}:Subsurface Weight":    f"{nodeName}:ms_amount",
        f"{node.bl_idname}:Subsurface Radius":    f"{sssMultName}:input1",
        f"{node.bl_idname}:Subsurface Anisotropy":f"{nodeName}:ms_phase",
        f"{node.bl_idname}:Subsurface Scale":     f"{sssMultName}:input2",
        f"{node.bl_idname}:Transmission Weight":  f"{nodeName}:refr_weight",
        f"{node.bl_idname}:Coat Weight":          f"{nodeName}:coat_weight",
        f"{node.bl_idname}:Coat Roughness":       f"{nodeName}:coat_roughness",
        f"{node.bl_idname}:Coat IOR":             f"{nodeName}:coat_ior",
        f"{node.bl_idname}:Coat Tint":            f"{nodeName}:coat_color",
        f"{node.bl_idname}:Coat Normal":          f"{nodeName}:coat_bump_input",
        f"{node.bl_idname}:Sheen Weight":         f"{nodeName}:sheen_weight",
        f"{node.bl_idname}:Sheen Roughness":      f"{nodeName}:sheen_roughness",
        f"{node.bl_idname}:Sheen Tint":           f"{nodeName}:sheen_color",
        f"{node.bl_idname}:Emission Color":       f"{nodeName}:emission_color",
        f"{node.bl_idname}:Thin Film Thickness":  f"{nodeName}:thinfilm_thickness",
        f"{node.bl_idname}:Thin Film IOR":        f"{nodeName}:thinfilm_ior"    
    }

    outboundConnectors = {
        f"{node.bl_idname}:BSDF": f"{nodeName}:outColor" 
    }

    if node.inputs["Specular IOR Level"].is_linked:
        errors.append(f"IOR Level input not supported on node: {node.name}")

    if node.inputs["Specular Tint"].is_linked:
        errors.append(f"Specular Tint input not supported on node: {node.name}")

    if node.inputs["Anisotropic"].is_linked:
        errors.append(f"Specular Anisotropic input not supported on node: {node.name}")

    if node.inputs["Anisotropic Rotation"].is_linked:
        errors.append(f"Specular Anisotropic Rotation input not supported on node: {node.name}")

    if node.inputs["Tangent"].is_linked:
        errors.append(f"Specular Tangent input not supported on node: {node.name}") 

    if node.inputs["Subsurface Scale"].is_linked:
        graphChildren.append(sssMultNode)
        graphChildren.append(sssColorNode)

    graphChildren.append(rsirNode)

    rsirGraph = RSIRGraph(
        uId=node.name,
        children=graphChildren,
        internalConnections=internalConnections,
        inboundConnectors=inboundConnectors,
        outboundConnectors=outboundConnectors
    )
    parsedNodes.append(node.name)

    return rsirGraph

