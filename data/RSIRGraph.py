from .RSIRNode import RSIRNode 

class RSIRGraph:
    """
    Redshift Intermediary Representation Graph. Graph holding all the information necesary to generate Redshift Nodes.
    """
    def __init__(
        self,
        uId,
        children,
        internalConnections,
        inboundConnectors,
        outboundConnectors,
        inputConnections=None
    ):
        """
        Initialize a new RSIRGraph.
        :param uId: Unique identifier for this RSIRGraph. Should be native Blender Node Name (node.name).
        :type uId: str

        :param children: List of RSIRNodes that are children of this RSIRGraph.
        :type children: list<RSIRNode>

        :param internalConnections: Dictionary of internal connections between RSIRNodes. Manually input.
        :type internalConnections: dict{str (RSNodeNameOutput: outputFieldName): str (RSNodeNameInput: inputFieldName)}

        :param inboundConnectors: Dictionary of inbound connectors. Manually input.
        :type inboundConnectors: dict{str (BlenderNodeBl_IdName:inputFieldName): str (RSNodeName:inputFieldName)}

        :param outboundConnectors: Dictionary of outbound connectors. These are generated by the script.
        :type outboundConnectors: dict{str (BlenderNodeBl_IdName:outputField): str (RSNodeName:outputField)}

        :param inputConnections: Dictionary of input connections. These are generated by the script.
        """   

        self.uId = uId        

        if not isinstance(children, list) and all(isinstance(item, RSIRNode) for item in children):
            raise ValueError("Children must be a list of RSIRNodes")

        self.children = children # List of RSIRNodes

        #We define internal connections, we can use pure RS nodes here because  this is going directly to the houdini parser, blender side doesn't touch it.
        self.internalConnections = internalConnections 

        # these do need to be translated, as they're used for setting up the connections for the parser.
        self.inboundConnectors = inboundConnectors

        #same here
        self.outboundConnectors = outboundConnectors

        # These are in RS nodes, since they're pased to the houdini parser.
        # 
        # To find these connectors, its going to query the blender node and ask:
        # "Hey, I see you are connected to my ShaderNodeMix input A through your Texture1 color output,
        # My actual ShaderNodeMix input A is actually inboundConnectors["ShaderNodeMix:A"] (RScolorMix1:input1), and I see your Texture1 color output is actually inputNode.outboundConnectors["Texture1:Color"] (RSColorMaker1:outColor)
        # and so it writes them for the parser.
        self.inputConnections = inputConnections or {}

    def __getitem__(self, uId):
        """
        Allows querying the RSIRGraph by uId using square brackets.
        """
        if uId == self.uId:
            return self


    def to_dict(self): 
        """Turns the RSIRGraph into a dictionary.

        :return: Dictionary representation of the RSIRGraph.
        :rtype: dict
        """



        childrenJson = [n.to_dict() for n in self.children]            
        print("Serializing RSIRGraph children")
        return {
            "uId": self.uId,
            "children": childrenJson,
            "internalConnections": self.internalConnections,
            "inboundConnectors": self.inboundConnectors,
            "outboundConnectors": self.outboundConnectors,
            "inputConnections": self.inputConnections
        }


