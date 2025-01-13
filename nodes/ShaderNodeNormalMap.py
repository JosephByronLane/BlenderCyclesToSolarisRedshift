from .nodeRegistry import registerNode

from ..data.RSIRGraph import RSIRGraph 
from ..data.RSIRNode import RSIRNode

from ..utils.uniqueDict import generateNodeName
from ..utils.redshiftPrefix import prefixRedhisftNode

@registerNode('ShaderNodeNormalMap')
def defineShaderNodeNormalMap(node, errors, parsedNodes):

    isConnectedToBumpMap = node.outputs["Normal"].links[0].to_node.bl_idname == 'ShaderNodeBump'

    if isConnectedToBumpMap:
        #if its connected to a bump map, we will handle it in the bump map node
        return None


    #raw strings of nodes
    normalString = "BumpMap"

    #generate names
    normalName= generateNodeName(normalString)

    #make the redshift type names
    normalType = prefixRedhisftNode(normalString)

     #make the redshift type nodes
    normalNode = RSIRNode(node_id=normalName,  node_type= normalType)

    #proprieties
    if node.space != 'TANGENT' and node.space != 'OBJECT':
        errors.append(f"Space not supported on node: {node.name}. Will default to TANGENT")

    normalNode.properties["scale"] = node.inputs["Strength"].default_value
    if(node.space == 'TANGENT'):
        space="1"
    elif(node.space == 'OBJECT'):
        space="2"
    else:
        space="1"

    #houdini wants a string for the input type
    normalNode.properties["inputType"] = space

    internalConnections={
    }


    inboundConnectors = {
       f"{node.bl_idname}:Color": f"{normalName}:input",
       f"{node.bl_idname}:Strength": f"{normalName}:scale"
    }

    outboundConnectors = {
        f"{node.bl_idname}:Normal": f"{normalName}:out"
    }

    if node.uv_map:
        errors.append(f"UV map not supported on node: {node.name}. Will be ignored")

    rsirGraph = RSIRGraph(
        uId=node.name,
        children=[normalNode],
        internalConnections=internalConnections,
        inboundConnectors=inboundConnectors,
        outboundConnectors=outboundConnectors
    )
    parsedNodes.append(node.name)

    return rsirGraph

