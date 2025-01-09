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

    try:
        existingStandardMaterialNode = parent_node.node("StandardMaterial1")
        exitinggRedshiftUsdMaterialNode = parent_node.node("redshift_usd_material1")
        if existingStandardMaterialNode:            
            existingStandardMaterialNode.destroy()

        if exitinggRedshiftUsdMaterialNode:
            exitinggRedshiftUsdMaterialNode.destroy()

    except Exception as e:
        print(f"Error deleting existing nodes: {e}")


    for graph in rsirGraphs:

        #first we create the RS Nodes based on the RSIRGraph children
        
        children = graph["children"]
        print("******************************************************")
        print("Creating individual graphs")   

        for child in children:
            try:
                nodeType = child["type"]
                nodeName = child["id"]
                nodeProps = child["properties"]
            except Exception as e:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(f"Error finding proprieties: {e}")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            
            print("-----------------------------------------------------------")
            print(f"Creating node: {nodeName} of type {nodeType} on graph {graph['uId']}")

            try:
                createdNode = parent_node.createNode(nodeType, node_name=nodeName)
            except Exception as e:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(f"Error creating node {nodeType}: {e}")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

            for name, value in nodeProps.items():
                try:
                    print(f"Setting parameter '{name}' to '{value}' on node '{nodeName}'")
                    if isinstance(value, (list, tuple)) and len(value) > 1:
                        parm = createdNode.parmTuple(name)
                        if parm is not None:
                            parm.set(value)
                        else:
                            raise Exception(f"Tuple parameter '{name}' not found on node '{nodeName}'.")

                    else:
                        parm = createdNode.parm(name)
                        if parm is not None:
                            parm.set(value)
                        else:
                            raise Exception(f"Float parameter '{name}' not found on node '{nodeName}'.")

                except Exception as e:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print(f"Failed to set parameter '{name}' on node '{nodeName}': {e}")
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        #after graph the child nodes, we wire the individual graphs up
        internalConnections = graph["internalConnections"]
        print("******************************************************")
        print("Wiring individual graphs")   
        
        for connection in internalConnections:
            try:    
                print("##############################################################")
                nodeMakingConnectionName = connection.split(":")[0]
                nodeMakingConnectionOutoutSocker = connection.split(":")[1]
                print(f"Node making connection: {nodeMakingConnectionName} and output socket: {nodeMakingConnectionOutoutSocker} ")

                nodeTakingConnectionName = internalConnections[connection].split(":")[0]
                nodeTakingConnectingInputSocket = internalConnections[connection].split(":")[1]
                print(f"Node taking input: {nodeTakingConnectionName} and input socket: {nodeTakingConnectingInputSocket} ")


                #TODO: use pyside to make panels to check if user wants to import into stage or /mat/
                nodeTakingConnection = hou.node(f"/stage/{matlibNode.name()}/{matname}/{nodeTakingConnectionName}")

                if nodeTakingConnection is None:
                    raise Exception(f"Node {nodeTakingConnectionName} not found in the graph")


                nodeMakingInputConnection = hou.node(f"/stage/{matlibNode.name()}/{matname}/{nodeMakingConnectionName}")


                #setNamedInput("refl_roughness", inputNode, "outColor")
                print(f"Connection info: {nodeTakingConnection.name()}.setNamedInput( {nodeTakingConnectingInputSocket}, {nodeMakingInputConnection.name()}, {nodeMakingConnectionOutoutSocker}) ")
                nodeTakingConnection.setNamedInput(nodeTakingConnectingInputSocket, nodeMakingInputConnection, nodeMakingConnectionOutoutSocker)
                print("#########")
            except Exception as e:

                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(f"Error connecting nodes: {e}")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        print("******************************************************")
        print("Connecting graphs between each other")
        #now we wire the connections between graphs
    for graph in rsirGraphs:
        inputConnections = graph["inputConnections"]



        for connection in inputConnections:
            try:    
                #this returns the first keys of the dictionary
                #ej, "RSColorSplitter1:outA": "RSColorMix1:mixAmount" -> "RSColorSplitter1:outA"
                nodeMakingConnectionName = connection.split(":")[0]
                nodeMakingConnectionInputSocketName = connection.split(":")[1]

                nodeMakingConnection = hou.node(f"/stage/{matlibNode.name()}/{matname}/{nodeMakingConnectionName}")


                allNodesTakingConnectionsNames = inputConnections[connection].split("&&")
                for i in range(len(allNodesTakingConnectionsNames)):  
                    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    print(f"Node making input: {nodeMakingConnectionName} and input socket: {nodeMakingConnectionInputSocketName} ")
                    nNodeConnection = allNodesTakingConnectionsNames[i]          
                    
                    nodeTakingConnectionName = nNodeConnection.split(":")[0]        
                    nodeTakingConnectionSocketName = nNodeConnection.split(":")[1]

                    print(f"Node taking connection: {nodeTakingConnectionName} and output socket: {nodeTakingConnectionSocketName} ")

                    nodeTakingConnection = hou.node(f"/stage/{matlibNode.name()}/{matname}/{nodeTakingConnectionName}")


                    print(f"{nodeTakingConnection.name()}.setNamedInput({nodeTakingConnectionSocketName}, {nodeMakingConnection.name()}, {nodeMakingConnectionInputSocketName})")
                    nodeTakingConnection.setNamedInput(nodeTakingConnectionSocketName, nodeMakingConnection, nodeMakingConnectionInputSocketName)
                
            except Exception as e:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(f"Error connecting graphs: {e}")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


    try:
        print("******************************************************")
        print("Connecting suboutput")
        #now we connect the suboutput
        subOutputNode = hou.node(f"/stage/{matlibNode.name()}/{matname}/suboutput1")
        if subOutputNode is None:
            raise Exception(f"Node suboutput1 not found in the graph")
        
        #NOTE if we want to support principled material blending we need to programatically set the output node rather than just assuming its the first standard material
        # to do this we could simply find the MaterialLayer or MaterialBlender  (depending on the approach we take) with the highest number at the end of their name.
        standardMaterialNode = hou.node(f"/stage/{matlibNode.name()}/{matname}/redshift_usd_material1")
        if standardMaterialNode is None:
            raise Exception(f"Node StandardMaterial1 not found in the graph")
        

        print(f"{subOutputNode.name()}, {standardMaterialNode.name()}")
        subOutputNode.setInput(0,standardMaterialNode, 0)

        parent_node.layoutChildren()
        matlibNode.layoutChildren()

        print("YAY YAY YAY YAY YAY YAY YAY YAY YAY")
        print("Script has finished executing succesffuly")
        print("YAY YAY YAY YAY YAY YAY YAY YAY YAY")

    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"Error connecting suboutput: {e}")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

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
    try:
        foundFiles=[]
        for root, dirs, files in os.walk(projectDirectory + '/tex/'):
        # select file name
            for file in files:
                # check the extension of files
                if file.endswith('.json'):
                    foundFiles.append(os.path.join(root, file))
    except Exception as e:
        raise Exception(f"Error during JSON search: {e}")

    return foundFiles

projectFolder = autoDetectFolder()
jsonFiles = findAllJson(projectFolder)
stage = hou.node("/stage")
if not stage:
    raise RuntimeError("Could not find /stage!")  

#before creating a new node we delete the old one if it exists
existingMatLibNode = stage.node("RuneMatLib")
if existingMatLibNode:            
    existingMatLibNode.destroy()

matlibNode = stage.createNode('materiallibrary', node_name='RuneMatLib')

for file in jsonFiles:
    import_rsir_json(file, matlibNode)

