import bpy # type: ignore

def register():
    bpy.types.Scene.ignore_invert_nodes = bpy.props.BoolProperty(
        name="Ignore Invert Nodes",
        description="Ignores the export of invert nodes in the chain.",
        default=False
    )
    bpy.types.Scene.move_textures_over = bpy.props.BoolProperty(
        name="Move textxures over",
        description="Exports and moves the textures with their path set to the Houdini project's /tex/ folder .",
        default=True
    )
    bpy.types.Scene.include_osl_shaders = bpy.props.BoolProperty(
        name="Include OSL Shaders",
        description="Allows exporting OSL Shaders where no Redshift nodes are available.",
        default=True
    )
    bpy.types.Scene.move_osl_shaders = bpy.props.BoolProperty(
    name="Move OSL Shaders",
    description="Moves used OSL Shaders to the Houdini's Projects folder under /osl/.",
    default=True
    )
    bpy.types.Scene.render_engine = bpy.props.EnumProperty(
        name="Render Engine",
        description="Select the render engine to use for the export.",
        items=[
            ("REDSHIFT", "Redshift", "Exports the materials for Redshift."), 
            #future plans...
        ],
        default="REDSHIFT"
    )

def unregister():
    del bpy.types.Scene.ignore_invert_nodes
    del bpy.types.Scene.move_textures_over