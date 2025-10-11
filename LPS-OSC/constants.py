# ############################################################################################################################
# ##############################################  COPYRIGHT (C)  2025  #######################################################
# ##############################################    IlexisTheMadcat    #######################################################
# ############################################################################################################################
# This program is part of a paid asset for VRChat made by IlexisTheMadcat.
# This code is provided as reference only. Redistribution or modification is not allowed under any circumstances.
# This code is provided as-is, without any express warranty of any kind, and without guarantee of functionality.
# The creator shall not be held liable for any damages this program may cause.
# To report bugs or request features, please use the issue tracker on the original repository.
# To make changes, submit pull requests to the original repository to be approved.
# ############################################################################################################################

import json
import os

if os.path.exists("config.cfg"):
    with open("config.cfg", "r", encoding='utf-8') as f:
        _data = json.loads(f.read())

        LPS_DOCUMENTS = os.path.expandvars(_data["save_file_directory"])
        LPS_SOUNDS = {key: os.path.expandvars(value) for key, value in _data["sounds"].items()}

else:
    LPS_DOCUMENTS = r"%userprofile%/Documents/Lexi's Posing System"

with open("Presets/Poses/preset_1.json", "r", encoding='utf-8') as f:
    reference_data = json.loads(f.read())
    JOINT_INDEX = sorted([param["name"] for param in reference_data["parameters"]])
    JOINT_INDEX.insert(0, "placeholder")  # Aligns joints to the Active Joint parameter

def JOINT_INDEX_GROUPED(joint_number) -> list:  # get joint group for undo history
    if joint_number in range(1,4):  # Hips XYZ
        return {"group": "Hips XYZ", "joints": [JOINT_INDEX[x] for x in range(1,4)]}
    if joint_number in range(4,7):  # Spine XYZ
        return {"group": "Spine XYZ", "joints": [JOINT_INDEX[x] for x in range(4,7)]}
    if joint_number in range(7,10):  # Chest XYZ
        return {"group": "Chest XYZ", "joints": [JOINT_INDEX[x] for x in range(7,10)]}
    if joint_number in range(10,13):  # Neck XYZ
        return {"group": "Neck XYZ", "joints": [JOINT_INDEX[x] for x in range(10,13)]}
    if joint_number in range(13,16): # Head XYZ
        return {"group": "Head XYZ", "joints": [JOINT_INDEX[x] for x in range(13,16)]}
    if joint_number in range(16,18):  # Left Eye XY
        return {"group": "Left Eye XY", "joints": [JOINT_INDEX[x] for x in range(16,18)]}
    if joint_number in range(19,21):  # Right Eye XY
        return {"group": "Right Eye XY", "joints": [JOINT_INDEX[x] for x in range(19,21)]}
    if joint_number in [22,18]:  # Left Shoulder XZ
        return {"group": "Left Shoulder XZ", "joints": [JOINT_INDEX[x] for x in [22,18]]}
    if joint_number in range(23,26):  # Left Upper Arm XYZ
        return {"group": "Left Upper Arm XYZ", "joints": [JOINT_INDEX[x] for x in range(23,26)]}
    if joint_number in [27]:  # Left Lower Arm Z
        return {"group": "Left Lower Arm Z", "joints": [JOINT_INDEX[27]]}
    if joint_number in [28,26,29]:  # Left Hand XYZ
        return {"group": "Left Hand XYZ", "joints": [JOINT_INDEX[x] for x in [28,26,29]]}
    if joint_number in range(30,50):  # Left Fingers XZXX*5
        return {"group": "Left Fingers XZXX*5", "joints": [JOINT_INDEX[x] for x in range(30,50)]}
    if joint_number in [50,21]:  # Right Shoulder XZ
        return {"group": "Right Shoulder XZ", "joints": [JOINT_INDEX[x] for x in [50,21]]}
    if joint_number in range(51,54): # Right Upper Arm XYZ
        return {"group": "Right Upper Arm XYZ", "joints": [JOINT_INDEX[x] for x in range(51,54)]}
    if joint_number in [55]:  # Right Lower Arm Z
        return {"group": "Right Lower Arm Z", "joints": [JOINT_INDEX[55]]}
    if joint_number in [56,54,57]:  # Right Hand XYZ
        return {"group": "Right Hand XYZ", "joints": [JOINT_INDEX[x] for x in [56,54,57]]}
    if joint_number in range(58,78):  # Right Fingers XZXX*5
        return {"group": "Right Fingers XZXX*5", "joints": [JOINT_INDEX[x] for x in range(51,54)]}
    if joint_number in range(78,81):  # Left Upper Leg XYZ
        return {"group": "Left Upper Leg XYZ", "joints": [JOINT_INDEX[x] for x in range(78,81)]}
    if joint_number in range(81,83):  # Left Lower Leg XY
        return {"group": "Left Lower Leg XY", "joints": [JOINT_INDEX[x] for x in range(81,83)]}
    if joint_number in range(83,85):  # Left Foot XY
        return {"group": "Left Foot XY", "joints": [JOINT_INDEX[x] for x in range(83,85)]}
    if joint_number in [85]:  # Left Toe X
        return {"group": "Left Toe X", "joints": [JOINT_INDEX[85]]}
    if joint_number in range(86,89):  # Right Upper Leg XYZ
        return {"group": "Right Upper Leg XYZ", "joints": [JOINT_INDEX[x] for x in range(86,89)]}
    if joint_number in range(89,91):  # Right Lower Leg XY
        return {"group": "Right Lower Leg XY", "joints": [JOINT_INDEX[x] for x in range(89,91)]}
    if joint_number in range(91,93):  # Right Foot XY
        return {"group": "Right Foot XY", "joints": [JOINT_INDEX[x] for x in range(91,93)]}
    if joint_number in [93]:  # Right Toe X
        return {"group": "Right Toe X", "joints": [JOINT_INDEX[93]]}
    if joint_number in range(94,137):  # All facials
        return {"group": "Facial", "joints": JOINT_INDEX[-43:]}

HAND_SIDE_SAVE_TEMPLATE = {
    "left": {
        "030_Left_Index_Proximal_X": "Index_Proximal_X",
        "031_Left_Index_Proximal_Z": "Index_Proximal_Z",
        "032_Left_Index_Intermediate_X": "Index_Intermediate_X",
        "033_Left_Index_Distal_X": "Index_Distal_X",
        "034_Left_Little_Proximal_X": "Little_Proximal_X",
        "035_Left_Little_Proximal_Z": "Little_Proximal_Z",
        "036_Left_Little_Intermediate_X": "Little_Intermediate_X",
        "037_Left_Little_Distal_X": "Little_Distal_X",
        "038_Left_Middle_Proximal_X": "Middle_Proximal_X",
        "039_Left_Middle_Proximal_Z": "Middle_Proximal_Z",
        "040_Left_Middle_Intermediate_X": "Middle_Intermediate_X",
        "041_Left_Middle_Distal_X": "Middle_Distal_X",
        "042_Left_Ring_Proximal_X": "Ring_Proximal_X",
        "043_Left_Ring_Proximal_Z": "Ring_Proximal_Z",
        "044_Left_Ring_Intermediate_X": "Ring_Intermediate_X",
        "045_Left_Ring_Distal_X": "Ring_Distal_X",
        "046_Left_Thumb_Proximal_X": "Thumb_Proximal_X",
        "047_Left_Thumb_Proximal_Z": "Thumb_Proximal_Z",
        "048_Left_Thumb_Intermediate_X": "Thumb_Intermediate_X",
        "049_Left_Thumb_Distal_X": "Thumb_Distal_X"
    },
    "right": {
        "058_Right_Index_Proximal_X": "Index_Proximal_X",
        "059_Right_Index_Proximal_Z": "Index_Proximal_Z",
        "060_Right_Index_Intermediate_X": "Index_Intermediate_X",
        "061_Right_Index_Distal_X": "Index_Distal_X",
        "062_Right_Little_Proximal_X": "Little_Proximal_X",
        "063_Right_Little_Proximal_Z": "Little_Proximal_Z",
        "064_Right_Little_Intermediate_X": "Little_Intermediate_X",
        "065_Right_Little_Distal_X": "Little_Distal_X",
        "066_Right_Middle_Proximal_X": "Middle_Proximal_X",
        "067_Right_Middle_Proximal_Z": "Middle_Proximal_Z",
        "068_Right_Middle_Intermediate_X": "Middle_Intermediate_X",
        "069_Right_Middle_Distal_X": "Middle_Distal_X",
        "070_Right_Ring_Proximal_X": "Ring_Proximal_X",
        "071_Right_Ring_Proximal_Z": "Ring_Proximal_Z",
        "072_Right_Ring_Intermediate_X": "Ring_Intermediate_X",
        "073_Right_Ring_Distal_X": "Ring_Distal_X",
        "074_Right_Thumb_Proximal_X": "Thumb_Proximal_X",
        "075_Right_Thumb_Proximal_Z": "Thumb_Proximal_Z",
        "076_Right_Thumb_Intermediate_X": "Thumb_Intermediate_X",
        "077_Right_Thumb_Distal_X": "Thumb_Distal_X"
    }
}

HAND_SIDE_LOAD_TEMPLATE = {
    "left": {
        "Index_Proximal_X": "030_Left_Index_Proximal_X",
        "Index_Proximal_Z": "031_Left_Index_Proximal_Z",
        "Index_Intermediate_X": "032_Left_Index_Intermediate_X",
        "Index_Distal_X": "033_Left_Index_Distal_X",
        "Little_Proximal_X": "034_Left_Little_Proximal_X",
        "Little_Proximal_Z": "035_Left_Little_Proximal_Z",
        "Little_Intermediate_X": "036_Left_Little_Intermediate_X",
        "Little_Distal_X": "037_Left_Little_Distal_X",
        "Middle_Proximal_X": "038_Left_Middle_Proximal_X",
        "Middle_Proximal_Z": "039_Left_Middle_Proximal_Z",
        "Middle_Intermediate_X": "040_Left_Middle_Intermediate_X",
        "Middle_Distal_X": "041_Left_Middle_Distal_X",
        "Ring_Proximal_X": "042_Left_Ring_Proximal_X",
        "Ring_Proximal_Z": "043_Left_Ring_Proximal_Z",
        "Ring_Intermediate_X": "044_Left_Ring_Intermediate_X",
        "Ring_Distal_X": "045_Left_Ring_Distal_X",
        "Thumb_Proximal_X": "046_Left_Thumb_Proximal_X",
        "Thumb_Proximal_Z": "047_Left_Thumb_Proximal_Z",
        "Thumb_Intermediate_X": "048_Left_Thumb_Intermediate_X",
        "Thumb_Distal_X": "049_Left_Thumb_Distal_X"
    },
    "right": {
        "Index_Proximal_X": "058_Right_Index_Proximal_X",
        "Index_Proximal_Z": "059_Right_Index_Proximal_Z",
        "Index_Intermediate_X": "060_Right_Index_Intermediate_X",
        "Index_Distal_X": "061_Right_Index_Distal_X",
        "Little_Proximal_X": "062_Right_Little_Proximal_X",
        "Little_Proximal_Z": "063_Right_Little_Proximal_Z",
        "Little_Intermediate_X": "064_Right_Little_Intermediate_X",
        "Little_Distal_X": "065_Right_Little_Distal_X",
        "Middle_Proximal_X": "066_Right_Middle_Proximal_X",
        "Middle_Proximal_Z": "067_Right_Middle_Proximal_Z",
        "Middle_Intermediate_X": "068_Right_Middle_Intermediate_X",
        "Middle_Distal_X": "069_Right_Middle_Distal_X",
        "Ring_Proximal_X": "070_Right_Ring_Proximal_X",
        "Ring_Proximal_Z": "071_Right_Ring_Proximal_Z",
        "Ring_Intermediate_X": "072_Right_Ring_Intermediate_X",
        "Ring_Distal_X": "073_Right_Ring_Distal_X",
        "Thumb_Proximal_X": "074_Right_Thumb_Proximal_X",
        "Thumb_Proximal_Z": "075_Right_Thumb_Proximal_Z",
        "Thumb_Intermediate_X": "076_Right_Thumb_Intermediate_X",
        "Thumb_Distal_X": "077_Right_Thumb_Distal_X"
    }
}
