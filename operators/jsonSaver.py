import json
import os
import bpy  # type: ignore
from ..data.tempStorage import GLOBAL_DATA_STORE


class RFXUTILS_OT_JsonSaver(bpy.types.Operator):
    bl_idname = "rfxutils.json_saver"
    bl_label = "Json saver"
    bl_description = "Saves the all selected node trees"
    bl_options = {"REGISTER"}

    key: bpy.props.StringProperty()

    def execute(self, context):   
        data = GLOBAL_DATA_STORE.get(self.key)
        if not data:
            self.report({'ERROR'}, "No data found to export!")
            return {'CANCELLED'}

        mat = data["mat"]
        RSIRGraphs = data["RSIRGraphs"]


        basePath = context.scene.custom_folder_path
        texPath = os.path.join(basePath, "tex")
        os.makedirs(texPath, exist_ok=True)
        file_path = os.path.join(texPath, f"{mat.name}.json")

        data_to_save = [n.to_dict() for n in RSIRGraphs]

        try:
            with open(file_path, 'w') as f:
                json.dump(data_to_save, f, indent=2)
            self.report({'INFO'}, f"Exported {mat.name} to {file_path}")

        except Exception as e:
            self.report({'ERROR'}, f"Failed to export {mat.name}: {e}")
            return {'CANCELLED'}
        return {"FINISHED"}
    

def register():
    bpy.utils.register_class(RFXUTILS_OT_JsonSaver)

def unregister():
    bpy.utils.register_class(RFXUTILS_OT_JsonSaver)
