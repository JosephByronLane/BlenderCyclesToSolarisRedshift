import bpy
import bmesh
from mathutils import Vector

def scale_uvs(obj):
    bpy.ops.object.mode_set(mode='EDIT')

    # Save the current area type
    current_area = bpy.context.area.type

    # Change the area to IMAGE_EDITOR
    bpy.context.area.type = 'IMAGE_EDITOR'

    # Access the UV editor and set the 2D cursor location
    for area in bpy.context.screen.areas:
        if area.type == 'IMAGE_EDITOR':
            for space in area.spaces:
                if space.type == 'IMAGE_EDITOR':
                    # Set the 2D cursor location
                    space.cursor_location = (0.0, 0.0)

                    break

    # switch to object mode (required to select objects)
    bpy.ops.object.mode_set(mode='OBJECT')


    obj = bpy.context.object

    # select the object and make it the active object
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # switch to edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    # select all mesh elements
    bpy.ops.mesh.select_all(action='SELECT')

    # use the 2D cursor as pivot
    bpy.context.space_data.pivot_point = 'CURSOR'

    bpy.ops.uv.select_all(action='SELECT')

    # scale the UVs by 0.5 on the X axis
    bpy.ops.transform.resize(value=(0.5, 1, 1))
    bpy.ops.transform

    print("Rescaled UVS")
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.context.area.type = current_area

def select_faces_above_threshold(obj, threshold):
    # Enter edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Get the mesh
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    
    # Ensure we're in face select mode
    bpy.ops.mesh.select_mode(type="FACE")
    
    # Deselect all faces
    bpy.ops.mesh.select_all(action='DESELECT')
    
    # Select faces based on X coordinate
    for face in bm.faces:
        if all((obj.matrix_world @ v.co).x >= threshold for v in face.verts):
            face.select = True
    
    # Update the mesh
    bmesh.update_edit_mesh(me)
    
    bpy.ops.object.mode_set(mode='OBJECT')

def move_selected_uvs(obj):
    bpy.ops.object.mode_set(mode='EDIT')
    
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    uv_layer = bm.loops.layers.uv.verify()
    
    # Move selected UVs by 0.5 on X axis
    for face in bm.faces:
        if face.select:
            for loop in face.loops:
                loop_uv = loop[uv_layer]
                loop_uv.uv.x += 0.5
    
    bmesh.update_edit_mesh(me)
    bpy.ops.object.mode_set(mode='OBJECT')

def process_mesh(obj):
    # Scale UVs
    #scale_uvs(obj)
    
    # Select faces above threshold
    select_faces_above_threshold(obj, -0.001)
    
    # Move selected UVs
    move_selected_uvs(obj)

def main():
    # Get the "Character" collection
    character_collection = bpy.data.collections.get("Character")
    
    if character_collection is None:
        print("Error: 'Character' collection not found")
        return
    
    # Iterate through all objects in the collection
    for obj in character_collection.objects:
        if obj.type == 'MESH':
            # Set the active object
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            
            # Process the mesh
            process_mesh(obj)
            
            # Deselect the object
            obj.select_set(False)

if __name__ == "__main__":
    main()
