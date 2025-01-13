NODE_REGISTRY = {}

def registerNode(bl_idname):
    """
    Decorator to register a node expander function with a specific Blender node type.
    Must be added above every node definition function.
    """
    def decorator(func):
        NODE_REGISTRY[bl_idname] = func
        return func
    return decorator

def getRegistry(bl_idname):
    """Retrieve the parser function for a given Blender node type."""
    return NODE_REGISTRY.get(bl_idname, None)