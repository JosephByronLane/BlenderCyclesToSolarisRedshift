UNIQUE_DICT = {}

def generateNodeName(nodeId=None):
    if UNIQUE_DICT.get(nodeId) is None:
        UNIQUE_DICT[nodeId] = 1
        return f"{nodeId}" + f"{UNIQUE_DICT[nodeId]}"
    else:
        UNIQUE_DICT[nodeId] += 1
        return f"{nodeId}" + f"{UNIQUE_DICT[nodeId]}"