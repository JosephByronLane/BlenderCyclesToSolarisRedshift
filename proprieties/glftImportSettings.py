import bpy # type: ignore
from ..utils.fillItemsCallback import fillCharactersCallback
from ..utils.fillItemsCallback import fillOutfitCallback
from ..utils.fillItemsCallback import fillBodyCallback
def register():
    bpy.types.Scene.grab_most_recent_meddle_export = bpy.props.BoolProperty(
        name="Grab most recent meddle export",
        description="Retrieves the most recent meddle export and grabs that as the import character.",
        default=True
    )
    bpy.types.Scene.apply_meddle_shaders = bpy.props.BoolProperty(
        name="Import with Meddle Shader",
        description="Automatically applies the Meddle-exported shaders to the imported GLTF.",
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
        default=True
    )   
    bpy.types.Scene.meddle_export_folder = bpy.props.StringProperty(
        name="Meddle export folder",
        description="Folder where all meddle characters/terrain are stored.",
        subtype='DIR_PATH',

        default="L:\\FFXIV TexTools\\Meddle\\"
    )  
    bpy.types.Scene.character_name = bpy.props.EnumProperty(
        name="Character name",
        description="Name of the character to be processed.",
        items=fillCharactersCallback
    )   
    bpy.types.Scene.body_type = bpy.props.EnumProperty(
        name="Character Type",
        description="The verson of the character to be imported (vanilla, modded, with/out piercing, etc).",
        items=fillBodyCallback
    )
    bpy.types.Scene.character_outfit = bpy.props.EnumProperty(
        name="Character gear",
        description="The gear of the character to be imported.",
        items=fillOutfitCallback
    )

#TODO: move to a separate file pls


def unregister():
    del bpy.types.Scene.grab_most_recent_meddle_export
    del bpy.types.Scene.separate_col_gear_gltf
    del bpy.types.Scene.only_merge_skin
    del bpy.types.Scene.keep_smallclothes_separate
    del bpy.types.Scene.meddle_export_folder
    del bpy.types.Scene.character_name
    del bpy.types.Scene.body_type
    del bpy.types.Scene.character_outfit

