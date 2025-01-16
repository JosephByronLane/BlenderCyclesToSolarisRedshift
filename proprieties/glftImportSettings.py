import bpy # type: ignore

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
def unregister():
    del bpy.types.Scene.auto_detect_gltf
