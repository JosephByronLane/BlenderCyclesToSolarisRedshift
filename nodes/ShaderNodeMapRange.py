from .nodeRegistry import registerNode

from ..data.RSIRGraph import RSIRGraph 
from ..data.RSIRNode import RSIRNode

from ..utils.uniqueDict import generateNodeName
from ..utils.redshiftPrefix import prefixRedhisftNode

@registerNode('ShaderNodeMapRange')
def defineShaderNodeMapRange(node, errors, parsedNodes):

    #raw strings of nodes
    mapRangeString = "RSMathRange"

    if node.data_type == 'FLOAT':
        mapRangeString = "RSMathRange"

    elif node.data_type == 'FLOAT_VECTOR':
        mapRangeString = "RSMathRangeVector"
     
    else:
        errors.append(f"Node {node.name} has an invalid data type: {node.data_type}. Will default to FLOAT")
        mapRangeString = "RSMathRange"

    #generate names
    mapRangeName= generateNodeName(mapRangeString)

    #make the redshift type names
    mapRangeType = prefixRedhisftNode(mapRangeString)

     #make the redshift type nodes
    mapRangeNode = RSIRNode(node_id=mapRangeName,  node_type= mapRangeType)

    #proprieties
    mapRangeNode.properties["input"] = node.inputs["Value"].default_value
    mapRangeNode.properties["old_min"] = node.inputs["From Min"].default_value
    mapRangeNode.properties["old_max"] = node.inputs["From Max"].default_value
    mapRangeNode.properties["new_min"] = node.inputs["To Min"].default_value
    mapRangeNode.properties["new_max"] = node.inputs["To Max"].default_value


    internalConnections={
    }


    inboundConnectors = {
        f"{node.bl_idname}:Value": f"{mapRangeName}:input",
        f"{node.bl_idname}:From Min": f"{mapRangeName}:old_min",
        f"{node.bl_idname}:From Max": f"{mapRangeName}:old_max",
        f"{node.bl_idname}:To Min": f"{mapRangeName}:new_min",
        f"{node.bl_idname}:To Max": f"{mapRangeName}:new_max",
    }

    outboundConnectors = {
        f"{node.bl_idname}:Result": f"{mapRangeName}:out",
    }

    if node.interpolation_type != "LINEAR":
        errors.append(f"Node {node.name} only supports Linear interpolation. Will default to LINEAR")

    if not node.clamp:
        errors.append(f"Node {node.name} only supports clamped values. Will default to clamped")

    rsirGraph = RSIRGraph(
        uId=node.name,
        children=[mapRangeNode],
        internalConnections=internalConnections,
        inboundConnectors=inboundConnectors,
        outboundConnectors=outboundConnectors
    )
    parsedNodes.append(node.name)

    return rsirGraph

