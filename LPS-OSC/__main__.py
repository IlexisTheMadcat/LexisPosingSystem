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

# TO ACTIAVTE VENV, DRAG ".venv/Scripts/Activate.ps1" INTO POWERSHELL
# __main__.py must be run from the parent directory (LPS-OSC) to work properly
# TO CREATE EXE:
# Be in ./
# >>> pyinstaller --onefile LPS-OSC/__main__.py -n LPS-OSC.exe

# LPS v1.2.0 OR HIGHER IS REQUIRED TO USE LPS-OSC 1.0.0
LPS_OSC_VERSION = 1.03
LPS_OSC_VERSION_STRING = "v1.0.3"
LPS_VERSIONS = (1.20, 1.210)  # 1.2.0 thru 1.2.1

# import concurrent.futures
import asyncio
import json
import winsound

from pythonosc import udp_client, osc_server, dispatcher
from colorama import init as ColorizeTerminal, Fore, Back, Style

from master_class import LPSMasterInstance
import constants as c
from functions import *
from parameter_preload import PARAMETER_PRELOAD

ColorizeTerminal()

# Set up the client (sending to VRChat)
vrc_client = udp_client.SimpleUDPClient("127.0.0.1", 9000)

LPSMI = LPSMasterInstance(
    vrc_client = vrc_client,
    osc_preload = {dict_item["name"]: dict_item["value"] for dict_item in PARAMETER_PRELOAD["joint_init"]},
    _globals = {"TIMEOUT_FLAG": False, "REDO_RESTORE": {}}
    
)
LPSMI.vrc_osc_dict.update({dict_item["name"]: dict_item["value"] for dict_item in PARAMETER_PRELOAD["control"]})

# Handler function for incoming OSC messages from VRC
def parameter_handler(address, *args):
    LPSMI.vrc_osc_dict.receive_update(address, args[0])

with open("Presets/Poses/preset_1.json", "r", encoding='utf-8') as reference_file:  
        reference_data = reference_file.read()
        reference_data = json.loads(reference_data)
        reference_data_dict = {dict_item["name"]: dict_item["value"] for dict_item in reference_data["parameters"]}

async def initialize_lps_params():
    while True:
        LPSMI.vrc_osc_dict["LPS/OSC_Handshake"] = 1
        if not await wait_for_condition(lambda: not LPSMI.vrc_osc_dict["LPS/OSC_Handshake"], timeout=1, poll_rate=0.05):
            continue
        else:
            break

    while True:
        LPSMI.vrc_osc_dict["LPS/OSC_Query_Initialize"] = 1  # Re/request parameters and wait for version response
        if not await wait_for_condition(lambda: all(LPSMI.vrc_osc_dict[key] != -1 for key in reference_data_dict.keys()) and 0 < LPSMI.vrc_osc_dict["LPS/Version"] < 100, timeout=2):
            continue
        else:
            break

    LPSMI.vrc_osc_dict["LPS/OSC_Initialized"] = 1

    if round(LPSMI.vrc_osc_dict['LPS/Version'], 3) < LPS_VERSIONS[0]:
        print(f"WARNING: This version of LPS ({round(LPSMI.vrc_osc_dict['LPS/Version']), 3}) is older than what the OSC program was designed for! Download the new version from Booth.pm!")
    elif round(LPSMI.vrc_osc_dict['LPS/Version'], 3) > LPS_VERSIONS[1]:
        print(f"WARNING: This version of LPS ({round(LPSMI.vrc_osc_dict['LPS/Version']), 3}) is newer than what the OSC program was designed for! Fetch the updated code from the README!")

    LPSMI.ACTION_HISTORY1 = []
    LPSMI.ACTION_HISTORY_POSITION1 = -1
    LPSMI.update_lps_history(
        "Initial commit",
        list(reference_data_dict.keys()),
        (None, [LPSMI.vrc_osc_dict[key] for key in reference_data_dict.keys()]),
        1)
    LPSMI.ACTION_HISTORY2 = []
    LPSMI.ACTION_HISTORY_POSITION2 = -1
    LPSMI.update_lps_history(
        "Initial commit",
        list(reference_data_dict.keys()),
        (None, [LPSMI.vrc_osc_dict[key] for key in reference_data_dict.keys()]),
        2)
    LPSMI.ACTION_HISTORY3 = []
    LPSMI.ACTION_HISTORY_POSITION3 = -1
    LPSMI.update_lps_history(
        "Initial commit",
        list(reference_data_dict.keys()),
        (None, [LPSMI.vrc_osc_dict[key] for key in reference_data_dict.keys()]),
        3)

    await play_sound("Initialized")

    LPSMI._globals["TIMEOUT_FLAG"] = False

    print(f"{Fore.LIGHTGREEN_EX}LPS initialized!{Style.RESET_ALL}")


async def main_loop():
    while True:
        await asyncio.sleep(0.05)  # Small delay to keep loop efficient

        if LPSMI._globals["TIMEOUT_FLAG"]:

            LPSMI.vrc_osc_dict["LPS/OSC_Initialized"] = 0
            await play_sound("Timeout")
            print(f"{Fore.RED}LPS connection timed out. Attempting reconnect.\nReason: {LPSMI._globals['TIMEOUT_FLAG']}.{Style.RESET_ALL}")
            await initialize_lps_params()
            continue

        # SAVES
        if LPSMI.vrc_osc_dict["LPS/Slot_Number"] > 0:

            if LPSMI.vrc_osc_dict["LPS/Saving"]:
                await play_sound("Command_Start")

                await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Saving_Held"] == 1 or LPSMI.vrc_osc_dict["LPS/Slot_Number"] == 0, timeout=1.25)

                if LPSMI.vrc_osc_dict["LPS/Slot_Number"] == 0: 
                    continue
                
                else:
                    await LPSMI.lps_save(LPSMI.vrc_osc_dict["LPS/Slot_Number"])  # Save the current pose
                    await play_sound("Save_Pose")
                    LPSMI.vrc_osc_dict["LPS/Saving"] = False
                    LPSMI.vrc_osc_dict["LPS/Saving_Held"] = False
                    await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Slot_Number"] == 0)  # Wait for the save slot to be released before continuing

            elif LPSMI.vrc_osc_dict["LPS/Loading"]:
                await play_sound("Command_Start")

                await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Loading_Held"] == 1 or LPSMI.vrc_osc_dict["LPS/Slot_Number"] == 0, timeout=1.25)

                if LPSMI.vrc_osc_dict["LPS/Slot_Number"] == 0:
                    continue  # Stop loading if the save slot is released early

                else:
                    if await LPSMI.lps_load(LPSMI.vrc_osc_dict["LPS/Slot_Number"]):  # Load the saved pose
                        LPSMI.vrc_osc_dict["LPS/Loading"] = False
                        await play_sound("Load_Pose")
                    else:
                        await play_sound("No_Action_History")
                        
                    LPSMI.vrc_osc_dict["LPS/Loading_Held"] = False
                    await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Slot_Number"] == 0)  # Wait for the save slot to be released before continuing

            else:  # Previewing
                buffer_data = await LPSMI.lps_get_current()

                await LPSMI.lps_load(LPSMI.vrc_osc_dict["LPS/Slot_Number"], preview=True)
                await play_sound("Preview_Pose")

                await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Slot_Number"] == 0)
                
                LPSMI.vrc_osc_dict.update(buffer_data)  # Restore the original pose

        # PRESETS
        if LPSMI.vrc_osc_dict["LPS/Preset_Pose"] > 0:

            await play_sound("Command_Start")

            await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Preset_Held"] == 1 or LPSMI.vrc_osc_dict["LPS/Preset_Pose"] == 0, timeout=1.25)

            if LPSMI.vrc_osc_dict["LPS/Preset_Pose"] == 0:
                continue

            else:
                if LPSMI.vrc_osc_dict["LPS/Preset_Pose"] == 1:  # poses (just tpose)
                    await LPSMI.lps_load(LPSMI.vrc_osc_dict["LPS/Preset_Pose"], is_preset=True)
                    await play_sound("Load_Pose")

                elif LPSMI.vrc_osc_dict["LPS/Preset_Pose"] > 1 and LPSMI.vrc_osc_dict["LPS/Preset_Pose"] < 17:  # left hand
                    await LPSMI.lps_load(LPSMI.vrc_osc_dict["LPS/Preset_Pose"], save_type=2, hand_side=0, is_preset=True)
                    await play_sound("Load_Pose")

                elif LPSMI.vrc_osc_dict["LPS/Preset_Pose"] > 16 and LPSMI.vrc_osc_dict["LPS/Preset_Pose"] < 32:  # right hand
                    await LPSMI.lps_load(LPSMI.vrc_osc_dict["LPS/Preset_Pose"]-15, save_type=2, hand_side=1, is_preset=True)
                    await play_sound("Load_Pose")

                elif LPSMI.vrc_osc_dict["LPS/Preset_Pose"] > 31 and LPSMI.vrc_osc_dict["LPS/Preset_Pose"] < 45:  # faces
                    await LPSMI.lps_load(LPSMI.vrc_osc_dict["LPS/Preset_Pose"], save_type=1, is_preset=True)
                    await play_sound("Load_Pose")

                await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Preset_Pose"] == 0)  # Wait for the save slot to be released before continuing

        # APPROXIMATION
        if LPSMI.vrc_osc_dict["LPS/Approximation_Weight_Radial"]:

            await play_sound("Command_Start")

            last_data = await LPSMI.lps_get_current()
            await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Approximation_Weight_Radial"] == 0)
            new_data = await LPSMI.lps_get_current()
            
            if new_data != last_data:
                LPSMI.update_lps_history(
                    "Full Body Approximation",
                    list(new_data.keys()),
                    (list(last_data.values()), list(new_data.values())),
                    LPSMI.vrc_osc_dict["LPS/Selected_Puppet"]
                )

                await play_sound("Command_End")

        # MOVE JOINT
        if (LPSMI.vrc_osc_dict["LPS/Active_Joint"] > 0 and LPSMI.vrc_osc_dict["LPS/Active_Joint"] < 194) or LPSMI.vrc_osc_dict["LPS/Active_Joint"] > 200:
            # 100 is joysticks (compensated), 194-196 is move gadget (ignored), 200 is facials
            
            await play_sound("Command_Start")

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
                    (last_values, new_values),
                    LPSMI.vrc_osc_dict["LPS/Selected_Puppet"]
                )

                await play_sound("Command_End")

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
                    (last_values, new_values),
                    LPSMI.vrc_osc_dict["LPS/Selected_Puppet"])
                
                await play_sound("Command_Start")
            
            await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Copy_Eye_Button"] == 0)

        # UNDO
        if LPSMI.vrc_osc_dict["LPS/Undo"]:
            if LPSMI.lps_undo(LPSMI.vrc_osc_dict["LPS/Selected_Puppet"]):
                await play_sound("Undo")
            else:
                await play_sound("No_Action_History")
            await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Undo"] == 0)

        # REDO
        if LPSMI.vrc_osc_dict["LPS/Redo"]:
            if LPSMI.lps_redo(LPSMI.vrc_osc_dict["LPS/Selected_Puppet"]):
                await play_sound("Redo")
            else:
                await play_sound("No_Action_History")
            await wait_for_condition(lambda: LPSMI.vrc_osc_dict["LPS/Redo"] == 0)

async def osc_handshake():
    while True:  # main loop
        if -1 in LPSMI.vrc_osc_dict.values():
            while True:  # query init retry loop
                LPSMI.vrc_osc_dict["LPS/OSC_Query_Initialize"] = 1  # Re/request parameters and wait for version response
                if not await wait_for_condition(lambda: all(LPSMI.vrc_osc_dict[key] != -1 for key in reference_data_dict.keys()) and 0 < LPSMI.vrc_osc_dict["LPS/Version"] < 100, timeout=2):
                    continue
                else:
                    break
        
        await wait_for_condition(lambda: not LPSMI._globals["TIMEOUT_FLAG"])

        if not LPSMI.vrc_osc_dict["LPS/OSC_Initialized"]:
            LPSMI._globals["TIMEOUT_FLAG"] = "LPS disabled OSC or did not initlialize OSC mode"
            continue

        missed_attempts = 0
        buffer = await LPSMI.lps_get_current()
        for i in range(6):
            if i == 10:
                LPSMI._globals["TIMEOUT_FLAG"] = "LPS did not respond to handshake within 10 seconds"
                break

            LPSMI.vrc_osc_dict["LPS/OSC_Handshake"] = 1 # Re/send handshake signal
            if not await wait_for_condition(lambda: not LPSMI.vrc_osc_dict["LPS/OSC_Handshake"], timeout=1):
                if missed_attempts == 0:
                    print(f"{Fore.BLACK}Warning: Missed handshake attempt.{Style.RESET_ALL}")
                missed_attempts += 1
                continue
            else:
                if missed_attempts > 0:
                    buffer_new = await LPSMI.lps_get_current()
                    print(f"{Fore.BLACK}Reconnected. ({missed_attempts}s){Style.RESET_ALL}")
                    if buffer != buffer_new:
                        print(f"{Fore.YELLOW}Warning: An OSC parameter mismatch was detected during timeout. Something might be out of sync!\n"
                              f"The last known pose was saved. Press UNDO to revert to last known pose.{Style.RESET_ALL}")
                        LPSMI.update_lps_history(
                            "Desync Placeholder",
                            list(buffer_new.keys()),
                            (list(buffer.values()), list(buffer_new.values())),
                            LPSMI.vrc_osc_dict["LPS/Selected_Puppet"]
                        )
                        await play_sound("Warning")
                        LPSMI._globals["REDO_RESTORE"] = buffer
                break
            

async def lps_handshake():
    while True:
        if LPSMI.vrc_osc_dict["LPS/LPS_Handshake"]: # Receive handshake signal
            LPSMI.vrc_osc_dict["LPS/LPS_Handshake"] = 0
        await asyncio.sleep(0.2)

async def run_server():
    disp = dispatcher.Dispatcher()
    disp.map("/avatar/parameters/*", parameter_handler)
    server = osc_server.AsyncIOOSCUDPServer(("127.0.0.1", 9001), disp, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()

    print(f"""
{Fore.LIGHTCYAN_EX}    __    ____  _____{Fore.BLUE}       ____  _____ ______
{Fore.LIGHTCYAN_EX}   / /   / __ \/ ___/{Fore.BLUE}      / __ \/ ___// ____/
{Fore.LIGHTCYAN_EX}  / /   / /_/ /\__ \{Fore.BLUE}______/ / / /\__ \/ /     
{Fore.LIGHTCYAN_EX} / /___/ ____/___/ /{Fore.BLUE}_____/ /_/ /___/ / /___   
{Fore.LIGHTCYAN_EX}/_____/_/    /____/ {Fore.BLUE}     \____//____/\____/   
{Fore.CYAN}
     LPS Assistant OSC Program {LPS_OSC_VERSION_STRING}
    File Management and Action History
    Copyright (C) 2025 IlexisTheMadcat{Style.RESET_ALL}
""")
    print("Listening for OSC messages on port 9001.")

    print(f"Attempting to connect to LPS. \n" \
          f"{Fore.YELLOW}Make sure you have OSC turned on in your avatar settings.{Style.RESET_ALL}")
    
    asyncio.create_task(lps_handshake())
    asyncio.create_task(osc_handshake())

    await play_sound("Startup")

    await initialize_lps_params()

    await main_loop()
    transport.close()

if __name__ == "__main__":
    asyncio.run(run_server())
