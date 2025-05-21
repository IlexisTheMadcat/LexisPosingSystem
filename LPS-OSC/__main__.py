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

# LPS v1.2.0 OR HIGHER IS REQUIRED TO USE LPS-OSC 1.0.0
LPS_OSC_VERSION = 1.00     # 1.0.0
LPS_VERSIONS = (1.19, 1.21)  # 1.2.0 thru 1.2.0 (+- 0.01 cuz rounding issues)

# import concurrent.futures
import asyncio
import json

from pythonosc import udp_client, osc_server, dispatcher

from master_class import LPSMasterInstance
import constants as c
from functions import *
from parameter_preload import PARAMETER_PRELOAD

# Set up the client (sending to VRChat)
vrc_client = udp_client.SimpleUDPClient("127.0.0.1", 9000)

LPSMI = LPSMasterInstance(
    vrc_client = vrc_client,
    osc_preload = {dict_item["name"]: dict_item["value"] for dict_item in PARAMETER_PRELOAD["joint_init"]}
)
LPSMI.vrc_osc_dict.update({dict_item["name"]: dict_item["value"] for dict_item in PARAMETER_PRELOAD["control"]})

# Handler function for incoming OSC messages from VRC
def parameter_handler(address, *args):
    LPSMI.vrc_osc_dict.receive_update(address, args[0])

async def initialize_lps_params():
    async with aio_open("Presets/Poses/preset_1.json", "r", encoding='utf-8') as reference_file:  
        reference_data = await reference_file.read()
        reference_data = json.loads(reference_data)
        reference_data_dict = {dict_item["name"]: dict_item["value"] for dict_item in reference_data["parameters"]}

    timing_out = False
    while not timing_out:
        LPSMI.vrc_osc_dict["LPS/OSC_Handshake"] = 1
        timing_out = await wait_for_condition(lambda: not LPSMI.vrc_osc_dict["LPS/OSC_Handshake"], timeout=1)

    LPSMI.vrc_osc_dict["LPS/OSC_Query_Initialize"] = 1  # request parameters
    await wait_for_condition(lambda: all(LPSMI.vrc_osc_dict[key] != -1 for key in reference_data_dict.keys()) and 0 < LPSMI.vrc_osc_dict["LPS/Version"] < 100)

    LPSMI.vrc_osc_dict["LPS/OSC_Initialized"] = 1

    if LPSMI.vrc_osc_dict["LPS/Version"] < LPS_VERSIONS[0]:  # not realistic but here for next time
        print(f"WARNING: This version of LPS ({LPSMI.vrc_osc_dict['LPS/Version']}) is older than what the OSC program was designed for! Download the new version from Booth.pm!")
    elif LPSMI.vrc_osc_dict["LPS/Version"] > LPS_VERSIONS[1]:
        print(f"WARNING: This version of LPS ({LPSMI.vrc_osc_dict['LPS/Version']}) is newer than what the OSC program was designed for! Fetch the updated code from the README!")

    print("LPS initialized!")

async def main_loop():
    while True:
        await asyncio.sleep(0.05)  # Small delay to keep loop efficient

        LPSMI.vrc_osc_dict["LPS/OSC_Handshake"] = 1
        if not await wait_for_condition(lambda: not LPSMI.vrc_osc_dict["LPS/OSC_Handshake"], timeout=1):
            LPSMI.vrc_osc_dict["LPS/OSC_Initialized"] = 0
            print("LPS connection timed out. Attempting reconnect.")
            LPSMI.ACTION_HISTORY = -1
            LPSMI.ACTION_HISTORY_POSITION = 0
            await initialize_lps_params()
            continue

        # SAVES
        if LPSMI.vrc_osc_dict["LPS/Slot_Number"] > 0:

            if LPSMI.vrc_osc_dict["LPS/Saving"]:

                await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Saving_Held"] == 1 or LPSMI.vrc_osc_dict["LPS/Slot_Number"] == 0)

                if LPSMI.vrc_osc_dict["LPS/Slot_Number"] == 0: 
                    continue
                
                else:
                    await LPSMI.lps_save(LPSMI.vrc_osc_dict["LPS/Slot_Number"])  # Save the current pose
                    LPSMI.vrc_osc_dict["LPS/Saving"] = False
                    LPSMI.vrc_osc_dict["LPS/Saving_Held"] = False
                    await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Slot_Number"] == 0)  # Wait for the save slot to be released before continuing

            elif LPSMI.vrc_osc_dict["LPS/Loading"]:

                await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Loading_Held"] == 1 or LPSMI.vrc_osc_dict["LPS/Slot_Number"] == 0)

                if LPSMI.vrc_osc_dict["LPS/Slot_Number"] == 0:
                    continue  # Stop loading if the save slot is released early

                else:
                    if await LPSMI.lps_load(LPSMI.vrc_osc_dict["LPS/Slot_Number"]):  # Load the saved pose
                        LPSMI.vrc_osc_dict["LPS/Loading"] = False
                        
                    LPSMI.vrc_osc_dict["LPS/Loading_Held"] = False
                    await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Slot_Number"] == 0)  # Wait for the save slot to be released before continuing

            else:  # Previewing
                buffer_data = await LPSMI.lps_get_current()

                await LPSMI.lps_load(LPSMI.vrc_osc_dict["LPS/Slot_Number"], preview=True)

                await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Slot_Number"] == 0)
                
                LPSMI.vrc_osc_dict.update(buffer_data)  # Restore the original pose

        # PRESETS
        if LPSMI.vrc_osc_dict["LPS/Preset_Pose"] > 0:

            await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Preset_Held"] == 1 or LPSMI.vrc_osc_dict["LPS/Preset_Pose"] == 0)

            if LPSMI.vrc_osc_dict["LPS/Preset_Pose"] == 0:
                continue

            else:
                if LPSMI.vrc_osc_dict["LPS/Preset_Pose"] == 1:  # poses (just tpose)
                    await LPSMI.lps_load(LPSMI.vrc_osc_dict["LPS/Preset_Pose"], is_preset=True)

                elif LPSMI.vrc_osc_dict["LPS/Preset_Pose"] > 1 and LPSMI.vrc_osc_dict["LPS/Preset_Pose"] < 17:  # left hand
                    await LPSMI.lps_load(LPSMI.vrc_osc_dict["LPS/Preset_Pose"], save_type=2, hand_side=0, is_preset=True)

                elif LPSMI.vrc_osc_dict["LPS/Preset_Pose"] > 16 and LPSMI.vrc_osc_dict["LPS/Preset_Pose"] < 32:  # right hand
                    await LPSMI.lps_load(LPSMI.vrc_osc_dict["LPS/Preset_Pose"]-15, save_type=2, hand_side=1, is_preset=True)

                elif LPSMI.vrc_osc_dict["LPS/Preset_Pose"] > 31 and LPSMI.vrc_osc_dict["LPS/Preset_Pose"] < 45:  # faces
                    await LPSMI.lps_load(LPSMI.vrc_osc_dict["LPS/Preset_Pose"], save_type=1, is_preset=True)

                await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Preset_Pose"] == 0)  # Wait for the save slot to be released before continuing

        # APPROXIMATION
        if LPSMI.vrc_osc_dict["LPS/Approximation_Weight_Radial"]:

            last_data = await LPSMI.lps_get_current()
            await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Approximation_Weight_Radial"] == 0)
            new_data = await LPSMI.lps_get_current()
            
            if new_data != last_data:
                LPSMI.update_lps_history(
                    "Full Body Approximation",
                    list(new_data.keys()),
                    (list(last_data.values()), list(new_data.values()))
                )

        # MOVE JOINT
        if (LPSMI.vrc_osc_dict["LPS/Active_Joint"] > 0 and LPSMI.vrc_osc_dict["LPS/Active_Joint"] < 194) or LPSMI.vrc_osc_dict["LPS/Active_Joint"] > 200:
            # 100 is joysticks (compensated), 194-196 is move gadget (ignored), 200 is facials

            # using joysticks
            if LPSMI.vrc_osc_dict["LPS/Active_Joint"] > 100:
                active_joint = LPSMI.vrc_osc_dict["LPS/Active_Joint"]-100
                if active_joint > 100:  # implies use of facials, adjust to joint index bounds
                    active_joint -= 7
            else:  # radials
                active_joint = LPSMI.vrc_osc_dict["LPS/Active_Joint"]
                
            joint_index_grouped_result = c.JOINT_INDEX_GROUPED(active_joint)

            last_values = [LPSMI.vrc_osc_dict[x] for x in joint_index_grouped_result["joints"]]
            await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Active_Joint"] == 0)  # Wait for the active joint to be released
            new_values = [LPSMI.vrc_osc_dict[x] for x in joint_index_grouped_result["joints"]]

            if new_values != last_values:
                LPSMI.update_lps_history(
                    f"Rotate {joint_index_grouped_result['group'].replace('_', ' ')}", 
                    joint_index_grouped_result['joints'],
                    (last_values, new_values)
                )

        # COPY TO RIGHT EYE
        if LPSMI.vrc_osc_dict["LPS/Copy_Eye_Button"]:
            joints = [c.JOINT_INDEX[x] for x in range(19,21)]

            last_values = [LPSMI.vrc_osc_dict[x] for x in joints]
            LPSMI.vrc_osc_dict[c.JOINT_INDEX[19]], LPSMI.vrc_osc_dict[c.JOINT_INDEX[20]] = (
                LPSMI.vrc_osc_dict[c.JOINT_INDEX[16]], LPSMI.vrc_osc_dict[c.JOINT_INDEX[17]])
            new_values = [LPSMI.vrc_osc_dict[x] for x in joints]

            if new_values != last_values:
                LPSMI.update_lps_history(
                    "Copy left eye to right eye", 
                    joints, 
                    (last_values, new_values))
            
            await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Copy_Eye_Button"] == 0)

        # UNDO
        if LPSMI.vrc_osc_dict["LPS/Undo"]:
            LPSMI.lps_undo()
            await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Undo"] == 0)

        # REDO
        if LPSMI.vrc_osc_dict["LPS/Redo"]:
            LPSMI.lps_redo()
            await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Redo"] == 0)

async def lps_handshake():
    while True:  # handshake
        if LPSMI.vrc_osc_dict["LPS/LPS_Handshake"]:
            LPSMI.vrc_osc_dict["LPS/LPS_Handshake"] = 0
        await asyncio.sleep(0.2)

async def run_server():
    disp = dispatcher.Dispatcher()
    disp.map("/avatar/parameters/*", parameter_handler)
    server = osc_server.AsyncIOOSCUDPServer(("127.0.0.1", 9001), disp, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    print("Listening for OSC messages on port 9001.")

    async with aio_open("Presets/Poses/preset_1.json", "r", encoding='utf-8') as reference_file:  
        reference_data = await reference_file.read()
        reference_data = json.loads(reference_data)
        reference_data_dict = {dict_item["name"]: dict_item["value"] for dict_item in reference_data["parameters"]}

    print("Attempting to connect to LPS. \n" \
          "Make sure you have OSC turned on in your avatar settings.")
    
    asyncio.create_task(lps_handshake())

    await initialize_lps_params()
    LPSMI.update_lps_history(
        "Initial commit",
        list(reference_data_dict.keys()),
        (None, [LPSMI.vrc_osc_dict[key] for key in reference_data_dict.keys()]))

    await main_loop()
    transport.close()

if __name__ == "__main__":
    asyncio.run(run_server())
