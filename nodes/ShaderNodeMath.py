from .nodeRegistry import registerNode

from ..data.RSIRGraph import RSIRGraph 
from ..data.RSIRNode import RSIRNode

from ..utils.uniqueDict import generateNodeName
from ..utils.redshiftPrefix import prefixRedhisftNode

from ..utils.findOslShader import findOSLShaderDirectory

@registerNode('ShaderNodeMath')
def defineShaderNodeMath(node, errors, parsedNodes):

    graphChildren =[]

    isClamped = node.use_clamp

    #raw strings of nodes
    mathString = "RSMathAdd"
    aux1String = ""
    aux2String = ""
    clampString = "RSMathRange"

    isSingleInput = False
    isOSL = False

    if node.operation == 'ADD':
        mathString = "RSMathAdd"
    elif node.operation == 'SUBTRACT':
        mathString = "RSMathSub"
    elif node.operation == 'MULTIPLY':
        mathString = "RSMathMul"
    elif node.operation == 'DIVIDE':
        mathString = "RSMathDiv"
    # elif node.operation == 'MULTIPLY_ADD':
    #     mathString = "RSMathMul"
    #     aux1String = "RSMathAdd"
    
    elif node.operation == 'POWER':
        mathString = "RSMathPow"
    elif node.operation == 'LOGARITHM':
        mathString = "RSMathLog"
    elif node.operation == 'SQRT':
        mathString = "RSMathSqrt"
        isSingleInput = True
    elif node.operation == 'INVERSE_SQRT':
        mathString = "RSMathDiv"
        aux1String = "RSMathSqrt"    
        isSingleInput = True
    elif node.operation == "ABSOLUTE":        
        mathString = "RSMathAbs"
        isSingleInput = True
    elif node.operation == "EXPONENT":
        mathString = "RSMathExp"
        isSingleInput = True
    elif node.operation=="MINIMUM":
        mathString = "RSMathMin"
    elif node.operation=="MAXIMUM":
        mathString = "RSMathMax"
    
    elif node.operation=="LESS_THAN":
        isOSL = True
        mathString = "rsOSL"
        #TODO: IMPLEMENT CUSTOM OSL NODE. it can be done, i believe
    # elif node.operation=="GREATER_THAN":
    #     #TODO: IMPLEMENT CUSTOM OSL NODE. it can be done, i believe
    elif node.operation=="SIGN":
        mathString = "RSMathSign"
        isSingleInput = True

    # elif node.operation=="COMPARE":
    #     #TODO: IMPLEMENT CUSTOM OSL NODE. it can be done, i believe
    # elif node.operation=="SMOOTH_MIN":
    #     #TODO: IMPLEMENT CUSTOM OSL NODE. it can be done, i believe
    # elif node.operation=="SMOOTH_MAX":
    #     #TODO: IMPLEMENT CUSTOM OSL NODE. it can be done, i believe

    #ok we get it OSL node for all of remaining round: ROUND, CEIL, TRUNC
    elif node.operation =="FLOOR":
        isSingleInput = True
        mathString="RSMathFloor"  

    #same for FLOORED_MODULO, WRAP, SNAP, PINGPONG
    elif node.operation=="FRACT":
        isSingleInput = True
        mathString="RSMathFrac"
    elif node.operation=="MODULO":
        mathString="RSMathMod"

    elif node.operation=="SINE":
        isSingleInput = True
        mathString="RSMathSin"
    elif node.operation=="COSINE":
        isSingleInput = True
        mathString="RSMathCos"
    elif node.operation=="TANGENT":
        isSingleInput = True
        mathString="RSMathTan"

    elif node.operation=="ARCSINE":
        isSingleInput = True
        mathString="RSMathAsin"
    elif node.operation=="ARCCOSINE":
        isSingleInput = True
        mathString="RSMathAcos"
    elif node.operation=="ARCTANGENT":
        isSingleInput = True
        mathString="RSMathAtan"
    elif node.operation =="ARCTAN2":
        mathString="RSMathAtan2"
    else:
        errors.append(f"Node {node.name} has an unsupported operation: {node.operation}. Will default to ADD operation.")
        mathString = "RSMathAdd"
    #also implement all of the hyperbolic functions and conversions



    #generate names
    mathName= generateNodeName(mathString)
    aux1Name= generateNodeName(aux1String)
    aux2Name= generateNodeName(aux2String)
    clampName = generateNodeName(clampString)

    #make the redshift type names
    mathType = prefixRedhisftNode(mathString)
    aux1Type = prefixRedhisftNode(aux1String)
    aux2Type = prefixRedhisftNode(aux2String)
    clampType = prefixRedhisftNode(clampString)

    mathNode = RSIRNode(node_id=mathName,  node_type= mathType)
    aux1Node = RSIRNode(node_id=aux1Name,  node_type= aux1Type)
    aux2Node = RSIRNode(node_id=aux2Name,  node_type= aux2Type)
    clampNode = RSIRNode(node_id=clampName,  node_type= clampType)

    #proprieties
    if isSingleInput:
        mathNode.properties["input"] = node.inputs[0].default_value

    elif node.operation == "POWER":
        mathNode.properties["base"] = node.inputs[0].default_value
        mathNode.properties["exponent"] = node.inputs[1].default_value

    elif node.operation == "LOGARITHM":
        mathNode.properties["input"] = node.inputs[0].default_value
        mathNode.properties["base"] = node.inputs[1].default_value

    elif node.operation == "MODULO":
        mathNode.properties["input"] = node.inputs[0].default_value
        mathNode.properties["divisor"] = node.inputs[1].default_value

    elif node.operation == "ARCTAN2":
        mathNode.properties["x"] = node.inputs[0].default_value
        mathNode.properties["y"] = node.inputs[1].default_value

    elif isOSL:
        mathNode.properties["osl"] = {}
        mathNode.properties["osl"]["rs_osl_file"] = findOSLShaderDirectory(node.bl_idname, node.operation)
        mathNode.properties["osl"]["press_button"] = "0"
        mathNode.properties["osl"]["input1"] = node.inputs[0].default_value
        mathNode.properties["osl"]["input2"] = node.inputs[1].default_value

    
    else:
        mathNode.properties["input1"] = node.inputs[0].default_value
        mathNode.properties["input2"] = node.inputs[1].default_value



    internalConnections={

    }         

    if isClamped:
        internalConnections[f"{mathName}:out"] = f"{clampName}:input"

    inboundConnectors = {}
    
    if isSingleInput:
        inboundConnectors[f"{node.bl_idname}: {node.inputs[0].name}"] = f"{mathName}:input"

    elif node.operation == "POWER":
        inboundConnectors[f"{node.bl_idname}:Base"] = f"{mathName}:base"
        inboundConnectors[f"{node.bl_idname}:Exponent"] = f"{mathName}:exponent"


    elif node.operation == "LOGARITHM":
        inboundConnectors[f"{node.bl_idname}:Value"] = f"{mathName}:input"
        inboundConnectors[f"{node.bl_idname}:Base"] = f"{mathName}:base"


    elif node.operation == "MODULO":
        inboundConnectors[f"{node.bl_idname}:Value"] = f"{mathName}:input"
        inboundConnectors[f"{node.bl_idname}:Value_001"] = f"{mathName}:divisor"


    elif node.operation == "ARCTAN2":
        inboundConnectors[f"{node.bl_idname}:X"] = f"{mathName}:x"
        inboundConnectors[f"{node.bl_idname}:Y"] = f"{mathName}:y"

    elif node.operation == "LESS_THAN":
        inboundConnectors[f"{node.bl_idname}:Value"] = f"{mathName}:input1"
        inboundConnectors[f"{node.bl_idname}:Threshold"] = f"{mathName}:input2"

    else:
        inboundConnectors[f"{node.bl_idname}:Value"] = f"{mathName}:input1"
        inboundConnectors[f"{node.bl_idname}:Value_001"] = f"{mathName}:input2"


    outboundConnectors = {
    }

    if isClamped:
        outboundConnectors[f"{node.bl_idname}:Value"] = f"{clampName}:out"
    else:
        outboundConnectors[f"{node.bl_idname}:Value" : f"{mathName}:out"]



    graphChildren.append(mathNode)
    
    if isClamped:
        graphChildren.append(clampNode)

    rsirGraph = RSIRGraph(
        uId=node.name,
        children=graphChildren,
        internalConnections=internalConnections,
        inboundConnectors=inboundConnectors,
        outboundConnectors=outboundConnectors
    )
    parsedNodes.append(node.name)

    return rsirGraph

