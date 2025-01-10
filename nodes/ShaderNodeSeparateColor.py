from .nodeRegistry import registerNode

from ..data.RSIRGraph import RSIRGraph 
from ..data.RSIRNode import RSIRNode

from ..utils.uniqueDict import generateNodeName
from ..utils.redshiftPrefix import prefixRedhisftNode

@registerNode('ShaderNodeSeparateColor')
def defineShaderNodeSeparateColor(node, errors):

    graphChildren = []

    #raw strings of nodes
    separateColorString = "RSColorSplitter"

    #might of might not be used d depending on the configuration of the node
    colorToHSLString = "RSColor2HSV"



    #generate names
    separateColorName= generateNodeName(separateColorString)

    #might of might not be used d depending on the configuration of the node
    colorToHSLName= generateNodeName(colorToHSLString)


    #make the redshift type names
    separateColorType = prefixRedhisftNode(separateColorString)

    #might of might not be used d depending on the configuration of the node
    colorToHSLType = prefixRedhisftNode(colorToHSLString)


     #make the redshift type nodes
    separateColorNode = RSIRNode(node_id=separateColorName,  node_type= separateColorType)

    #might of might not be used d depending on the configuration of the node
    colorToHSLNode = RSIRNode(node_id=colorToHSLName,  node_type= colorToHSLType)



    #proprieties
    separateColorNode.properties["input"] = tuple(node.inputs["Color"].default_value) 



    internalConnections={     

    }
    if node.mode== 'HSL':
        errors.append(f"HSL mode not supported on node: {node.name}. Will default to HSV")


    if node.mode == 'HSL' or node.mode == 'HSV':
        internalConnections[f"{colorToHSLName}:outColor"] = f"{separateColorName}:input"


        

    inboundConnectors = {
    
    
    }

    if node.mode=='HSL' or node.mode=='HSV':
        inboundConnectors[f"{node.bl_idname}:Color"] = f"{colorToHSLName}:input"
    else:
        inboundConnectors[f"{node.bl_idname}:Color"] = f"{separateColorName}:input"
                          


    if node.mode == 'RGB':
        outboundConnectors = {
            f"{node.bl_idname}:Red": f"{separateColorName}:outR",
            f"{node.bl_idname}:Green": f"{separateColorName}:outG",
            f"{node.bl_idname}:Blue": f"{separateColorName}:outB",
        }
    elif node.mode == 'HSV':
        outboundConnectors = {
            f"{node.bl_idname}:Red": f"{separateColorName}:outR",
            f"{node.bl_idname}:Green": f"{separateColorName}:outG",
            f"{node.bl_idname}:Blue": f"{separateColorName}:outB",
        }
    elif node.mode == 'HSL':
        outboundConnectors = {
            #???? for some reason the HSL output nodes are RGB rather than HSL
            f"{node.bl_idname}:Red": f"{separateColorName}:outR",
            f"{node.bl_idname}:Green": f"{separateColorName}:outG",
            f"{node.bl_idname}:Blue": f"{separateColorName}:outB",
        }




    if node.mode == 'HSL' or node.mode == 'HSV':
        graphChildren.append(colorToHSLNode)

    graphChildren.append(separateColorNode)

    rsirGraph = RSIRGraph(
        uId=node.name,
        children=graphChildren,
        internalConnections=internalConnections,
        inboundConnectors=inboundConnectors,
        outboundConnectors=outboundConnectors
    )

    return rsirGraph

