from .nodeRegistry import registerNode

from ..data.RSIRGraph import RSIRGraph 
from ..data.RSIRNode import RSIRNode

from ..utils.uniqueDict import generateNodeName
from ..utils.redshiftPrefix import prefixRedhisftNode

@registerNode('NodeReroute')
def defineNodeReroute(node, errors, parsedNodes):

    #raw strings of nodes
    rerouteString = "__dot"

    #generate names
    rerouteName= generateNodeName(rerouteString)

    #generate nodes

    #tecnically we dont need the node type since it will be called with the generic matNode.createNetworkDot in the houdini parser
    rerouteNode = RSIRNode(node_id=rerouteName,  node_type= rerouteString)

    #no proprieties since its a network dot/reroute

    #sigle node, no internal connections
    internalConnections={
        
    }

    
    inboundConnectors = {
       f"{node.bl_idname}:Input": f"{rerouteName}:input"
    }

    outboundConnectors = {
        f"{node.bl_idname}:Output": f"{rerouteName}:output"
    }


    rsirGraph = RSIRGraph(
        uId=node.name,
        children=[rerouteNode],
        internalConnections=internalConnections,
        inboundConnectors=inboundConnectors,
        outboundConnectors=outboundConnectors
    )
    parsedNodes.append(node.name)

    return rsirGraph

