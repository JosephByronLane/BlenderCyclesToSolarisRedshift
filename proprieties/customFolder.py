import bpy # type: ignore

def register():
    bpy.types.Scene.custom_folder_path = bpy.props.StringProperty(
        name="Folder Path",
        description="Path to the selected folder",
        subtype='DIR_PATH',
        default=""
    )

def unregister():
    del bpy.types.Scene.custom_folder_path