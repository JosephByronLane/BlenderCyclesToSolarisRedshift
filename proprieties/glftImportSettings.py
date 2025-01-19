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
def unregister():
    del bpy.types.Scene.auto_detect_gltf
