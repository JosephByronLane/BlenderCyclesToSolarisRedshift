import hou
import json
import os, stat
import ptvsd
import time

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

    print("******************************************************")
    print("Creating individual graphs")   
    for graph in rsirGraphs:

        #first we create the RS Nodes based on the RSIRGraph children
        try:
            children = graph["children"]
            if len(children) == 0:
                raise Exception("No children found on graph")
            
        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(f"Error no children found on graph {graph['uId']}: {e}")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(f"Creating graph {graph['uId']} with {len(children)} children")


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
                #creating network dots doesn't work with the createNode function, so we need to use the createNetworkDot function
                # on the material node itself.

                #TODO: remove the if-else and make it an elif for the other node types that might spring up
                if not nodeType ==  "__dot":
                    createdNode = parent_node.createNode(nodeType, node_name=nodeName)
                else:
                    createdNode = parent_node.createNetworkDot()

            except Exception as e:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(f"Error creating node {nodeType}: {e}")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

            for name, value in nodeProps.items():
                try:
                    #vector/color parameters
                    if isinstance(value, (list, tuple)) and len(value) > 1 and all(isinstance(v, (int, float)) for v in value):
                        print(f"Setting tuple parameter '{name}' to '{value}' on node '{nodeName}'")

                        parm = createdNode.parmTuple(name)
                        if parm is not None:
                            parm.set(value)
                        else:
                            raise Exception(f"Tuple parameter '{name}' not found on node '{nodeName}'")
                    
                    #float parameters
                    elif isinstance(value, (int, float)):
                        print(f"Setting float parameter '{name}' to '{value}' on node '{nodeName}'")

                        parm = createdNode.parm(name)
                        if parm is not None:
                            parm.set(value)
                        else:
                            raise Exception(f"Float parameter '{name}' not found on node '{nodeName}'.")
                        
                    #ramp Nodes/parameters
                    elif isinstance(value, dict) and name == "ramp":
                        print(f"Setting ramp parameter '{name}' to '{value}' on node '{nodeName}'")

                        stops = value["stops"]
                        interpolationValue = value.get("interpolation", "CONSTANT")  
                        
                        interpolation = {
                            "LINEAR":    hou.rampBasis.Linear,
                            "EASE":      hou.rampBasis.CatmullRom,  
                            "CONSTANT":  hou.rampBasis.Constant,
                            "CARDINAL":  hou.rampBasis.Bezier,
                            "B_SPLINE":  hou.rampBasis.BSpline
                        }      

                        ramp_basis = interpolation[interpolationValue]
            
                        positions = []
                        values = []
                        for stop in stops:
                            positions.append(stop["position"])
                            values.append(stop["color"])
                            
                        num_stops = len(stops)
                        bases = tuple(ramp_basis for _ in range(num_stops)) #blender only supports one interpolation type for all stops                
                        
                        ramp_data = hou.Ramp(bases, tuple(positions), tuple(values))    

                        createdNode.parm('ramp').set(ramp_data)

                    #OSL Nodes/parameters
                    elif isinstance(value, dict) and name == "osl":
                        
                        for prop in value:
                            print(f"Setting OSL parameter '{prop}' to '{value[prop]}' on node '{nodeName}'")

                            parm = createdNode.parm(prop)                            
                                
                            if parm is not None:
                                parm.set(value[prop])

                            if prop == "RS_osl_file":
                                print(f"rsl path put, pressing button")
                                createdNode.parm('RS_osl_compile').pressButton()

                            if parm is None:
                                raise Exception(f"OSL parameter '{prop}' not found on node '{nodeName}'")
                        
                    #string parameters
                    elif isinstance(value, str):
                        print(f"Setting string parameter '{name}' to '{value}' on node '{nodeName}'")

                        parm = createdNode.parm(name)
                        if parm is not None:
                            parm.set(value)
                        else:
                            raise Exception(f"String parameter '{name}' not found on node '{nodeName}'")
                    
                    
                    
                    else:
                        raise Exception(f"Unsupported parameter type for '{name}' on node '{nodeName}'")


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

                #while we could add the loop to check if a graph as many inputs, truth is we dont since we can define all those inputs on the blender sript.
                #though ideally perhaps it would be better to standarize both functions here and below, so:
                #TODO: make this function similar to the one below to check if &&'s are present and loop through them
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
        if graph["uId"] == "__dot":
            isDot = True
        else:
            isDot = False


        for connection in inputConnections:
            try:    
                #this returns the first keys of the dictionary
                #ej, "RSColorSplitter1:outA": "RSColorMix1:mixAmount" -> "RSColorSplitter1:outA"
                nodeMakingConnectionName = connection.split(":")[0]
                nodeMakingConnectionInputSocketName = connection.split(":")[1]

                nodeMakingConnection = hou.item(f"/stage/{matlibNode.name()}/{matname}/{nodeMakingConnectionName}")
                #check if what were tryna connect is a network dot, if it is then it wont have these properties
                if isDot:
                    nodeMakingConnectionInputSockets = nodeMakingConnection.inputNames()
                    nodeMakingConnectionSocketIndex = nodeMakingConnectionInputSockets.index(nodeMakingConnectionInputSocketName) if nodeMakingConnectionInputSocketName in nodeMakingConnectionInputSockets else 0
                else:
                    nodeMakingConnectionSocketIndex = 0

                if nodeMakingConnection is None:
                    raise Exception(f"Node {nodeMakingConnectionName} not found in the graph. Did you export it in the children's list and is the node type correct?")

                allNodesTakingConnectionsNames = inputConnections[connection].split("&&")
                for i in range(len(allNodesTakingConnectionsNames)):  
                    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    print(f"Node making input: {nodeMakingConnectionName} and input socket: {nodeMakingConnectionInputSocketName} ")
                    nNodeConnection = allNodesTakingConnectionsNames[i]          
                    
                    nodeTakingConnectionName = nNodeConnection.split(":")[0]        
                    nodeTakingConnectionSocketName = nNodeConnection.split(":")[1]
                    #check if what were tryna connect is a network dot, if it is then it wont have these properties
                    nodeTakingConnectionInputSockets = nodeTakingConnection.inputNames()
                    nodeTakingConnectionSocketIndex = nodeTakingConnectionInputSockets.index(nodeTakingConnectionSocketName) if nodeTakingConnectionSocketName in nodeTakingConnectionInputSockets else 0

                    print(f"Node taking connection: {nodeTakingConnectionName} and output socket: {nodeTakingConnectionSocketName} ")

                    #we use hou.item rather than hou.node since networkDots cant be accessed with hou.node
                    nodeTakingConnection = hou.item(f"/stage/{matlibNode.name()}/{matname}/{nodeTakingConnectionName}")


                    print(f"{nodeTakingConnection.name()}.setInput({nodeTakingConnectionSocketIndex}, {nodeMakingConnection.name()}, {nodeMakingConnectionSocketIndex})")
                    nodeTakingConnection.setInput(nodeTakingConnectionSocketIndex, nodeMakingConnection, nodeMakingConnectionSocketIndex)
                
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


def autoFillMaterials(matLibNode):
    """Auto fills and assigns the materials to the character according to RuneFX Pipeline naming convention

    :param matLibNode: Material Library node containing the materials
    :type matLibNode: hou.node
    """

    print("******************************************************")
    print("Parsing material names")

    #we populate the materials
    populateMatsButton = matLibNode.parm("fillmaterials")
    populateMatsButton.pressButton()

    numMats = matLibNode.parm("materials").eval()

    acceptedMaterialNames = ["hair_mat", "face_mat", "body_mat", "bra_mat", "hands_mat", "tail_mat", "panties_mat", "pupil_mat", "brows_mat", "feet_mat", "pants_mat", "chest_mat", "head_mat", "eyeShadow_mat"]

    #we verify that the materials exist in the list of accepted materials exported from blender
    #NOTE: the materials output should be sanitized from the blender output, but it doesn't hurt to check it here too.
    existingMatNodesList = matLibNode.children()
    validMaterials = []
    for matNode in existingMatNodesList:
        try:
            matName = matNode.name()
            print("===============================================================")
            print(f"Checking material {matName}...")
            if matName in acceptedMaterialNames:
                validMaterials.append(matName)
                print(f"Material {matName} found in the list of accepted materials")
            else:
                raise Exception(f"Material {matName} not found in the list of accepted materials. It will not be bound to geometry")
        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(f"Error checking  materials:: {e}")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    print("******************************************************")
    print("Binding materials to geometry")

    #we bind the materials to the geometry
    for i in range(1, numMats+1):
        try:
            #first we get the materials name
            matNameFull = matLibNode.parm(f"matnode{i}").eval() #chest_mat
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(f"Binding material {matNameFull} to geometry...")
            if matNameFull in validMaterials:
                matNamePart = matNameFull.split("_")[0] #chest

                #since the head, hands and face are all separate materials on the same mesh we need do use USD's subdiv groups so no SSS seams appear
                if matNameFull == "face_mat" or matNameFull == "head_mat" or matNameFull == "body_mat":
                    matSuffix = f"_grp/{matNamePart}_geo"
                else:
                    matSuffix = f"_geo"

                geoAssignmentParm = matlibNode.parm(f'geopath{i}')

                print(f"Binding material {matNameFull} to geometry {matNamePart}{matSuffix}...")

                geoAssignmentParm.set(f"/stage/geo/{matNamePart}{matSuffix}")

                
        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(f"Error populating materials: {e}")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")






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




