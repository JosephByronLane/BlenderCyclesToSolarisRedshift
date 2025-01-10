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
    
    
    
    
    
    internalConnections={
    }

    if isNormalMapConnected:
        internalConnections[f"{normalMapName}:out"] = f"{bumpMapName}:normalMap"
    
    inboundConnectors = {
       
    }

    outboundConnectors = {

    }


    rsirGraph = RSIRGraph(
        uId=node.name,
        children=[],
        internalConnections=internalConnections,
        inboundConnectors=inboundConnectors,
        outboundConnectors=outboundConnectors
    )
    parsedNodes.append(node.name)
    parsedNodes.append(inputNormalMapNode.name)
    
    return rsirGraph

