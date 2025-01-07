from .nodeRegistry import registerNode

from ..data.RSIRGraph import RSIRGraph 
from ..data.RSIRNode import RSIRNode

from ..utils.uniqueDict import generateNodeName

@registerNode('ShaderNodeOutputMaterial')
def defineOutputMaterial(node, errors):

    redshiftNodeName = "redshift_usd_material"

    nodeName= generateNodeName(redshiftNodeName)

    #doesnt need redshift:: prefix for some fucking reason dont ask me why
    rsirNode = RSIRNode(node_id=nodeName,  node_type=redshiftNodeName)

    


    #single node, no internal connections
    internalConnections={

    }


    #NOTE  Thickness tecnically slider doesnt exist in Redshift to my knowledge.     
    #      might be t he depth parameter in the transmission tab? idk
    inboundConnectors = {
            f"{node.bl_idname}:Surface":                f"{nodeName}:Surface",
            f"{node.bl_idname}:Volume":                 f"{nodeName}:Volume",
            f"{node.bl_idname}:Displacement":           f"{nodeName}:Displacement",        
    }

    if node.inputs["Thickness"].is_linked:
        errors.append(f"Thickness input not supported on node: {node.name}")




    outboundConnectors = {
        f"{node.bl_idname}:BSDF": f"{nodeName}:outColor" 
    }


    rsirGraph = RSIRGraph(
        uId=node.name,
        children=[rsirNode],
        internalConnections=internalConnections,
        inboundConnectors=inboundConnectors,
        outboundConnectors=outboundConnectors
    )

    return rsirGraph

