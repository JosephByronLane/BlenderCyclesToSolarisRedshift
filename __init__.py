
if "bpy" in locals():
    import importlib
    importlib.reload(exportMaterial)
    importlib.reload(materialParser)
    importlib.reload(projectFolder)
    importlib.reload(autoDetectFolder)
    importlib.reload(selectFolder)
    importlib.reload(degruopNodes)

#even though we dont use it we need to use bpy for hot reload to work
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
from .panels import projectFolder

from .operators import materialParser
from .operators import autoDetectFolder
from .operators import selectFolder
from .operators import degruopNodes

from .proprieties import customFolder
def register():
    exportMaterial.register()
    materialParser.register()
    projectFolder.register()
    autoDetectFolder.register()
    selectFolder.register()
    customFolder.register()
    degruopNodes.register()

def unregister():
    exportMaterial.unregister()
    materialParser.unregister()
    projectFolder.unregister()
    autoDetectFolder.unregister()
    selectFolder.unregister()
    customFolder.unregister()
    degruopNodes.unregister()


if __name__ == "__main__":
    register()

