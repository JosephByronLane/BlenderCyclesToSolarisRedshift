class Node:
    """All implemented nodes inherit from this."""
    bl_idname = None

    def expand(self, node, new_id):
        # must be overridden by child
        raise NotImplementedError()


