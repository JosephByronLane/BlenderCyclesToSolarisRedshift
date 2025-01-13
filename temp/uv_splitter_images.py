import bpy
import os
from PIL import Image

def extend_image(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        new_img = Image.new('RGBA', (width * 2, height))
        new_img.paste(img, (0, 0))
        new_img.paste(img, (width, 0))
    return new_img

def process_material(material):
    if not material.node_tree:
        return

    for node in material.node_tree.nodes:
        if node.type == 'TEX_IMAGE' and node.image:
            image = node.image
            if image.filepath.endswith('_extended.png'):
                continue  # Skip already extended images

            # Get the directory and filename
            dir_path = os.path.dirname(bpy.path.abspath(image.filepath))
            file_name = os.path.basename(image.filepath)
            name, ext = os.path.splitext(file_name)

            # Create the new directory
            new_dir = os.path.join(dir_path, f"extended_{material.name}")
            os.makedirs(new_dir, exist_ok=True)

            # Create the new filename
            new_file_name = f"{name}_extended.png"
            new_file_path = os.path.join(new_dir, new_file_name)

            # Extend and save the image
            extended_img = extend_image(bpy.path.abspath(image.filepath))
            extended_img.save(new_file_path)

            # Replace the image in the material
            new_image = bpy.data.images.load(new_file_path)
            node.image = new_image

def main():
    
      # Get the "Character" collection
    character_collection = bpy.data.collections.get("Character")
    
    if character_collection is None:
        print("Error: 'Character' collection not found")
        return
    
    # Iterate through all objects in the collection
    for obj in character_collection.objects:
        if obj.type == 'MESH':
        # Process each material
            for material_slot in obj.material_slots:
                if material_slot.material:
                    process_material(material_slot.material)

if __name__ == "__main__":
    main()
