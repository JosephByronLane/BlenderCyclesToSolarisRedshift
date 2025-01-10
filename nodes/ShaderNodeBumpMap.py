from .nodeRegistry import registerNode

from ..data.RSIRGraph import RSIRGraph 
from ..data.RSIRNode import RSIRNode

from ..utils.uniqueDict import generateNodeName
from ..utils.redshiftPrefix import prefixRedhisftNode

@registerNode('ShaderNodeBumpMap')
def defineShaderNodeBumpMap(node, errors, parsedNodes):


    graphChildren = []

    isNormalMapConnected = node.inputs["Normal"].is_linked and node.inputs["Normal"].links[0].to_node.type == "ShaderNodeNormalMap"

    if isNormalMapConnected:
        inputNormalMapNode = node.inputs["Normal"].links[0].from_node

    #raw strings of nodes
    bumpMapString = "BumpMap"
    normalMapString = "BumpMap"

    bumpBlenderString = "BumpBlender"


    #generate names
    bumpMapName= generateNodeName(bumpMapString)
    normalMapName= generateNodeName(normalMapString)

    bumpBlenderName= generateNodeName(bumpBlenderString)

    #make the redshift type names
    bumpMapType = prefixRedhisftNode(bumpMapString)
    normalMapType = prefixRedhisftNode(normalMapString)

    bumpBlenderType = prefixRedhisftNode(bumpBlenderString)


     #make the redshift type nodes
    bumpMapNode = RSIRNode(node_id=bumpMapName,  node_type= bumpMapType)
    normalMapNode = RSIRNode(node_id=normalMapName,  node_type= normalMapType)

    bumpBlenderNode = RSIRNode(node_id=bumpBlenderName,  node_type= bumpBlenderType)

    #proprieties

    bumpMapNode.properties["inputType"] = "0"
    bumpMapNode.properties["scale"] = node.inputs["Distance"].default_value



    bumpBlenderNode.properties["bumpWeight0"] = 1
    bumpBlenderNode.properties["additive"] = 1
    
    
    
    internalConnections={
    }

    if isNormalMapConnected:
        internalConnections[f"{normalMapName}:out"] = f"{bumpBlenderName}:bumpInput0"
        internalConnections[f"{bumpMapName}:out"] = f"{bumpBlenderName}:baseInput"
    
    inboundConnectors = {
       
    }

    if isNormalMapConnected:
        inboundConnectors[f"{inputNormalMapNode.bl_idname}:Color"] = f"{normalMapName}:input"
        inboundConnectors[f"{inputNormalMapNode.bl_idname}:Strength"] = f"{normalMapName}:scale"

    inboundConnectors[f"{node.bl_idname}:Normal"] = f"{bumpMapName}:input"
    inboundConnectors[f"{node.bl_idname}:Distance"] = f"{bumpMapName}:scale"


    outboundConnectors = {
    }

    if isNormalMapConnected:
        outboundConnectors[f"{node.bl_idname}:Normal"] = f"{bumpBlenderName}:outDisplacement"
    else:
        outboundConnectors[f"{node.bl_idname}:Normal"] = f"{bumpMapName}:out"




    if isNormalMapConnected:
        graphChildren.append(normalMapNode)
        graphChildren.append(bumpBlenderNode)
    
    graphChildren.append(bumpMapNode)

    rsirGraph = RSIRGraph(
        uId=node.name,
        children=graphChildren,
        internalConnections=internalConnections,
        inboundConnectors=inboundConnectors,
        outboundConnectors=outboundConnectors
    )
    parsedNodes.append(node.name)
    parsedNodes.append(inputNormalMapNode.name)
    
    return rsirGraph

