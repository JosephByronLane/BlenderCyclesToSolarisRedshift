import bpy # type: ignore

class RFX_OT_MergeSimilarMeshes(bpy.types.Operator):
    bl_idname = "rfxutils.merge_meshes"
    bl_label = "Merge Similar Meshes"
    bl_description = "Merges all similar meshes into a single one.  (All _mat into a single one, all _sho to a single one, etc)" 
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selectedObjects = bpy.context.selected_objects

        #dictionary that will hold the objects to merge.
        #the key will be the mesh name up to the last dot
        #the values are a list of t he meshName objects of all meshes that have the same name up to the last dot
        parsedObjects = {}
        

        for object in selectedObjects:
            if object.type == "MESH":
                #mesh names are like 
                # c0801f0102_fac_0_mt_c0801f0102_fac_a_skin_nB94ABBFB.4;atr_t.001
                # or
                # c0801f0102_fac_2_mt_c0801f0102_iri_a_iris_n88D124B1.002
                # or 
                # c0201e0000_glv_0_mt_c0201b0001_bibo_skin_n8DF9FD07.005
                
                #we want to merge all meshes that have the same name up to the last dot
                meshName = object.name
                meshNameParts = meshName.split(".")
                meshNameBase = meshNameParts[0]

                if meshNameBase in parsedObjects:
                    parsedObjects[meshNameBase].append(object)
                else:
                    parsedObjects[meshNameBase] = [object]

        #now we have all the objects we want to merge in the parsedObjects dictionary
        for key in parsedObjects:
            objectsToMerge = parsedObjects[key]
            print("----------------------------------------------")
            print("Merging objects: ", objectsToMerge)
            print("Key: ", key)
            if len(objectsToMerge) > 1:
                #deselect all to ensure a clean context
                bpy.ops.object.select_all(action='DESELECT')
                
                #active object will be first one
                activeObject = objectsToMerge[0]
                bpy.context.view_layer.objects.active = activeObject
                
                # select all remaining objects
                for obj in objectsToMerge:
                    obj.select_set(True)
                
                # merge em
                print("Active object: ", activeObject)
                print("Selected objects: ", objectsToMerge)
                bpy.ops.object.join()
                
                # deselecting them just incase
                bpy.ops.object.select_all(action='DESELECT')
                print("Merged.")
            print("----------------------------------------------")

        
        return {"FINISHED"}


def register():
    bpy.utils.register_class(RFX_OT_MergeSimilarMeshes)

def unregister():
    bpy.utils.register_class(RFX_OT_MergeSimilarMeshes)
