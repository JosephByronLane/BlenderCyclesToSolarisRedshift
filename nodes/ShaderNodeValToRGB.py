from .nodeRegistry import registerNode

from ..data.RSIRGraph import RSIRGraph 
from ..data.RSIRNode import RSIRNode

from ..utils.uniqueDict import generateNodeName
from ..utils.redshiftPrefix import prefixRedhisftNode

@registerNode('ShaderNodeValToRGB')
def defineShaderNodeValToRGB(node, errors):

    #raw strings of nodes
    rampString = "RSRamp"

    #generate names
    rampName= generateNodeName(rampString)

    #make the redshift type names
    rampType = prefixRedhisftNode(rampString)

     #make the redshift type nodes
    rampNode = RSIRNode(node_id=rampName,  node_type= rampType)

    #proprieties
    colorRamp = node.color_ramp
    stops = []
    for elt in colorRamp.elements:
        stops.append({
            "position": elt.position,
            "color": tuple(elt.color)[:3],  # RGB, Redshift Ramp doesnt support alpha
        })

    rampNode.properties["ramp"] = {}
    
    rampNode.properties["ramp"]["interpolation"] = colorRamp.interpolation
    rampNode.properties["ramp"]["stops"] = stops
    
    #single node, no internal connections
    internalConnections={
    }


    inboundConnectors = {
       f"{node.bl_idname}:Fac": f"{rampName}:input"
    }

    outboundConnectors = {
        f"{node.bl_idname}:Color": f"{rampName}:outColor"
    }

    if node.outputs["Alpha"].is_linked:
        errors.append(f"Alpha output not supported on node: {node.name}. Will be ignored.")

    rsirGraph = RSIRGraph(
        uId=node.name,
        children=[rampNode],
        internalConnections=internalConnections,
        inboundConnectors=inboundConnectors,
        outboundConnectors=outboundConnectors
    )

    return rsirGraph

