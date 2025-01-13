import os


def findOSLShaderDirectory(nodeBl_id, identifier):
    """Finds the directory containing the specified OSL Shader. Naming convention is "'ShaderNodeBl_id'_'identifier'.osl".

    :param nodeBl_id: Unique node bl_idname to identify the shader.
    :type nodeBl_id: str
    :param identifier: unique identifier saying what the shader does.
    :type identifier: str
    """
    #osl filepath is under /osl/ directory, we are currently in the /utils/ directory
    oslDirectory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "osl")
    oslShader = f"{nodeBl_id}-{identifier}.osl"

    print(f"OSL SHADER: {oslShader}")
    print(f"OSL DIRECTORY: {oslDirectory}")

    for root, dirs, files in os.walk(oslDirectory):
        print(f"searching in {root}")
        if oslShader in files:

            return os.path.join(root, oslShader)
    
    return None