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

import os
import asyncio
import winsound
from packaging.version import parse as ver, Version
import json
from datetime import datetime

from pythonosc import udp_client
from aiofiles import open as aio_open
from colorama import init as ColorizeTerminal, Fore, Back, Style

import constants as c
from functions import update_history, undo_table, redo_table, folder_init, play_sound, wait_for_condition
from osc_dict import OSCParameterDict

ColorizeTerminal()

class LPSMasterInstance:
    """ Ties everything together. """
    def __init__(self, vrc_client: udp_client.SimpleUDPClient, osc_version, osc_preload: dict = {}, **kwargs):
        self.ACTION_HISTORY1 = []
        self.ACTION_HISTORY_POSITION1 = -1
        self.ACTION_HISTORY2 = []
        self.ACTION_HISTORY_POSITION2 = -1
        self.ACTION_HISTORY3 = []
        self.ACTION_HISTORY_POSITION3 = -1

        self.ACTION_HISTORY_VERBOSE = True
        self.AVATAR_PARAM_VERBOSE = False

        self.vrc_client = vrc_client
        self.osc_preload = osc_preload
        self.vrc_osc_dict = OSCParameterDict(self.vrc_client, verbose=lambda: self.AVATAR_PARAM_VERBOSE, preload=osc_preload)
        self.osc_version: Version = osc_version
        self.gui_dict = dict()

        self._globals = kwargs.pop("_globals", {"TIMEOUT_FLAG": False})

    @property
    def lps_version(self) -> Version:
        if any(self.vrc_osc_dict[key] == -1 for key in ['LPS/Version_MAJOR', 'LPS/Version_MINOR', 'LPS/Version_PATCH']):
            return None
        
        return ver(f"{self.vrc_osc_dict['LPS/Version_MAJOR']}.{self.vrc_osc_dict['LPS/Version_MINOR']}.{self.vrc_osc_dict['LPS/Version_PATCH']}")

    async def scan_for_unitialized_values(self):
        if -1 in self.vrc_osc_dict.values():
            tries = 0
            while True:  # query init retry loop
                self.vrc_osc_dict["LPS/OSC_Query_Initialize"] = 1  # Re/request parameters and wait for version response
                if not await wait_for_condition(lambda: (-1 not in self.vrc_osc_dict.values()) and self.lps_version, timeout=3):
                    tries += 1
                    continue

                if tries > 3:
                    print(f"{Fore.RED}Took longer than expected to request parameters. Maybe the VRChat client is running too slow?\nIf you just loaded an LPS avatar, you can ignore this warning.{Style.RESET_ALL}")
                
                break

    
    async def uninitialize_values(self):
        async with aio_open("Presets/Poses/preset_1.lpspose", "r", encoding='utf-8') as reference_file:  
            reference_data = await reference_file.read()
            reference_data = json.loads(reference_data)
            reference_data_dict = {dict_item["name"]: dict_item["value"] for dict_item in reference_data["parameters"]}

        # also these
        reference_data_dict.update({
            "201_Hips_X_Move": -1,
            "202_Hips_Y_Move": -1,
            "203_Hips_Z_Move": -1,
            "204_Hips_Scale": -1,
        })

        for key in reference_data_dict.keys():
            self.vrc_osc_dict[key] = -1

    def update_lps_history(self, action, keys, values: tuple, puppet_number: int=0):
        if puppet_number == 0:
            if self.ACTION_HISTORY_VERBOSE: 
                print(f"{Fore.LIGHTRED_EX}Update: Puppet number is 0, returning.{Style.RESET_ALL}")
            return
        if puppet_number == 1:
            self.ACTION_HISTORY1, self.ACTION_HISTORY_POSITION1 = update_history(
                action, keys, values, 
                history=self.ACTION_HISTORY1, position=self.ACTION_HISTORY_POSITION1)
        if puppet_number == 2:
            self.ACTION_HISTORY2, self.ACTION_HISTORY_POSITION2 = update_history(
                action, keys, values, 
                history=self.ACTION_HISTORY2, position=self.ACTION_HISTORY_POSITION2)
        if puppet_number == 3:
            self.ACTION_HISTORY3, self.ACTION_HISTORY_POSITION3 = update_history(
                action, keys, values, 
                history=self.ACTION_HISTORY3, position=self.ACTION_HISTORY_POSITION3)
        
        if self.ACTION_HISTORY_VERBOSE:
            print(f"Puppet {puppet_number} |", action)

    def lps_undo(self, puppet_number: int=0):
        if puppet_number == 0:
            if self.ACTION_HISTORY_VERBOSE: 
                print(f"{Fore.LIGHTRED_EX}Undo: Puppet number is 0, returning.{Style.RESET_ALL}")
            return
        if puppet_number == 1:
            result = undo_table(self.vrc_osc_dict, self.ACTION_HISTORY1, self.ACTION_HISTORY_POSITION1)
            if result:
                self.ACTION_HISTORY1, self.ACTION_HISTORY_POSITION1 = result
                return True
            else:
                if self.ACTION_HISTORY_VERBOSE:
                    print(f"{Fore.LIGHTRED_EX}Nothing to undo on puppet {puppet_number}.{Style.RESET_ALL}")
        if puppet_number == 2:
            result = undo_table(self.vrc_osc_dict, self.ACTION_HISTORY2, self.ACTION_HISTORY_POSITION2)
            if result:
                self.ACTION_HISTORY2, self.ACTION_HISTORY_POSITION2 = result
                return True
            else:
                if self.ACTION_HISTORY_VERBOSE:
                    print(f"{Fore.LIGHTRED_EX}Nothing to undo on puppet {puppet_number}.{Style.RESET_ALL}")
        if puppet_number == 3:
            result = undo_table(self.vrc_osc_dict, self.ACTION_HISTORY3, self.ACTION_HISTORY_POSITION3)
            if result:
                self.ACTION_HISTORY3, self.ACTION_HISTORY_POSITION3 = result
                return True
            else:
                if self.ACTION_HISTORY_VERBOSE:
                    print(f"{Fore.LIGHTRED_EX}Nothing to undo on puppet {puppet_number}.{Style.RESET_ALL}")

    def lps_redo(self, puppet_number: int=0):
        if puppet_number == 0:
            if self.ACTION_HISTORY_VERBOSE: 
                print(f"{Fore.LIGHTRED_EX}Redo: Puppet number is 0, returning.{Style.RESET_ALL}")
            return
        if puppet_number == 1:
            result = redo_table(self.vrc_osc_dict, self.ACTION_HISTORY1, self.ACTION_HISTORY_POSITION1)
            if result:
                self.ACTION_HISTORY1, self.ACTION_HISTORY_POSITION1 = result
                return True
            else:
                if self.ACTION_HISTORY_VERBOSE:
                    print(f"{Fore.LIGHTRED_EX}Nothing to redo on puppet {puppet_number}.{Style.RESET_ALL}")
        if puppet_number == 2:
            result = redo_table(self.vrc_osc_dict, self.ACTION_HISTORY2, self.ACTION_HISTORY_POSITION2)
            if result:
                self.ACTION_HISTORY2, self.ACTION_HISTORY_POSITION2 = result
                return True
            else:
                if self.ACTION_HISTORY_VERBOSE:
                    print(f"{Fore.LIGHTRED_EX}Nothing to redo on puppet {puppet_number}.{Style.RESET_ALL}")
        if puppet_number == 3:
            result = redo_table(self.vrc_osc_dict, self.ACTION_HISTORY3, self.ACTION_HISTORY_POSITION3)
            if result:
                self.ACTION_HISTORY3, self.ACTION_HISTORY_POSITION3 = result
                return True
            else:
                if self.ACTION_HISTORY_VERBOSE:
                    print(f"{Fore.LIGHTRED_EX}Nothing to redo on puppet {puppet_number}.{Style.RESET_ALL}")


    async def lps_save(self, save_name:int, save_type=0, hand_side=None, is_autosave=False, puppet:int=0):
        """ Save pose rig. """
        folder_init()

        hand_side = self.vrc_osc_dict["LPS/Hand_Side"]

        if not save_type:
            if 1 <= save_name <= 6:  # pose slots
                save_type = 0
            elif 7 <= save_name <= 12:  # hand slots
                save_type = 2
            elif 13 <= save_name <= 18:  # face slots
                save_type = 1
            elif 19 <= save_name <= 24 :  # scene slots
                save_type = 3
            
        if save_type == 0:
            reference_file_path = f"Presets/Poses/preset_1.lpspose"
        elif save_type == 2:  # If hand save, check the hand side
            if hand_side is None:
                raise ValueError("hand_side must be specified for hand saves.")
            if hand_side:  # Right hand
                reference_file_path = f"Presets/Hands/_hand_right_ref.json"
            else:  # Left hand
                reference_file_path = f"Presets/Hands/_hand_left_ref.json"
        elif save_type == 1:
            reference_file_path = f"Presets/Faces/preset_32.lpsface"
        elif save_type == 3:
            reference_file_path = f"Presets/Scenes/preset_45.lpsscene"

        if save_type in [0,1,2]:
            async with aio_open(reference_file_path, "r", encoding='utf-8') as reference_file:  # Get pose keys for reference
                reference_data = await reference_file.read()
                reference_data = json.loads(reference_data)
                reference_data_dict = {dict_item["name"]: dict_item["value"] for dict_item in reference_data["parameters"]}  # Get the reference data items

            if not is_autosave:
                save_file = await aio_open(f"{c.LPS_DOCUMENTS}/{['1-6 Poses','13-18 Faces','7-12 Hands'][save_type]}/Slot {save_name}/slot_{save_name} (rename me!).lps{['pose','face','hand'][save_type]}", "a", encoding='utf-8')
            else:
                if not puppet:
                    puppet = self.vrc_osc_dict["LPS/Selected_Puppet"]
                
                save_file = await aio_open(f"{c.LPS_DOCUMENTS}/Autosaves/Puppet {puppet}/Autosave_{datetime.now().strftime(r'%Y-%m-%d_%H-%M-%S')}.lpspose", "a", encoding='utf-8')

            save_file_items = {}  # Create a dictionary to hold the items to be saved
            for key in reference_data_dict.keys():
                save_file_items[key if save_type != 2 else c.HAND_SIDE_SAVE_TEMPLATE["right" if hand_side else "left"][key]] = self.vrc_osc_dict[key]
                # HAND_SIDE_TEMPLATE saves the hand side data in a bilateral-friendly format

            save_file_data = {
                "save_type": save_type, 
                "lps_version": str(self.lps_version),
                "osc_version": str(self.osc_version),
                "parameters": []
            }  # Initialize the save file data structure

            for key, value in save_file_items.items():  # Iterate over the items to be saved
                save_file_data["parameters"].append({"name": key, "value": value})

            await save_file.seek(0)
            await save_file.truncate()  # Clear the file before writing
            await save_file.write(json.dumps(save_file_data, indent=4))
            await save_file.close()
        
        elif save_type == 3:  # save all as scene
            async with aio_open(reference_file_path, "r", encoding='utf-8') as reference_file:  # Get pose keys for reference
                reference_data = await reference_file.read()
                reference_data = json.loads(reference_data)
                reference_data_dict = {dict_item["name"]: dict_item["value"] for dict_item in reference_data["puppet_1"]}

            save_file = await aio_open(f"{c.LPS_DOCUMENTS}/19-24 Scenes/Slot {save_name}/slot_{save_name} (rename me!).lpsscene", "a", encoding='utf-8')

            save_file_data = {
                "save_type": 3, 
                "lps_version": str(self.lps_version),
                "osc_version": str(self.osc_version),
                "puppet_1": [],
                "puppet_2": [],
                "puppet_3": []
            }  # Initialize the save file data structure

            # prevent accidental puppet switch
            def force_close_puppet_select():
                self.vrc_osc_dict["LPS/Selecting_Puppet"] = 0
            
            # for good measure
            force_close_puppet_select()

            buffer_puppet_number = self.vrc_osc_dict["LPS/Selected_Puppet"]

            def save_changes_to_file(puppet_number):
                save_file_items = {}  # Create a dictionary to hold the items to be saved
                for key in reference_data_dict.keys():
                    save_file_items[key] = self.vrc_osc_dict[key]

                for key, value in save_file_items.items():  # Iterate over the items to be saved
                    save_file_data["puppet_"+str(puppet_number)].append({"name": key, "value": value})

            for puppet_x in [1,2,3]:
                await play_sound("Command_Start")
                self.vrc_osc_dict["LPS/Selected_Puppet"] = 0
                await wait_for_condition(lambda: not self.vrc_osc_dict["LPS/Puppet_Ready"] or force_close_puppet_select())
                await self.uninitialize_values()
                await asyncio.sleep(0.2)
                self.vrc_osc_dict["LPS/Selected_Puppet"] = puppet_x
                await wait_for_condition(lambda: not self.vrc_osc_dict["LPS/Puppet_Ready"] or force_close_puppet_select())
                await wait_for_condition(lambda: self.vrc_osc_dict["LPS/Puppet_Ready"] or force_close_puppet_select())
                await self.scan_for_unitialized_values()
                await asyncio.sleep(1)
                save_changes_to_file(puppet_x)

            # write file
            await save_file.seek(0)
            await save_file.truncate()  # Clear the file before writing
            await save_file.write(json.dumps(save_file_data, indent=4))
            await save_file.close()

            # restore puppet selection
            self.vrc_osc_dict["LPS/Selected_Puppet"] = buffer_puppet_number
        

    async def lps_load(self, save_name:int, is_preset=False, save_type=0, hand_side=None, preview=False):
        """ Load to pose rig. Automatically records to undo history. """
        folder_init()

        restore_in_case_of_error = await self.lps_get_current(save_type=save_type, hand_side=hand_side)

        if not hand_side:
            hand_side = self.vrc_osc_dict["LPS/Hand_Side"]

        if not save_type:
            if 1 <= save_name <= 6:  # pose slots
                save_type = 0
            elif 7 <= save_name <= 12:  # hand slots
                save_type = 2
            elif 13 <= save_name <= 18:  # face slots
                save_type = 1
            elif 19 <= save_name <= 24 :  # scene slots
                save_type = 3
            
        if save_type == 0:
            reference_file_path = f"Presets/Poses/preset_1.lpspose"
        elif save_type == 2:  # If hand save, check the hand side
            if hand_side is None:
                raise ValueError("hand_side must be specified for hand saves.")
            if hand_side:  # Right hand
                reference_file_path = f"Presets/Hands/_hand_right_ref.json"
            else:  # Left hand
                reference_file_path = f"Presets/Hands/_hand_left_ref.json"
        elif save_type == 1:
            reference_file_path = f"Presets/Faces/preset_32.lpsface"
        elif save_type == 3:
            reference_file_path = f"Presets/Scenes/preset_45.lpsscene"

        try: 
            # search for file
            file_name = None
            if not is_preset:
                file_list = os.listdir(f"{c.LPS_DOCUMENTS}/{['1-6 Poses','13-18 Faces','7-12 Hands','19-24 Scenes'][save_type]}/Slot {save_name}")
                
                for x in file_list:
                    if not file_list[0].split(".")[-1] in [["lpspose","lpsface","lpshand","lpsscene"][save_type], "json"]:
                        file_list.pop(x)

                if not len(file_list):
                    return None

                else:
                    file_name = f"{c.LPS_DOCUMENTS}/{['1-6 Poses','13-18 Faces','7-12 Hands','19-24 Scenes'][save_type]}/Slot {save_name}/{file_list[0]}"

            elif is_preset:
                file_name = f"Presets/{['Poses','Faces','Hands', 'Scenes'][save_type]}/preset_{save_name}.{['lpspose','lpsface','lpshand','lpsscene'][save_type]}"

            # file doesn't exist
            if not file_name:
                if preview:
                    # load reference instead
                    async with aio_open(reference_file_path, "r", encoding='utf-8') as reference_file:
                        reference_data = await reference_file.read()
                        reference_data = json.loads(reference_data)
                        reference_data_dict = {dict_item["name"]: dict_item["value"] for dict_item in reference_data["parameters"]}
                        reference_data_dict.pop("001_Hips_X", None)
                        self.vrc_osc_dict.update(reference_data_dict)

                    return True

                return None  # fail otherwise

            # file exists, load from file
            async with aio_open(file_name, "r", encoding='utf-8') as save_file:
                save_file_data = await save_file.read()
                save_file_data = json.loads(save_file_data)

                if not is_preset and save_file_data.get("save_type", None) is None:
                    raise ValueError("The file you attempted to load does not contain save type information. Add \"save_type\": 0 (or 1, 2, 3) to the root of the JSON file and try again.\n0 = Pose, 1 = Face, 2 = Hand gesture, 3 = Scene.")

                # check if save type matches intentions
                if not is_preset and save_file_data["save_type"] != save_type:
                    raise ValueError(f"Attempted to load a \"{['Pose', 'Face', 'Hand gesture', 'Scene'][save_file_data['save_type']]}\" file from a \"{['Pose', 'Face', 'Hand gesture', 'Scene'][save_type]}\" slot.")

                if save_type in [0,1,2]:
                    async with aio_open(reference_file_path, "r", encoding='utf-8') as reference_file:  # Get pose keys for reference
                        reference_data = await reference_file.read()
                        reference_data = json.loads(reference_data)
                        reference_data_dict = {dict_item["name"]: dict_item["value"] for dict_item in reference_data["parameters"]}  # Get the reference data items
                        reference_data_dict.pop("001_Hips_X", None)

                    before_values = await self.lps_get_current(save_type=save_type, hand_side=hand_side)
                    for parameter in save_file_data["parameters"]:
                        name, value = parameter["name"], parameter["value"]
                        if save_type != 2:
                            if name in reference_data_dict.keys():
                                self.vrc_osc_dict[name] = value
                        else:
                            if c.HAND_SIDE_LOAD_TEMPLATE[['left','right'][hand_side]][name] in reference_data_dict.keys():
                                self.vrc_osc_dict[c.HAND_SIDE_LOAD_TEMPLATE[['left','right'][hand_side]][name]] = value
                    after_values = await self.lps_get_current(save_type=save_type, hand_side=hand_side)

                    if after_values != before_values and not preview:
                        if save_type == 0:
                            self.update_lps_history(
                                f"Load saved pose {save_name} (\"{file_list[0]}\")" if not is_preset else f"Load preset pose {save_name}", 
                                list(after_values.keys()), (list(before_values.values()), list(after_values.values())),
                                self.vrc_osc_dict["LPS/Selected_Puppet"])
                        elif save_type == 1: 
                            self.update_lps_history(
                                f"Load saved face {save_name} (\"{file_list[0]}\")" if not is_preset else f"Load preset face {save_name}", 
                                list(after_values.keys()), (list(before_values.values()), list(after_values.values())),
                                self.vrc_osc_dict["LPS/Selected_Puppet"])
                        elif save_type == 2:
                            self.update_lps_history(
                                f"Load preset hand {save_name} (\"{file_list[0]}\") to {'right' if hand_side else 'left'} hand" if is_preset else f"Load saved hand {save_name} to {'right' if hand_side else 'left'} hand", 
                                list(after_values.keys()), (list(before_values.values()), list(after_values.values())),
                                self.vrc_osc_dict["LPS/Selected_Puppet"])
                            
                elif save_type == 3 and not preview:  # scene
                    async with aio_open(reference_file_path, "r", encoding='utf-8') as reference_file:  # Get pose keys for reference
                        reference_data = await reference_file.read()
                        reference_data = json.loads(reference_data)
                        reference_data_dict = {dict_item["name"]: dict_item["value"] for dict_item in reference_data["puppet_1"]}

                    async def apply_changes_with_action_history(puppet_number):  # for scene
                        before_values = await self.lps_get_current(save_type=0)
                        for parameter in save_file_data["puppet_"+str(puppet_number)]:
                            name, value = parameter["name"], parameter["value"]
                            if name in reference_data_dict.keys():
                                self.vrc_osc_dict[name] = value
                        after_values = await self.lps_get_current(save_type=0)

                        if after_values != before_values and not preview:
                            self.update_lps_history(
                                f"[SCENE] Load saved pose from scene {save_name} (\"{file_list[0]}\")", 
                                list(after_values.keys()), (list(before_values.values()), list(after_values.values())),
                                puppet_number)

                    # prevent accidental puppet switch
                    def force_close_puppet_select():
                        self.vrc_osc_dict["LPS/Selecting_Puppet"] = 0
                    
                    # for good measure
                    force_close_puppet_select()

                    buffer_puppet_number = self.vrc_osc_dict["LPS/Selected_Puppet"]

                    for puppet_x in [1, 2, 3]:
                        self.vrc_osc_dict["LPS/Selected_Puppet"] = 0
                        await wait_for_condition(lambda: not self.vrc_osc_dict["LPS/Puppet_Ready"] or force_close_puppet_select())
                        await self.lps_save(0, is_autosave=True, puppet=puppet_x)
                        print(f"{Fore.LIGHTCYAN_EX}Autosaved pose for puppet {puppet_x}. (Scene){Style.RESET_ALL}")
                        await play_sound("Autosave")
                        await self.uninitialize_values()
                        self.vrc_osc_dict["LPS/Selected_Puppet"] = puppet_x
                        await wait_for_condition(lambda: not self.vrc_osc_dict["LPS/Puppet_Ready"] or force_close_puppet_select())
                        await wait_for_condition(lambda: self.vrc_osc_dict["LPS/Puppet_Ready"] or force_close_puppet_select())
                        await self.scan_for_unitialized_values()
                        await apply_changes_with_action_history(puppet_x)
                        await asyncio.sleep(1)

                    # restore puppet selection
                    self.vrc_osc_dict["LPS/Selected_Puppet"] = buffer_puppet_number
                
                notify = False

                if not is_preset and not preview:
                    if not save_file_data.get("lps_version", None):
                        print(f"{Fore.YELLOW}Warning: The loaded file does not contain LPS version information.\nIf the pose is accurate, add: \"lps_version\": {self.lps_version} to the root of the JSON file.{Style.RESET_ALL}")
                        notify = True
                    else:
                        if ver(str(save_file_data["lps_version"])) != self.lps_version:
                            print(f"{Fore.YELLOW}Warning: The loaded file was saved with LPS version {save_file_data['lps_version']}, but you are running LPS version {self.lps_version}. The pose may not be accurate.{Style.RESET_ALL}")
                            notify = True
                    if not save_file_data.get("osc_version", None):
                        print(f"{Fore.YELLOW}Warning: The loaded file does not contain OSC version information.\nIf the pose is accurate, add: \"osc_version\": {self.osc_version} to the root of the JSON file.{Style.RESET_ALL}")
                        notify = True
                    else:
                        if ver(str(save_file_data["osc_version"])) != self.osc_version:
                            print(f"{Fore.YELLOW}Warning: The loaded file was saved with LPS-OSC version {save_file_data['osc_version']}, but you are running LPS-OSC version {self.osc_version}. The pose may not be accurate.{Style.RESET_ALL}")
                            notify = True

                    if notify:
                        await play_sound("Warning")

            return True
        
        except Exception as e:
            print(f"{Fore.RED}Ignoring error attempting to load file:\n{type(e).__name__}: {e}{Style.RESET_ALL}")
            self.vrc_osc_dict.update(restore_in_case_of_error)
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            return None
            

    async def lps_get_current(self, save_type=0, hand_side=None) -> dict:
        if len(self.vrc_osc_dict) == 0:
            print("Warning: vrc_osc_dict is empty. LPS may not be fully initialized or it wasn't provided.")

        if -1 in self.vrc_osc_dict.values():
            print("-1 found in vrc_osc_dict. The OSC program may not have fully caught up for some reason.")
        
        if save_type == 0:
            reference_file_path = f"Presets/Poses/preset_1.lpspose"
        elif save_type == 2:  # If hand save, check the hand side
            if hand_side is None:
                raise ValueError("hand_side must be specified for hand saves.")
            if hand_side:  # Right hand
                reference_file_path = f"Presets/Hands/_hand_right_ref.json"
            else:  # Left hand
                reference_file_path = f"Presets/Hands/_hand_left_ref.json"
        elif save_type == 1:
            reference_file_path = f"Presets/Faces/preset_32.lpsface"
        elif save_type == 3:
            reference_file_path = f"Presets/Scenes/preset_45.lpsscene"

        async with aio_open(reference_file_path, "r", encoding='utf-8') as reference_file:  # Get pose keys for reference
            reference_data = await reference_file.read()
            reference_data = json.loads(reference_data)
            reference_data_dict = {dict_item["name"]: dict_item["value"] for dict_item in reference_data["parameters"]}  # Get the reference data items
            reference_data_dict.pop("001_Hips_X", None)
        
        buffer_data = {}

        for key in reference_data_dict.keys():
            try:
                buffer_data[key] = self.vrc_osc_dict[key]
            except KeyError:
                print(f"Key {key} not found in osc_dict. Maybe LPS isn't initialized?")
                continue

        return buffer_data