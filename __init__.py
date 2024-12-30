
if "bpy" in locals():
    import importlib
    importlib.reload(exportMaterial)
    importlib.reload(materialParser)

import bpy
bl_info = {
    "name": "RFXUtils",
    "author": "Rune",
    "version": (0, 1),
    "blender": (4, 3, 0), 
    "location": "3D View > N-panel",
    "description": "Utils for RFX workflow",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}
from .panels import exportMaterial
from .operators import materialParser


def register():
    exportMaterial.register()
    materialParser.register()

def unregister():
    exportMaterial.unregister()
    materialParser.unregister()

if __name__ == "__main__":
    register()

