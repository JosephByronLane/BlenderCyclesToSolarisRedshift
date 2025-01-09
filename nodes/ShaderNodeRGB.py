from .nodeRegistry import registerNode

from ..data.RSIRGraph import RSIRGraph 
from ..data.RSIRNode import RSIRNode

from ..utils.uniqueDict import generateNodeName
from ..utils.redshiftPrefix import prefixRedhisftNode

@registerNode('ShaderNodeRGB')
def defineShaderNodeRGB(node, errors):

    #raw strings of nodes
    colorConstantString = "RSColorConstant"

    #generate names
    colorConstantName= generateNodeName(colorConstantString)

    #make the redshift type names
    colorConstantType = prefixRedhisftNode(colorConstantString)

     #make the redshift type nodes
    colorConstantNode = RSIRNode(node_id=colorConstantName,  node_type= colorConstantType)

    #proprieties
    colorConstantNode.properties["color"] = tuple(node.outputs[0].default_value)

    #single node, no internal connections
    internalConnections={
    }

    #RGB node has no inbound connections
    inboundConnectors = {
       
    }

    outboundConnectors = {
        f"{node.bl_idname}:Color": f"{colorConstantName}:outColor"
    }


    rsirGraph = RSIRGraph(
        uId=node.name,
        children=[colorConstantNode],
        internalConnections=internalConnections,
        inboundConnectors=inboundConnectors,
        outboundConnectors=outboundConnectors
    )

    return rsirGraph

