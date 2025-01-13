from .nodeRegistry import registerNode

from ..data.RSIRGraph import RSIRGraph 
from ..data.RSIRNode import RSIRNode

from ..utils.uniqueDict import generateNodeName
from ..utils.redshiftPrefix import prefixRedhisftNode

@registerNode('ShaderNodeInvert')
def defineShaderNodeInvert(node, errors, parsedNodes):

    #raw strings of nodes
    invertString = "RSMathInvColor"
    mixString = "RSColorMix"

    #generate names
    invertName= generateNodeName(invertString)
    mixName= generateNodeName(mixString)

    #make the redshift type names
    invertType = prefixRedhisftNode(invertString)
    mixType = prefixRedhisftNode(mixString)

     #make the redshift type nodes
    invertNode = RSIRNode(node_id=invertName,  node_type= invertType)
    mixNode = RSIRNode(node_id=mixName,  node_type= mixType)


    #proprieties
    mixNode.properties["mixAmount"] = node.inputs["Fac"].default_value
    invertNode.properties["input"] = tuple(node.inputs["Color"].default_value)

    internalConnections={
        f"{invertName}:outColor": f"{mixName}:input1",
        }


    inboundConnectors = {
       f"{node.bl_idname}:Color": f"{invertName}:input&&{mixName}:input2",
       f"{node.bl_idname}:Fac": f"{mixName}:mixAmount"
    }

    outboundConnectors = {
        f"{node.bl_idname}:Color": f"{mixName}:outColor"
    }


    rsirGraph = RSIRGraph(
        uId=node.name,
        children=[invertNode, mixNode],
        internalConnections=internalConnections,
        inboundConnectors=inboundConnectors,
        outboundConnectors=outboundConnectors
    )
    parsedNodes.append(node.name)

    return rsirGraph

