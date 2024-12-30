class IRNode:
    def __init__(self, node_id, node_type):
        self.id = node_id
        self.type = node_type
        self.properties = {}     # key-value for node-specific params
        self.connections = {}    

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "properties": self.properties,
            "connections": self.connections
        }