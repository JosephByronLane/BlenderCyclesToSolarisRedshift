
if "bpy" in locals():
    import importlib
    import sys
    importlib.reload(exportMaterial)
    importlib.reload(materialParser)
    importlib.reload(projectFolder)
    importlib.reload(autoDetectFolder)
    importlib.reload(selectFolder)
    importlib.reload(degruopNodes)
    importlib.reload(nodes)
    importlib.reload(jsonSaver)
    importlib.reload(showExportWarning)
    importlib.reload(findOslShader)
    ##reloading all the node definitions
    prefix = __package__ + ".nodes."
    for name, module in list(sys.modules.items()):
        if name.startswith(prefix) and module is not None:
            importlib.reload(module)

    importlib.reload(uniqueDict)

    ##reloading all the data definitions
    prefix = __package__ + ".data."
    for name, module in list(sys.modules.items()):
        if name.startswith(prefix) and module is not None:
            importlib.reload(module)
    

#even though we dont use it we need to use bpy for hot reload to work
import bpy  # type: ignore


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
from .operators import showExportWarning
from .operators import jsonSaver
from .operators import showExportWarning
from .proprieties import customFolder

from .utils import uniqueDict
from .utils import findOslShader
from . import nodes



def register():
    exportMaterial.register()
    materialParser.register()
    projectFolder.register()
    autoDetectFolder.register()
    selectFolder.register()
    customFolder.register()
    degruopNodes.register()
    jsonSaver.register()
    showExportWarning.register()

def unregister():
    exportMaterial.unregister()
    materialParser.unregister()
    projectFolder.unregister()
    autoDetectFolder.unregister()
    selectFolder.unregister()
    customFolder.unregister()
    degruopNodes.unregister()
    jsonSaver.unregister()
    showExportWarning.unregister()


if __name__ == "__main__":
    register()

