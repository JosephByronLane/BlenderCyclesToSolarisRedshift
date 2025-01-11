from .nodeRegistry import registerNode

from ..data.RSIRGraph import RSIRGraph 
from ..data.RSIRNode import RSIRNode

from ..utils.uniqueDict import generateNodeName
from ..utils.redshiftPrefix import prefixRedhisftNode

@registerNode('ShaderNodeGamma')
def defineShaderNodeGamma(node, errors, parsedNodes):

    #raw strings of nodes
    gammaString = "RSColorCorrection"

    #generate names
    gammaName= generateNodeName(gammaString)

    #make the redshift type names
    gammaType = prefixRedhisftNode(gammaString)

     #make the redshift type nodes
    gammaNode = RSIRNode(node_id=gammaName,  node_type= gammaType)

    #proprieties
    gammaNode.properties["gamma"] = node.inputs["Gamma"].default_value
    gammaNode.properties["input"] = node.inputs["Color"].default_value  
    internalConnections={
    
    }


    inboundConnectors = {
        f"{node.bl_idname}:Color": f"{gammaName}:input",
        f"{node.bl_idname}:Gamma": f"{gammaName}:gamma"
    }

    outboundConnectors = {
        f"{node.bl_idname}:Color": f"{gammaName}:outColor"
    }


    rsirGraph = RSIRGraph(
        uId=node.name,
        children=gammaNode,
        internalConnections=internalConnections,
        inboundConnectors=inboundConnectors,
        outboundConnectors=outboundConnectors
    )
    parsedNodes.append(node.name)

    return rsirGraph

