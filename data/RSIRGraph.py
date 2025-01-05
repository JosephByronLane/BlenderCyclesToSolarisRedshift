class RSIRGraph:
    """
    Redshift Intermediary Representation Graph. Graph holding all the information necesary to generate Redshift Nodes.
    """
    def __init__(
        self,
        uId,
        children=None,
        internal_connections=None,
        inbound_connectors=None,
        outbound_connectors=None,
        input_connections=None
    ):
        """
        Initialize a new RSIRGraph.
        :param uId: Unique identifier for this RSIRGraph. Should be native Blender Node Name (node.name).
        :type uId: str
        :param children: List of RSIRNodes that are children of this RSIRGraph.
        :param internal_connections: Dictionary of internal connections between RSIRNodes.
        :param inbound_connectors: Dictionary of inbound connectors.
        :param outbound_connectors: Dictionary of outbound connectors.
        :param input_connections: Dictionary of input connections.
        """   

        self.uId = uId
        
        self.children = children or [] # List of RSIRNodes
        self.internal_connections = internal_connections or {}
        self.inbound_connectors = inbound_connectors or {}
        self.outbound_connectors = outbound_connectors or {}
        self.input_connections = input_connections or {}

    def to_dict(self): 
        """Turns the RSIRGraph into a dictionary.

        :return: Dictionary representation of the RSIRGraph.
        :rtype: dict
        """
        return {
            "uId": self.uId,
            "children": self.children,
            "internalConnections": self.internal_connections,
            "inboundConnectors": self.inbound_connectors,
            "outboundConnectors": self.outbound_connectors,
            "inputConnections": self.input_connections
        }


