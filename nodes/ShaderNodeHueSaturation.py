from .nodeRegistry import registerNode

from ..data.RSIRGraph import RSIRGraph 
from ..data.RSIRNode import RSIRNode

from ..utils.uniqueDict import generateNodeName
from ..utils.redshiftPrefix import prefixRedhisftNode

@registerNode('ShaderNodeHueSaturation')
def defineShaderNodeHueSaturation(node, errors, parsedNodes):

    #raw strings of nodes
    hueSaturationString = "RSColorCorrection"

    #generate names
    hueSaturationName= generateNodeName(hueSaturationString)

    #make the redshift type names
    hueSaturationType = prefixRedhisftNode(hueSaturationString)

     #make the redshift type nodes
    hueSaturationNode = RSIRNode(node_id=hueSaturationName,  node_type= hueSaturationType)


    #proprieties

    #blenders hue shift is 0-1 while redshifts is degrees (0-360)
    #so we need to convert the blender default (.5) to redshift default (0)

    RSHueValue = (node.inputs["Hue"].default_value -.5 ) * 360

    hueSaturationNode.properties["hue"] = RSHueValue
    hueSaturationNode.properties["saturation"] = node.inputs["Saturation"].default_value
    hueSaturationNode.properties["level"] = node.inputs["Value"].default_value

    internalConnections={
    }

    #TODO: if a gamma node is added before/after this node, merge them together. RSColorCorrection has a gamma slider
    inboundConnectors = {
       f"{node.bl_idname}:Color": f"{hueSaturationName}:input"
    }

    outboundConnectors = {
        f"{node.bl_idname}:Color": f"{hueSaturationName}:outColor"
    }


    rsirGraph = RSIRGraph(
        uId=node.name,
        children=[hueSaturationNode],
        internalConnections=internalConnections,
        inboundConnectors=inboundConnectors,
        outboundConnectors=outboundConnectors
    )
    parsedNodes.append(node.name)

    return rsirGraph

