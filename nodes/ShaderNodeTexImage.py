from .nodeRegistry import registerNode

from ..data.RSIRGraph import RSIRGraph 
from ..data.RSIRNode import RSIRNode

from ..utils.uniqueDict import generateNodeName
from ..utils.redshiftPrefix import prefixRedhisftNode
@registerNode('ShaderNodeTexImage')
def defineImageTexture(node, errors):

    texSamplerString = "TextureSampler"
    colorSplitterString = "RSColorSplitter"
    colorMakerString = "RSColorMaker"

    texSamplerName= generateNodeName(texSamplerString)
    colorSplitterName= generateNodeName(colorSplitterString)
    colorMakerName= generateNodeName(colorMakerString)

    texSamplerNode = RSIRNode(node_id=texSamplerName,  node_type= prefixRedhisftNode(texSamplerString))
    colorSplitterNode = RSIRNode(node_id=colorSplitterName,  node_type= prefixRedhisftNode(colorSplitterString))
    colorMakerNode = RSIRNode(node_id=colorMakerName,  node_type= prefixRedhisftNode(colorMakerString))

    texSamplerNode.properties["tex0"] = node.image.filepath
    
    #colorspace parameters
    if node.image.colorspace_settings.name != 'Non-Color' and  node.image.colorspace_settings.name != 'sRGB':
        errors.append(f"Color space not supported on node: {node.name} will default to sRGB")
        texSamplerNode.properties["tex0_colorSpace"] = "AgX Base sRGB"

    if node.image.colorspace_settings.name == 'Non-Color':
        texSamplerNode.properties["tex0_colorSpace"] = "Raw"

    if node.image.colorspace_settings.name == 'sRGB':
        texSamplerNode.properties["tex0_colorSpace"] = "AgX Base sRGB"

    internalConnections={
        f"{texSamplerName}:outColor": f"{colorSplitterName}:input",
        f"{colorSplitterName}:outR": f"{colorMakerName}:red",
        f"{colorSplitterName}:outG": f"{colorMakerName}:green",
        f"{colorSplitterName}:outB": f"{colorMakerName}:blue",
    }

    #NOTE: need to add truncation support of mapping node if it is connected to UV input in blender node
    # and map it to the RS Node's 'scale', 'offset', and 'rotation' inputs.
    inboundConnectors = {
       
    }

    outboundConnectors = {
        f"{node.bl_idname}:Color": f"{colorMakerName}:outColor" ,
        f"{node.bl_idname}:Alpha": f"{colorSplitterName}:outA" 
    }


    rsirGraph = RSIRGraph(
        uId=node.name,
        children=[texSamplerNode, colorSplitterNode, colorMakerNode],
        internalConnections=internalConnections,
        inboundConnectors=inboundConnectors,
        outboundConnectors=outboundConnectors
    )

    return rsirGraph

