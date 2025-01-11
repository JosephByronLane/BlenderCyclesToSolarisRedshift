from .nodeRegistry import registerNode

from ..data.RSIRGraph import RSIRGraph 
from ..data.RSIRNode import RSIRNode

from ..utils.uniqueDict import generateNodeName
from ..utils.redshiftPrefix import prefixRedhisftNode

@registerNode('ShaderNodeHueSaturation')
def defineShaderNodeHueSaturation(node, errors, parsedNodes):

    graphChildren =[]

    #raw strings of nodes
    hueSaturationString = "RSColorCorrection"
    colorMixString = "RSColorMix"
    #generate names
    hueSaturationName= generateNodeName(hueSaturationString)
    colorMixName= generateNodeName(colorMixString)
    #make the redshift type names
    hueSaturationType = prefixRedhisftNode(hueSaturationString)
    colorMixType = prefixRedhisftNode(colorMixString)
     #make the redshift type nodes
    hueSaturationNode = RSIRNode(node_id=hueSaturationName,  node_type= hueSaturationType)
    colorMixNode = RSIRNode(node_id=colorMixName,  node_type= colorMixType)

    #proprieties

    #blenders hue shift is 0-1 while redshifts is degrees (0-360)
    #so we need to convert the blender default (.5) to redshift default (0)

    colorMixNode.properties["mixAmount"] = node.inputs["Fac"].default_value

    RSHueValue = (node.inputs["Hue"].default_value -.5 ) * 360

    hueSaturationNode.properties["hue"] = RSHueValue
    hueSaturationNode.properties["saturation"] = node.inputs["Saturation"].default_value
    hueSaturationNode.properties["level"] = node.inputs["Value"].default_value

    internalConnections={
        f"{hueSaturationName}:outColor": f"{colorMixName}:input1",
    }

    #TODO: if a gamma node is added before/after this node, merge them together. RSColorCorrection has a gamma slider
    inboundConnectors = {
        f"{node.bl_idname}:Color": f"{hueSaturationName}:input&&{colorMixName}:input2",
        f"{node.bl_idname}:Hue": f"{hueSaturationName}:hue",
        f"{node.bl_idname}:Saturation": f"{hueSaturationName}:saturation",
        f"{node.bl_idname}:Value": f"{hueSaturationName}:level",
        f"{node.bl_idname}:Fac": f"{colorMixName}:mixAmount"
    }

    outboundConnectors = {
        f"{node.bl_idname}:Color": f"{colorMixName}:outColor"
    }

    graphChildren.append(hueSaturationNode)
    graphChildren.append(colorMixNode)

    rsirGraph = RSIRGraph(
        uId=node.name,
        children=graphChildren,
        internalConnections=internalConnections,
        inboundConnectors=inboundConnectors,
        outboundConnectors=outboundConnectors
    )
    parsedNodes.append(node.name)

    return rsirGraph

