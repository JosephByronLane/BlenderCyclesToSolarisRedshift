import bpy # type: ignore
from ..utils.fillItemsCallback import fillItemsCallback
def register():
    bpy.types.Scene.auto_detect_gltf = bpy.props.BoolProperty(
        name="Auto Detect GLTF",
        description="Auto detects the character GLTF file from the Houdini Project folder.",
        default=False
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
        default=False
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
