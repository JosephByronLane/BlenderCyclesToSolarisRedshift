import bpy
from PIL import Image
import os

# get the selected object
obj = bpy.context.active_object

# loop through its materials
for mat_slot in obj.material_slots:
    mat = mat_slot.material
    if mat is not None and mat.use_nodes:
        # loop through material's nodes
        for node in mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                # this is an image texture node
                image = node.image
                if image is not None:
                    new_filepath = image.filepath[:-4] + "_mirrored5.png"
                    # check if mirrored image already exists
                    if os.path.isfile(new_filepath):
                        # mirrored image exists, load it
                        new_image = bpy.data.images.load(new_filepath)
                        # update the node to use the new image
                        node.image = new_image
                    elif not image.filepath.endswith("_mirrored5.png"):
                        print(" augmenting image;  present.")
                        print("Image path:", image.filepath)
                        # open the image
                        orig_img = Image.open(image.filepath)

                        # mirror it
                        #mirrored_img = orig_img.transpose(Image.FLIP_LEFT_RIGHT)
                        mirrored_img = orig_img
                        # concatenate original and mirrored images
                        new_img = Image.new('RGBA', (orig_img.width * 2, orig_img.height))
                        new_img.paste(orig_img, (0, 0))
                        new_img.paste(mirrored_img, (orig_img.width, 0))

                        # save it
                        new_img.save(new_filepath)
                        
                        # load the new image
                        new_image = bpy.data.images.load(new_filepath)

                        # update the node to use the new image
                        node.image = new_image
                        
                        
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
        

print("Rescaled UVS")
bpy.ops.object.mode_set(mode='OBJECT')

bpy.context.area.type = current_area
