import bpy # type: ignore

class RFX_OT_ChangeMeshNames(bpy.types.Operator):
    bl_idname = "rfxutils.change_mesh_names"
    bl_label = "Change mesh names"
    bl_description = "Change mesh names to conform to the RuneFX Pipeline nomenclature" 
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selectedObjects = bpy.context.selected_objects

        parsedMaterials = []
        for object in selectedObjects:
            if object.type == "MESH":
                meshFullName = object.name
            

                #since for renaming we need the character's name/body/gear, and the user might of changed the selected character (to import another one, for example)
                #we can grab the name of the parent armature to get the character's data.

                armatureName = object.parent.name

                #the armature name is as follows:
                #{character/gear}_{charaName}_{gear/bodyName}_armature.

                #however the material/geo will be named
                #{character/gear}_{charaName}_{geoName/matName}_geo/{mat}
                splitArmatureName = armatureName.split("_")

                importType = splitArmatureName[0]                
                characterName = splitArmatureName[1]
                outfitName = splitArmatureName[2]

                #gear might be as in c0801h0148_hir_0_mt_c0201h0148_hir_a_hair_5FB0AC65.0;atr_top
                #so we split by _'s, and then we take the 3rd to the 8th element
                #leaving us with hir_0_mt_c0201h0148_hir_a_hairQQ
                #which wont contain doubles of another class, for example the example above contains _top in it.
                print("==============================================")

                print(f"Mesh full name: {meshFullName}")
                returnedName = self.renamer(meshFullName)
                print(f"Returned geo name: {returnedName}")
                nameToApply = f"{importType}_{characterName}_{returnedName}"

                object.name = nameToApply

                #then we rename the materials aswell
                materials = object.data.materials
                for mat in  materials:
                    if mat.name not in parsedMaterials:
                        print("==============================================")
                        matNameFull = mat.name
                        print(f"Material full name: {matNameFull}")
                        returnedName = self.renamer(matNameFull)
                        print(f"Returned mat name: {returnedName}")
                        nameToApply = f"{importType}_{characterName}_{returnedName}"
                        mat.name = nameToApply

                        parsedMaterials.append(mat.name)
                

        return {"FINISHED"}

    def renamer(self, fullName):
        print("----------------------------------------------")
        print("Renaming...")
        fullNameSplitBase = fullName.split("_")

        isMaterial = "mt" in fullNameSplitBase[0] 

        exportSuffix = "_mat" if isMaterial else "_geo"

        
        #we check  this one first because weapons have less total splits than their counterparts.
        #and id rather deal with them here rather than give them their whole house in the function below
        #we can deal with it in the function below, but only as a material, since that one seems to have consistent splits
        if "w" in fullName[0]:
            return "weapon" + exportSuffix
         
        if isMaterial:            
            print("Material detected")
            fullNameSplit = fullNameSplitBase[1:]
        else:
            print("Geo detected")
            fullNameSplit = fullNameSplitBase[4:]

        print(f"Name we will be working with: {fullNameSplit}")

        if  "w" in fullNameSplit[0]:
            return "weapon"+ exportSuffix
        #character (gear, skin, tail, etc)
        elif "c" in fullNameSplit[0]:
            #tail
            #smallclothes
            if "e0000" in fullNameSplit[0]:
                if "top" in fullNameSplit[1]:
                    return "body-bra"+ exportSuffix
                elif "dwn" in fullNameSplit[1]:
                    return "panties"+ exportSuffix
                else:
                    return "unknown"+ exportSuffix
            
            #body/skin
            elif "skin" in fullNameSplit[2]:
                if "bibo" in fullNameSplit[1]:
                    return "body_bibo"+ exportSuffix
                elif "a" in fullNameSplit[1]:
                    return "body_default"+ exportSuffix 
                elif "b" in fullNameSplit[1]:
                    return "body_bibo_hands_legs"+ exportSuffix
                else:
                    return "unknown"+ exportSuffix

            #face    
            #we dont simply check for 'fac' because fac can also be taken by beards, face marking thingies, etc
            elif "fac" in fullNameSplit[1] and "a" in fullNameSplit[2]:
                return "face"+ exportSuffix

            #hair
            elif "hir" in fullNameSplit[1]:
                return "hair"+ exportSuffix

            #brows
            elif "etc" in fullNameSplit[1] and "a" in fullNameSplit[2]:
                return "face_brows"+ exportSuffix
            
            #etc b doesn't exist since originally a was the eyebrows and b was the eyelashes, but since we merged them it dont exist no more.

            #eye shadow
            elif "etc" in fullNameSplit[1] and "c" in fullNameSplit[2]:
                return "face_eye_shadow"+ exportSuffix
            
            #iris
            elif "iri" in fullNameSplit[1]:
                return "face_pupil"+ exportSuffix
            

            #ring
            elif "rir" in fullNameSplit[1]:
                return "ring"+ exportSuffix
            
            #tail
            elif "t" in fullNameSplit[0]:
                return "tail"+ exportSuffix

            
            
            
            #gear

            #hands
            elif "glv" in fullNameSplit[1]:
                return "hands"+ exportSuffix
            
            #feet
            elif "sho" in fullNameSplit[1]:
                return "feet"+ exportSuffix
            
            #legs
            elif "dwn" in fullNameSplit[1]:
                return "legs"+ exportSuffix
            
            #chest
            elif "top" in fullNameSplit[1]:
                return "chest"+ exportSuffix
            
            #helmet
            elif "met" in fullNameSplit[1]:
                return "helmet"+ exportSuffix

            else:
                return "unknown"+ exportSuffix
        else:
            return "unknown"+ exportSuffix    

                    
            
                
def register():
    bpy.utils.register_class(RFX_OT_ChangeMeshNames)

def unregister():
    bpy.utils.register_class(RFX_OT_ChangeMeshNames)
