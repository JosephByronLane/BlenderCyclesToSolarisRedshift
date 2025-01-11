class RSIRNode:
    """
    Redshift Intermediary Representation Node.
    This represents one Redshift node.
    """
    def __init__(self, node_id, node_type):
        """Initializes a new RSIRNode.

        :param node_id: Unique identifier for this RSIRNode. Should be native Redshift Node Name + number of node.
        :type node_id: str
        :param node_type: The type of Redshift node this is.
        :type node_type: str
        """

        self.id = node_id
        self.type = node_type
        self.properties = {}    

    def to_dict(self):

        print(f"Serializing cild node {self.id}")

        return {
            "id": self.id,
            "type": self.type,
            "properties": self.properties,
        }
    
    counter = 1
    def new_id(node_type):
        RSIRNode.counter += 1
        return f"{node_type}{RSIRNode.counter}"