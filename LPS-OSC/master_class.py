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
from typing import Union
import json

from pythonosc import udp_client
from aiofiles import open as aio_open
from colorama import init as ColorizeTerminal, Fore, Back, Style

import constants as c
from functions import update_history, undo_table, redo_table, folder_init
from osc_dict import OSCParameterDict

ColorizeTerminal()

class LPSMasterInstance:
    """ Ties everything together. """
    def __init__(self, **kwargs):
        self.ACTION_HISTORY1 = []
        self.ACTION_HISTORY_POSITION1 = -1
        self.ACTION_HISTORY2 = []
        self.ACTION_HISTORY_POSITION2 = -1
        self.ACTION_HISTORY3 = []
        self.ACTION_HISTORY_POSITION3 = -1

        self.ACTION_HISTORY_VERBOSE = True
        self.AVATAR_PARAM_VERBOSE = False

        self.vrc_client: udp_client.SimpleUDPClient = kwargs.pop("vrc_client", None) # VRChat parameters
        if not self.vrc_client:
            raise ValueError('vrc_client not provided')

        self.vrc_osc_dict = OSCParameterDict(self.vrc_client, verbose=lambda: self.AVATAR_PARAM_VERBOSE, preload=kwargs.pop("osc_preload", {}))
        self.gui_dict = dict()

        self._globals = kwargs.pop("_globals", {})

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


    async def lps_save(self, save_name:int, save_type=0, hand_side=None):
        """ Save pose rig. """
        folder_init()

        hand_side = self.vrc_osc_dict["LPS/Hand_Side"]

        if 1 <= save_name <= 6:  # pose slots
            save_type = 0
        elif 7 <= save_name <= 12:  # hand slots
            save_type = 2
        elif 13 <= save_name <= 18:  # face slots
            save_type = 1
        
        if save_type == 2:  # If hand save, check the hand side
            if hand_side is None:
                raise ValueError("hand_side must be specified for hand saves.")
            if hand_side:  # Right hand
                reference_file_path = f"Presets/Hands/_hand_right_ref.json"
            else:  # Left hand
                reference_file_path = f"Presets/Hands/_hand_left_ref.json"
        else:
            reference_file_path = f"Presets/{['Poses','Faces'][save_type]}/preset_{[1,32][save_type]}.json"

        async with aio_open(f"{c.LPS_DOCUMENTS}/{['1-6 Poses','13-18 Faces','7-12 Hands'][save_type]}/Slot {save_name}/slot_{save_name} (rename me!).json", "a", encoding='utf-8') as save_file:
            async with aio_open(reference_file_path, "r", encoding='utf-8') as reference_file:  # Get pose keys for reference
                reference_data = await reference_file.read()
                reference_data = json.loads(reference_data)
                reference_data_dict = {dict_item["name"]: dict_item["value"] for dict_item in reference_data["parameters"]}  # Get the reference data items
                reference_data_dict.pop("001_Hips_X", None)

            save_file_items = {}  # Create a dictionary to hold the items to be saved
            for key in reference_data_dict.keys():
                save_file_items[key if save_type != 2 else c.HAND_SIDE_SAVE_TEMPLATE["right" if hand_side else "left"][key]] = self.vrc_osc_dict[key]
                # HAND_SIDE_TEMPLATE saves the hand side data in a bilateral-friendly format

            save_file_data = {"save_type": save_type, "parameters": []}  # Initialize the save file data structure

            for key, value in save_file_items.items():  # Iterate over the items to be saved
                save_file_data["parameters"].append({"name": key, "value": value})

            await save_file.seek(0)
            await save_file.truncate()  # Clear the file before writing
            await save_file.write(json.dumps(save_file_data, indent=4))


    async def lps_load(self, save_name:int, is_preset=False, save_type=0, hand_side=None, preview=False):
        """ Load to pose rig. Automatically records to undo history. """
        folder_init()

        restore_in_case_of_error = await self.lps_get_current(save_type=save_type, hand_side=hand_side)

        if not is_preset:
            hand_side = self.vrc_osc_dict["LPS/Hand_Side"]

            if 1 <= save_name <= 6:  # pose slots
                save_type = 0
            elif 7 <= save_name <= 12:  # hand slots
                save_type = 2
            elif 13 <= save_name <= 18:  # face slots
                save_type = 1

        if save_type == 2:  # If hand save, check the hand side
            if hand_side is None:
                raise ValueError("hand_side must be specified for hand saves.")
            if not hand_side:  # Left hand
                reference_file_path = f"Presets/Hands/_hand_left_ref.json"
            else:  # Right hand
                reference_file_path = f"Presets/Hands/_hand_right_ref.json"
        else:
            reference_file_path = f"Presets/{['Poses','Faces'][save_type]}/preset_{[1,32][save_type]}.json"

        try: 
            # search for file
            file_name = None
            if not is_preset:
                file_name = os.listdir(f"{c.LPS_DOCUMENTS}/{['1-6 Poses','13-18 Faces','7-12 Hands'][save_type]}/Slot {save_name}")
                if not len(file_name):
                    pass
                else:
                    file_name = f"{c.LPS_DOCUMENTS}/{['1-6 Poses','13-18 Faces','7-12 Hands'][save_type]}/Slot {save_name}/{file_name[0]}"
            elif is_preset:
                file_name = f"Presets/{['Poses','Faces','Hands'][save_type]}/preset_{save_name}.json"

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

                return None

            # file exists, load from file
            async with aio_open(file_name, "r", encoding='utf-8') as save_file:
                async with aio_open(reference_file_path, "r", encoding='utf-8') as reference_file:  # Get pose keys for reference
                    reference_data = await reference_file.read()
                    reference_data = json.loads(reference_data)
                    reference_data_dict = {dict_item["name"]: dict_item["value"] for dict_item in reference_data["parameters"]}  # Get the reference data items
                    reference_data_dict.pop("001_Hips_X", None)
                
                save_data = await save_file.read()
                save_data = json.loads(save_data)

                # check if save type matches intentions
                if not is_preset and save_data["save_type"] != save_type:
                    raise ValueError(f"Attempted to load a {['Pose', 'Face', 'Hand gesture'][save_data['save_type']]} file from a {['Pose', 'Face', 'Hand gesture'][save_type]} slot.")
                
                before_values = await self.lps_get_current(save_type=save_type, hand_side=hand_side)
                for parameter in save_data["parameters"]:
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
                            f"Load saved pose {save_name}" if not is_preset else f"Load preset pose {save_name}", 
                            list(after_values.keys()), (list(before_values.values()), list(after_values.values())),
                            self.vrc_osc_dict["LPS/Selected_Puppet"])
                    elif save_type == 1: 
                        self.update_lps_history(
                            f"Load saved face {save_name}" if not is_preset else f"Load preset face {save_name}", 
                            list(after_values.keys()), (list(before_values.values()), list(after_values.values())),
                            self.vrc_osc_dict["LPS/Selected_Puppet"])
                    elif save_type == 2:
                        self.update_lps_history(
                            f"Load preset hand {save_name} to {'right' if hand_side else 'left'} hand" if is_preset else f"Load saved hand {save_name} to {'right' if hand_side else 'left'} hand", 
                            list(after_values.keys()), (list(before_values.values()), list(after_values.values())),
                            self.vrc_osc_dict["LPS/Selected_Puppet"])

            return True
        
        except Exception as e:
            print(f"Ignoring error attempting to load file:\n{type(e).__name__}: {e}")
            self.vrc_osc_dict.update(restore_in_case_of_error)
            return None
            

    async def lps_get_current(self, save_type=0, hand_side=None) -> dict:
        if len(self.vrc_osc_dict) == 0:
            print("Warning: vrc_osc_dict is empty. LPS may not be fully initialized or it wasn't provided.")

        if -1 in self.vrc_osc_dict.values():
            print("-1 found in vrc_osc_dict. The OSC program may not have fully caught up for some reason.")
        
        if save_type == 2:  # If hand save, check the hand side
            if hand_side is None:
                raise ValueError("hand_side must be specified for hand saves.")
            if not hand_side:  # Left hand
                reference_file_path = f"Presets/Hands/_hand_left_ref.json"
            else:  # Right hand
                reference_file_path = f"Presets/Hands/_hand_right_ref.json"

        else:
            reference_file_path = f"Presets/{['Poses','Faces'][save_type]}/preset_{[1,32][save_type]}.json"

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