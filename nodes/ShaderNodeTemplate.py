from .nodeRegistry import registerNode

from ..data.RSIRGraph import RSIRGraph 
from ..data.RSIRNode import RSIRNode

from ..utils.uniqueDict import generateNodeName
from ..utils.redshiftPrefix import prefixRedhisftNode

@registerNode('ShaderNameHere')
def defineShaderName(node, errors):

    #raw strings of nodes
    exampleString = "asdf"

    #generate names
    texSamplerName= generateNodeName(texSamplerName)

    #make the redshift type names
    clampResultType = prefixRedhisftNode(texSamplerName)

     #make the redshift type nodes
    texSamplerNode = RSIRNode(node_id=texSamplerName,  node_type= clampResultType)

    #colorspace proprieties


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

    return rsirGraph

