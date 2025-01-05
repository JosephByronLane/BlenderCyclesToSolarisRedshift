class RSIRNode:
    """
    Redshift Intermediary Representation Node.
    This represents one Redshift node.
    """
    def __init__(self, node_id, node_type):
        self.id = node_id
        self.type = node_type
        self.properties = {}    

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "properties": self.properties,
        }