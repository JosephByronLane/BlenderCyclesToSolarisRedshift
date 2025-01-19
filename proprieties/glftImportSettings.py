import bpy # type: ignore
from ..utils.fillItemsCallback import fillItemsCallback
def register():
    bpy.types.Scene.grab_most_recent_meddle_export = bpy.props.BoolProperty(
        name="Grab most recent meddle export",
        description="Retrieves the most recent meddle export and grabs that as the import character.",
        default=True
    )
    bpy.types.Scene.separate_col_gear_gltf = bpy.props.BoolProperty(
        name="Separate Gear and Collider GLTF",
        description="Tells the importer wether you have separate collider + gear GLTF or a single file.",
        default=False
    )
    bpy.types.Scene.only_merge_skin = bpy.props.BoolProperty(
        name="Only merge skin meshes",
        description="Only merges skin meshes rather than the whole darn thing.",
        default=False
    )
    bpy.types.Scene.keep_smallclothes_separate = bpy.props.BoolProperty(
        name="Keep smallclothes separate",
        description="Ensures that the smallclotes aren't merged into the same mesh as the body.",
        default=True
    )   
    bpy.types.Scene.meddle_export_folder = bpy.props.BoolProperty(
        name="Meddle export folder",
        description="Folder where all meddle characters/terrain are stored.",
        default="L:\FFXIV TexTools\Meddle"
    )  
    bpy.types.Scene.character_name = bpy.props.EnumProperty(
        name="Character name",
        description="Name of the character to be processed.",
        items=[
        ],
        default=""
    )   
    bpy.types.Scene.collider_type = bpy.props.EnumProperty(
        name="Collider Type",
        description="The type of collider to be imported (vanilla, modded, etc.).",
        items=[
        ],
        default=""
    )
    bpy.types.Scene.character_outfit = bpy.props.EnumProperty(
        name="Character Outfit",
        description="The outfit of the character to be imported.",
        items=[
        ],
        default=fillItemsCallback
    )

#TODO: move to a separate file pls


def unregister():
    del bpy.types.Scene.auto_detect_gltf
