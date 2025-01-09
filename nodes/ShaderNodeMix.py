from .nodeRegistry import registerNode

from ..data.RSIRGraph import RSIRGraph 
from ..data.RSIRNode import RSIRNode

from ..utils.uniqueDict import generateNodeName
from ..utils.redshiftPrefix import prefixRedhisftNode
@registerNode('ShaderNodeMix')
def defineMixNode(node, errors):

    #is used for the factor on the vector mix
    isNonUniform = False

    mixString="RSColorMix"
    clampResultString= "RSColorRange"
    clampFactorString = "RSMathRange"

    #a list of all the children that the RSIRGraph will need
    graphChildren = []

    #we figure out exactly what time of mix it is
    if node.data_type == 'FLOAT':
        mixString = 'RSMathMix'
        clampResultString = "RSMathRange"

    elif node.data_type == 'RGBA':
        clampResultString = "RSColorRange"
        mixString = 'RSColorMix'

    elif node.data_type == 'VECTOR':
        clampResultString = "RSMathRangeVector"
        mixString = 'RSMathMixVector'
        if node.factor_mode == 'NON_UNIFORM':
            isNonUniform = True
            clampFactorString = "RSMathRangeVector"

    elif node.data_type == 'ROTATION':
        #only used in geometry nodes, if you manage to get this error you are a god
        errors.append(f"Rotation data type not supported on node: {node.name} will default to Vector")
        mixString = 'RSVectorMix'

    else:
        errors.append(f"Data type not supported on node: {node.name} will default to RGBA")
        mixString = 'RSmix'
    

    #we generate names
    mixName= generateNodeName(mixString)

    #might or might not be used d depending on the configuration of the node
    colorCompositeName = generateNodeName("RSColorComposite")
    clampResultName= generateNodeName(clampResultString)
    clampFactorName= generateNodeName(clampFactorString)

    #we make the redshift type nodes

    mixType = prefixRedhisftNode(mixString)

    #might or might not be used d depending on the configuration of the node
    colorCompositeType = prefixRedhisftNode("RSColorComposite")
    clampResultType = prefixRedhisftNode(clampResultString)
    clampFactorType = prefixRedhisftNode(clampFactorString)


    #we generate the RSIR nodes
    mixNode = RSIRNode(node_id=mixName,  node_type= mixType)

    #these nodes might or might not be used depending on what configuration the node is in
    colorCompositeNode = RSIRNode(node_id=colorCompositeName,  node_type= colorCompositeType)
    clampResultNode = RSIRNode(node_id=clampResultName,  node_type= clampResultType)
    clampFactorNode = RSIRNode(node_id=clampFactorName,  node_type= clampFactorType)


    #we set the mix node proprieties 
    #NOTE: We dont need to set clamp proprieties since by default their values are mapped to 0-1

    inputA = node.inputs["A"].default_value
    inputB = node.inputs["B"].default_value

    if node.data_type in ('RGBA', 'VECTOR'):
        #we make tuples since theyre 4 values (RGBA) or 3 (XYZ)
        if node.blend_type == "MIX" or node.data_type == 'VECTOR':
            #meaning it 
            mixNode.properties["input1"] = tuple(inputA)
            mixNode.properties["input2"] = tuple(inputB)
        else:
            colorCompositeNode.properties["base_color"] = tuple(inputA)
            colorCompositeNode.properties["blend_color"] = tuple(inputB)
    else:
        mixNode.properties["input1"] = inputA
        mixNode.properties["input2"] = inputB
   
    #we cant directly set the factor value since the RSColorComposite doesn't have a mix factor.
    #we could switch to a RSColorLayer but that would be a bit overkill since we'd have 7 empty inputs.
    #TODO: make this scale so that if it detects many ShaderNodeMix with composite type it switches to RSColorLayer

    if node.data_type == "VECTOR":
        if (isNonUniform):
            mixNode.properties["mixAmount"] = tuple(node.inputs["Factor"].default_value)
        else:
            default_val = node.inputs["Factor"].default_value
            mixNode.properties["mixAmount"] = (default_val, default_val, default_val)
    else:
        mixNode.properties["mixAmount"] = node.inputs["Factor"].default_value


    #then we set the composite node's color proprieties if the node isn't in mix mode
     #composite nodes
    if node.blend_type != 'MIX' and node.data_type == 'RGBA':
        if node.blend_type == 'DARKEN':
            blendType = "8"
        elif node.blend_type == 'MULTIPLY':
            blendType = "5"
        elif node.blend_type == 'BURN':
            blendType = "12"
            
        elif node.blend_type == 'LIGHTEN':
            blendType = "7"
        elif node.blend_type == 'SCREEN':
            blendType = "9"
        elif node.blend_type == 'DODGE':
            blendType = "13"
        elif node.blend_type == 'ADD':
            blendType = "3"

        elif node.blend_type == 'OVERLAY':
            blendType = "14"
        elif node.blend_type == 'SOFT_LIGHT':
            blendType = "11"
        #linear light doesn't exist in redshift

        elif node.blend_type == 'DIFFERENCE':
            blendType = "6"
        elif node.blend_type == 'EXCLUSION':
            blendType = "15"
        elif node.blend_type == 'SUBTRACT':
            blendType = "4"
        elif node.blend_type == 'DIVIDE':
            blendType = "16"

        #hue doesnt exist in redshift
        #saturation doesnt exist in redshift
        #color doesnt exist in redshift
        #value doesnt exist in redshift lmao what the fuck

        #TODO: custom hsl????

        else:
            errors.append(f"Blend type on node: {node.name} is not supported. Will default to Screen")
            blendType ="9"     

        colorCompositeNode.properties["comp_mode"] = blendType



    #we wire up the internal graph connections.

    #these are a bit of a mess since they depend wether  we clamp the input, output, or if its a composite node
    # if its a composite node we'll need a intermediary RScolorComposite node to on the input1

    internalConnections = {}

    if node.clamp_factor:
        #we can hardcode here because we will either use a MathRangeVector or a MathRange(float) which both have 'out' as the output name
        #we will never use the RSColorMix as theclamp for the factor.
        #the clamp for the result however, is another story lmao
        internalConnections[f"{clampFactorName}:out"] = f"{mixName}:mixAmount"

    mixOutputSocketName = 'outColor' if node.data_type == 'RGBA' else 'out'

    if node.clamp_result:
        internalConnections[f"{mixName}:{mixOutputSocketName}"] = f"{clampResultName}:input"

    if node.blend_type != 'MIX' and node.data_type == 'RGBA':
        internalConnections[f"{colorCompositeName}:outColor"] = f"{mixName}:input1"
   
    inboundConnectors = {  
    }

    if node.clamp_factor:
        inboundConnectors[f"{node.bl_idname}:Factor"] = f"{clampFactorName}:input"
    else:
        inboundConnectors[f"{node.bl_idname}:Factor"] = f"{mixName}:mixAmount"

    if node.blend_type != 'MIX' and node.data_type == 'RGBA':
        inboundConnectors[f"{node.bl_idname}:A"] = f"{colorCompositeName}:base_color"
        inboundConnectors[f"{node.bl_idname}:B"] = f"{colorCompositeName}:blend_color&&{mixName}:input2"

    else:
        inboundConnectors[f"{node.bl_idname}:A"] = f"{mixName}:input1"
        inboundConnectors[f"{node.bl_idname}:B"] = f"{mixName}:input2"


    #setting outbound conectors
    outboundConnectors = {}

    if node.clamp_result:    
        outboundConnectors[f"{node.bl_idname}:Result"] =  f"{clampResultName}:{mixOutputSocketName}"

    else:
        outboundConnectors[f"{node.bl_idname}:Result"] =f"{mixName}:{mixOutputSocketName}"


    #we add the children to the graphlist

    if node.clamp_result:
        graphChildren.append(clampResultNode)
    
    if node.clamp_factor:
        graphChildren.append(clampFactorNode)

    if node.blend_type != 'MIX' and node.data_type == 'RGBA':
        graphChildren.append(colorCompositeNode)

    graphChildren.append(mixNode)

    rsirGraph = RSIRGraph(
        uId=node.name,
        children=graphChildren,
        internalConnections=internalConnections,
        inboundConnectors=inboundConnectors,
        outboundConnectors=outboundConnectors
    )

    return rsirGraph

