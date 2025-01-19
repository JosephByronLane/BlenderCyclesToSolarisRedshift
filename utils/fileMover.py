import os
import shutil
import bpy # type: ignore

def fileMover(src, dst, errors):
    """Moves files from the src directory to the /HoudiniProjectFolder/dst directory.

    :param src: Full source path of the file to move.
    :type src: srt
    :param dst: Destination to move the file to (inside the houdini project folder).
    :type dst: str
    :param errors: List  containing errors to report back to the user.
    :type errors: List<str>
    :return: Full path of the moved file.
    :rtype: str
    """
    print("Preparing to move file..")
    print(f"src: {src}")
    print("dst: ", dst) 

    houdiniProjectFolder = bpy.context.scene.custom_folder_path
    if houdiniProjectFolder == "":
        errors.append("Houdini project path not set. Will not move images.")
        return src
    
    fullDstPath = os.path.join(houdiniProjectFolder, dst)  

    print("fullDstPath", fullDstPath)


    #we remove the filename from the path to make sure the directory exists
    dstDirectiryWithoutFileName = os.path.dirname(fullDstPath)

    print("dstDirectiryWithoutFileName", dstDirectiryWithoutFileName)

    if not os.path.exists(dstDirectiryWithoutFileName):
        print("Creating directory: ", dstDirectiryWithoutFileName)
        os.makedirs(dstDirectiryWithoutFileName, exist_ok=True)

    try:
        shutil.copy(src, fullDstPath)
    except FileNotFoundError as e:
        errors.append(f"Blender image filepath couldn't be found. Make sure to not save the images in the blender project: {e}")
        return src

    except Exception as e:
        errors.append(f"Error moving file: {e}")
        return src
    print(f"File moved from {src} to {houdiniProjectFolder}")

    return fullDstPath