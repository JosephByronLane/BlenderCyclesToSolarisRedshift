import bpy # type: ignore

def register():
    bpy.types.Scene.auto_detect_gltf = bpy.props.BoolProperty(
        name="Auto Detect GLTF",
        description="Auto detects the character GLTF file from the Houdini Project folder.",
        default=False
    )
def unregister():
    del bpy.types.Scene.auto_detect_gltf
