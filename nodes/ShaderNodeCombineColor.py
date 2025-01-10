from .nodeRegistry import registerNode

from ..data.RSIRGraph import RSIRGraph 
from ..data.RSIRNode import RSIRNode

from ..utils.uniqueDict import generateNodeName
from ..utils.redshiftPrefix import prefixRedhisftNode

@registerNode('ShaderNodeCombineColor')
def defineShaderNodeCombineColor(node, errors):

    graphChildren = []


    #raw strings of nodes
    combineColorString = "RSColorMaker"

    hsvToColorString = "RSHSV2Color"

    #generate names
    combineColorName= generateNodeName(combineColorString)
    hsvToColorName= generateNodeName(hsvToColorString)

    #make the redshift type names
    combineColorType = prefixRedhisftNode(combineColorString)
    hsvToColorType = prefixRedhisftNode(hsvToColorString)

     #make the redshift type nodes
    combineColorNode = RSIRNode(node_id=combineColorName,  node_type= combineColorType)
    hsvToColorNode = RSIRNode(node_id=hsvToColorName,  node_type= hsvToColorType)

    #proprieties
    combineColorNode.properties["red"] = node.inputs["Red"].default_value
    combineColorNode.properties["green"] = node.inputs["Green"].default_value
    combineColorNode.properties["blue"] = node.inputs["Blue"].default_value
    combineColorNode.properties["alpha"] = 1

    internalConnections={

    }
    if node.mode !=  "RGB":
        internalConnections[ f"{combineColorName}:color"] = f"{hsvToColorName}:outColor"


    inboundConnectors = {
       f"{node.bl_idname}:Red": f"{combineColorName}:red",
       f"{node.bl_idname}:Green": f"{combineColorName}:green",
       f"{node.bl_idname}:Blue": f"{combineColorName}:blue"
    }

    outboundConnectors = {

    }

    if node.mode != "RGB":
        outboundConnectors[f"{node.bl_idname}:Color"] = f"{hsvToColorName}:outColor"

    if node.mode == "RGB":
        outboundConnectors[f"{node.bl_idname}:Color"] = f"{combineColorName}:outColor"



    #errors
    if node.mode=="HSL":
        errors.append(f"HSL mode not supported on node: {node.name}. Will default to HSV")

    if node.mode != "RGB":
        graphChildren.append(hsvToColorNode)

    graphChildren.append(combineColorNode)

    rsirGraph = RSIRGraph(
        uId=node.name,
        children=graphChildren,
        internalConnections=internalConnections,
        inboundConnectors=inboundConnectors,
        outboundConnectors=outboundConnectors
    )

    return rsirGraph

