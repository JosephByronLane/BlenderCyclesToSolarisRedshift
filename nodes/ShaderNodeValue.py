from .nodeRegistry import registerNode

from ..data.RSIRGraph import RSIRGraph 
from ..data.RSIRNode import RSIRNode

from ..utils.uniqueDict import generateNodeName
from ..utils.redshiftPrefix import prefixRedhisftNode

@registerNode('ShaderNodeValue')
def defineShaderNodeValue(node, errors):

    #raw strings of nodes
    scalarConstantString = "RSScalarConstant"

    #generate names
    scalarConstantName= generateNodeName(scalarConstantString)

    #make the redshift type names
    scalarConstantType = prefixRedhisftNode(scalarConstantName)

     #make the redshift type nodes
    scalarConstantNode = RSIRNode(node_id=scalarConstantName,  node_type= scalarConstantType)

    #proprieties
    scalarConstantNode.properties["val"] = node.outputs[0].default_value

    #single node, no internal connections
    internalConnections={
    }

    #ShaderNodeValue has no inbound connections
    inboundConnectors = {
       
    }

    outboundConnectors = {
        f"{node.bl_idname}:Value": f"{scalarConstantName}:out"
    }


    rsirGraph = RSIRGraph(
        uId=node.name,
        children=[scalarConstantNode],
        internalConnections=internalConnections,
        inboundConnectors=inboundConnectors,
        outboundConnectors=outboundConnectors
    )

    return rsirGraph

