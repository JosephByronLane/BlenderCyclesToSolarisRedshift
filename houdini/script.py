import hou
import json
import os, stat

def import_rsir_json(filepath, matlibNode=None):
    """Creates redshift nodes based on input json data

    :param filepath: file path containing the JSON RSIRGraph data
    :type filepath: str
    :param matlibNode: material library node to create the new material in
    :type matlibNode: hou.Node
    :raises RuntimeError: Material library node not found
    """
    if matlibNode is None:
        raise RuntimeError("Error getting material library node")

    
    # Read JSON
    with open(filepath, 'r') as f:
        rsirGraphs = json.load(f)  

    matname = filepath.split("/")[-1].split(".")[0]
    parent_node = matlibNode.createNode('rs_usd_material_builder', node_name=matname)

    created_nodes = {}
    
    #before we do anything we delete the existing standardMaterial and redshift_usd_material nodes
    #since we will be creating our own nodes
    existingStandardMaterialNode = parent_node.node("StandardMaterial1")
    exitinggRedshiftUsdMaterialNode = parent_node.node("redshift_usd_material1")

    if existingStandardMaterialNode:            
            existingStandardMaterialNode.destroy()

    if exitinggRedshiftUsdMaterialNode:
        exitinggRedshiftUsdMaterialNode.destroy()


    for graph in rsirGraphs:

        #first we create the RS Nodes based on the RSIRGraph children
        
        children = graph["children"]

        for child in children:
            nodeType = child["type"]
            nodeName = child["id"]
            nodeProps = child["properties"]
            print("-----------------------------------------------------")
            print(f"Creating node: {nodeName} of type {nodeType}")
            createdNode = parent_node.createNode(nodeType, node_name=nodeName)
            for name, value in nodeProps.items():
                try:
                    if isinstance(value, (list, tuple)) and len(value) == 4:
                        parm = createdNode.parmTuple(name)
                        if parm:
                            parm.set(value)
                        else:
                            print(f"Parameter '{name}' not found on node '{nodeName}'.")
                    else:
                        parm = createdNode.parm(name)
                        if parm:
                            parm.set(value)
                        else:
                            print(f"Parameter '{name}' not found on node '{nodeName}'.")
                            
                except Exception as e:
                    print(f"Failed to set parameter '{name}' on node '{nodeName}': {e}")
            
        #after graph the child nodes, we wire them up
        internalConnections = graph["internalConnections"]
        print("************")
        print("Connecting nodes")   
        
        for connection in internalConnections:
            try:    
                nodeMakingConnectionName = connection.split(":")[0]
                nodeMakingConnectionOutoutSocker = connection.split(":")[1]
                print(f"Node making connection: {nodeMakingConnectionName} and output socket: {nodeMakingConnectionOutoutSocker} ")

                nodeTakingConnectionName = internalConnections[connection].split(":")[0]
                nodeTakingConnectingInputSocket = internalConnections[connection].split(":")[1]
                print(f"Node taking input: {nodeTakingConnectionName} and input socket: {nodeTakingConnectingInputSocket} ")


                #TODO: use pyside to make panels to check if user wants to import into stage or /mat/
                nodeTakingConnection = hou.node(f"/stage/{matlibNode.name()}/{matname}/{nodeTakingConnectionName}")
                if nodeTakingConnection is None:
                    raise NodeNotfoundError(f"Node {nodeTakingConnectionName} not found in the graph")


                nodeMakingInputConnection = hou.node(f"/stage/{matlibNode.name()}/{matname}/{nodeMakingConnectionName}")


                #setNamedInput("refl_roughness", inputNode, "outColor")
                print(f"{nodeTakingConnection.name()}, {nodeTakingConnectingInputSocket}, {nodeMakingInputConnection.name()}, {nodeMakingConnectionOutoutSocker} ")
                nodeTakingConnection.setNamedInput(nodeTakingConnectingInputSocket, nodeMakingInputConnection, nodeMakingConnectionOutoutSocker)
                print("#########")
            except Exception as e:
                print(f"Error connecting nodes: {e}")


    parent_node.layoutChildren()
    matlibNode.layoutChildren()

    print(f"Imported {len(created_nodes)} IR nodes into {parent_node.path()}")

def has_hidden_attribute(filepath):
    return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)

def autoDetectFolder(autoDetectDrive='H:/'):
    try: 
        if not os.path.exists(autoDetectDrive):
            raise Exception("Auto Detect directory doesn't exist") 
    
        visible_folders = []
        
        for entry in os.listdir(autoDetectDrive):
            full_path = os.path.join(autoDetectDrive, entry)
            if not has_hidden_attribute(full_path) and os.path.isdir(full_path):
                visible_folders.append(full_path)
        
        if not visible_folders:
            raise Exception( "No visible folders found in H: drive.")
        
        #select the first folder, since there should one be one ($ACTIVE) 
        selected_folder = visible_folders[0]
        return selected_folder
    
    except Exception as e:
        raise Exception(f"Error during auto-detection: {e}")

def findAllJson(projectDirectory):
    foundFiles=[]
    for root, dirs, files in os.walk(projectDirectory + '/tex/'):
    # select file name
        for file in files:
            # check the extension of files
            if file.endswith('.json'):
                foundFiles.append(os.path.join(root, file))

    return foundFiles

projectFolder = autoDetectFolder()
jsonFiles = findAllJson(projectFolder)
stage = hou.node("/stage")
if not stage:
    raise RuntimeError("Could not find /stage!")  

# #before creating a new node we delete the old one if it exists
# existingMatLibNode = stage.node("RuneMatLib")
# if existingMatLibNode:            
#     existingMatLibNode.destroy()

matlibNode = stage.createNode('materiallibrary', node_name='RuneMatLib')

for file in jsonFiles:
    import_rsir_json(file, matlibNode)

