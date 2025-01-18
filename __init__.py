
if "bpy" in locals():
    import importlib
    import sys

    ##reloading all the node definitions
    prefix = __package__ + ".panels."
    for name, module in list(sys.modules.items()):
        if name.startswith(prefix) and module is not None:
            importlib.reload(module)

    ##reloading all the node definitions
    prefix = __package__ + ".operators."
    for name, module in list(sys.modules.items()):
        if name.startswith(prefix) and module is not None:
            importlib.reload(module)
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
from .panels import cleanupNodeGraph
from .panels import exportMaterialSettings
from .panels import importGLTF
from .panels import meddlePanel

from .operators import materialParser
from .operators import autoDetectFolder
from .operators import selectFolder
from .operators import degruopNodes
from .operators import showExportWarning
from .operators import jsonSaver
from .operators import showExportWarning
from .operators import orphanRemover
from .operators import disconnectSpecular
from .operators import fixSSS
from .operators import changeNames
from .operators import importGLTFToScene
from .operators import mergeSimilarMesh
from .operators import eyeShadowFixer

from .proprieties import customFolder
from .proprieties import materialParserSettings
from .proprieties import glftImportSettings

from .utils import uniqueDict

def register():
    projectFolder.register()
    importGLTF.register()
    meddlePanel.register()
    cleanupNodeGraph.register()
    exportMaterial.register()
    materialParser.register()
    autoDetectFolder.register()
    selectFolder.register()
    customFolder.register()
    degruopNodes.register()
    jsonSaver.register()
    showExportWarning.register()
    materialParserSettings.register()
    orphanRemover.register()
    disconnectSpecular.register()
    fixSSS.register()
    exportMaterialSettings.register()
    changeNames.register()
    importGLTFToScene.register()
    mergeSimilarMesh.register()
    glftImportSettings.register()
    eyeShadowFixer.register()


def unregister():
    projectFolder.unregister()
    exportMaterial.unregister()
    meddlePanel.register()
    materialParser.unregister()
    autoDetectFolder.unregister()
    selectFolder.unregister()
    customFolder.unregister()
    degruopNodes.unregister()
    jsonSaver.unregister()
    showExportWarning.unregister()
    materialParserSettings.unregister()
    cleanupNodeGraph.unregister()
    orphanRemover.unregister()
    disconnectSpecular.unregister()
    fixSSS.unregister()
    exportMaterialSettings.unregister()
    changeNames.unregister()
    importGLTF.unregister()
    importGLTFToScene.unregister()
    mergeSimilarMesh.unregister()
    glftImportSettings.unregister()
    eyeShadowFixer.unregister()

if __name__ == "__main__":
    register()

