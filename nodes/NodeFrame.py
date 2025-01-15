from .nodeRegistry import registerNode

from ..data.RSIRGraph import RSIRGraph 
from ..data.RSIRNode import RSIRNode

from ..utils.uniqueDict import generateNodeName
from ..utils.redshiftPrefix import prefixRedhisftNode

@registerNode('NodeFrame')
def defineNodeFrame(node, errors, parsedNodes):


    #we could tecnically add support to the frame node, but due to houdini's .layoutChildren not organizing them they would all be strewn around in the center.
    #in theory we *might* be able to copy blender's nodes positions and somehow translate those into houdini, but idk and im not in the mood to find out.

    #TODO: could the above be done?
    return None

    #raw strings of nodes
    exampleString = "asdf"

    #generate names
    texSamplerName= generateNodeName(texSamplerName)

    #make the redshift type names
    clampResultType = prefixRedhisftNode(texSamplerName)

     #make the redshift type nodes
    texSamplerNode = RSIRNode(node_id=texSamplerName,  node_type= clampResultType)

    #proprieties


    internalConnections={
    }


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

    return rsirGraph

