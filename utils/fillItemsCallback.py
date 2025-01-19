import os

def fillCharactersCallback(self, context):
    """Fills the enum proprieties of the GLTF Importer.

    :param scene: Blenders scene
    :type scene: _type_
    :param context: _description_
    :type context: _type_
    """

    #we first get the meddle folder path
    meddleFolder = self.meddle_export_folder
    if not os.path.isdir(meddleFolder):
        print("ERROR: Meddle folder not found")
        return ["ERROR", "ERROR" , "ERROR"]
    
    #from there, we follow the naming convention
    #{meshFunction}-{characterName}-{outfitName}-{export_textures}

    #the mesh function dictates wether its gear, a collider or terrain.
    #the character name is the name of the character
    #the outfit name is the name of the outfit
    #and the export_textures must be "raw" else it wont show up.

    #we make a list of all the items that match the naming convection and return those for the enum.
    items = []
    for dir in os.listdir(meddleFolder):
        #we check if the dir is a folder/directory and not a file
        if not os.path.isdir(os.path.join(meddleFolder, dir)):
            continue
       

        split = dir.split("-")
        if (split[0] in {"gear", "collider", "terrain"}) and len(split) == 4:
            chara_name = split[1]
            chara_desc = f"Import the character {chara_name}"
            
            #we dont want duplicate characters in the list
            #so we check if the character is already in the list
            #since one character can have many outfits

            if any(chara_name in item for item in items):
                continue

            #we return chara's name twice since the first one is what we'll use to re-build the path
            #when we try to import it.
            items.append((chara_name, chara_name, chara_desc))
    return items


def fillOutfitCallback(self, context):
    """Fills the enum proprieties of the GLTF Importer.

    :param scene: Blenders scene
    :type scene: _type_
    :param context: _description_
    :type context: _type_
    """

    #we first get the meddle folder path
    meddleFolder = self.meddle_export_folder
    if not os.path.isdir(meddleFolder):
        print("ERROR: Meddle folder not found")
        return ["ERROR", "ERROR" , "ERROR"]
    
    #from there, we follow the naming convention
    #{meshFunction}-{characterName}-{outfitName}-{export_textures}

    #the mesh function dictates wether its gear, a collider or terrain.
    #the character name is the name of the character
    #the outfit name is the name of the outfit
    #and the export_textures must be "raw" else it wont show up.

    #we make a list of all the items that match the naming convection and return those for the enum.
    items = []
    for dir in os.listdir(meddleFolder):
        #we check if the dir is a folder/directory and not a file
        if not os.path.isdir(os.path.join(meddleFolder, dir)):
            continue       
        
        split = dir.split("-")
        if (split[0] in {"gear", "terrain"}) and len(split) == 4:
            chara_outfit = split[2]
            chara_desc = f"Import the outfit {chara_outfit}"
            
            #we skip the entries of the not selected characters
            currentlySelectedCharacter = self.character_name

            if currentlySelectedCharacter != split[1]:
                continue

            #we don't really need to check for duplicate outfits here since 
            #by windows' nature, we can't have two folders with the same name in the same directory.

            items.append((chara_outfit, chara_outfit, chara_desc))
    return items

def fillBodyCallback(self, context):
    """Fills the enum proprieties of the GLTF Importer.

    :param scene: Blenders scene
    :type scene: _type_
    :param context: _description_
    :type context: _type_
    """

    #we first get the meddle folder path
    meddleFolder = self.meddle_export_folder
    if not os.path.isdir(meddleFolder):
        print("ERROR: Meddle folder not found")
        return ["ERROR", "ERROR" , "ERROR"]
    
    #from there, we follow the naming convention
    #{meshFunction}-{characterName}-{outfitName}-{export_textures}

    #the mesh function dictates wether its gear, a collider or terrain.
    #the character name is the name of the character
    #the outfit name is the name of the outfit
    #and the export_textures must be "raw" else it wont show up.

    #we make a list of all the items that match the naming convection and return those for the enum.
    items = []
    for dir in os.listdir(meddleFolder):
        #we check if the dir is a folder/directory and not a file
        if not os.path.isdir(os.path.join(meddleFolder, dir)):
            continue       
        
        split = dir.split("-")
        if (split[0] in {"body"}) and len(split) == 4:
            bodyName = split[2]
            bodyDesc = f"Import the body {bodyName}"
            
            #we skip the entries of the not selected characters
            currentlySelectedCharacter = self.character_name

            if currentlySelectedCharacter != split[1]:
                continue

            #we don't really need to check for duplicate body types here since 
            #by windows' nature, we can't have two folders with the same name in the same directory.

            items.append((bodyName, bodyName, bodyDesc))
    return items