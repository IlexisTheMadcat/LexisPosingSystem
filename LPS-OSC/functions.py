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

import asyncio
import os
import json
import winsound
from contextlib import suppress

from aiofiles import open as aio_open
from colorama import init as ColorizeTerminal, Fore, Back, Style
from pygame.mixer import Sound

import constants as c

ColorizeTerminal()

async def play_sound(sound_name):
    if isinstance(sound_name, str):
        if sound_name in c.LPS_SOUNDS and c.LPS_SOUNDS[sound_name]:
            if c.LPS_SOUNDS[sound_name] == "MUTE":
                return
            
            with suppress((RuntimeError, FileNotFoundError)):
                Sound(c.LPS_SOUNDS[sound_name]).play()

        else:
            winsound.MessageBeep(winsound.MB_OK)

    elif isinstance(sound_name, int):
        winsound.MessageBeep(sound_name)

def update_history(action, keys, values: tuple, history=[], position=-1):
    """Call after a destructive action to make it undoable. \n
    Also call at start of program for a base line. \n
    Returns a COPY of the new history and position. If history was provided as a class/module attribute, continue to use that in future references. \n
    history - history list \n
    position - position in history \n
    keys - which keys the history effects \n
    values: tuple(before, after) - the values before and after the destructive action \n
    """
    if position < -1:
        history = history[:position+1]
    position = -1
    history.append({
        "action": action, 
        "keys": keys, 
        "values": values
    })

    return history, position


def undo_table(dict_item, history=[], position=-1):
    if not history or position == -len(history):
        return None
    
    else:
        action = history[position]["action"]
        joints = history[position]["keys"]
        values = history[position]["values"]
        for joint, value in zip(joints, values[0]):
            dict_item[joint] = value
        
        position -= 1
        
        print(f"Undid {action}")

        return history, position


def redo_table(dict_item, history=[], position=-1):
    if position >= -1:
        return None
    
    else:
        position += 1

        action = history[position]["action"]
        joints = history[position]["keys"]
        values = history[position]["values"]
        for joint, value in zip(joints, values[1]):
            dict_item[joint] = value

        print(f"Redid {action}")

        return history, position


def search_in_keys(dict_obj, search_term):
    """Search for a term in the keys of a dictionary."""
    found_keys = []
    for key in dict_obj.keys():
        if search_term.lower() in key.lower():
            found_keys.append(key)
    return found_keys

def folder_init():
    if not os.path.exists(c.LPS_DOCUMENTS):  # Initialize folder
        os.mkdir(c.LPS_DOCUMENTS)

    if not os.path.exists(f"{c.LPS_DOCUMENTS}/1-6 Poses"):
        os.mkdir(f"{c.LPS_DOCUMENTS}/1-6 Poses")
    for i in range(1,7):
        if not os.path.exists(f"{c.LPS_DOCUMENTS}/1-6 Poses/Slot {i}"):
            os.mkdir(f"{c.LPS_DOCUMENTS}/1-6 Poses/Slot {i}")

    if not os.path.exists(f"{c.LPS_DOCUMENTS}/7-12 Hands"):
        os.mkdir(f"{c.LPS_DOCUMENTS}/7-12 Hands")
    for i in range(7,13):
        if not os.path.exists(f"{c.LPS_DOCUMENTS}/7-12 Hands/Slot {i}"):
            os.mkdir(f"{c.LPS_DOCUMENTS}/7-12 Hands/Slot {i}")

    if not os.path.exists(f"{c.LPS_DOCUMENTS}/13-18 Faces"):
        os.mkdir(f"{c.LPS_DOCUMENTS}/13-18 Faces")
    for i in range(13,19):
        if not os.path.exists(f"{c.LPS_DOCUMENTS}/13-18 Faces/Slot {i}"):
            os.mkdir(f"{c.LPS_DOCUMENTS}/13-18 Faces/Slot {i}")
    
    if not os.path.exists(f"{c.LPS_DOCUMENTS}/19-24 Scenes"):
        os.mkdir(f"{c.LPS_DOCUMENTS}/19-24 Scenes")
    for i in range(19,25):
        if not os.path.exists(f"{c.LPS_DOCUMENTS}/19-24 Scenes/Slot {i}"):
            os.mkdir(f"{c.LPS_DOCUMENTS}/19-24 Scenes/Slot {i}")

    if not os.path.exists(f"{c.LPS_DOCUMENTS}/Autosaves"):
        os.mkdir(f"{c.LPS_DOCUMENTS}/Autosaves")
    for i in ["Puppet 1","Puppet 2","Puppet 3"]:
        if not os.path.exists(f"{c.LPS_DOCUMENTS}/Autosaves/{i}"):
            os.mkdir(f"{c.LPS_DOCUMENTS}/Autosaves/{i}")

def validate_config():
    with open("config.cfg", "r+", encoding='utf-8') as f:
        _data = json.loads(f.read())

        if "save_file_directory" not in _data.keys():
            _data["save_file_directory"] = r"%userprofile%/Documents/Lexi's Posing System"

        if "sounds" not in _data.keys():
            _data["sounds"] = {}

        sound_dirs = {
            "Startup": "Sounds/Startup.wav",
            "Initialized": "Sounds/Initialized.wav",
            "Timeout": "Sounds/Timeout.wav",
            "Undo": "Sounds/Undo.wav",
            "Redo": "Sounds/Redo.wav",
            "No_Action_History": "Sounds/No_Action_History.wav",
            "Preview_Pose": "Sounds/Redo.wav",
            "Save_Pose": "Sounds/Save_Pose.wav",
            "Load_Pose": "Sounds/Load_Pose.wav",
            "Command_Start": "Sounds/Redo.wav",
            "Command_End": "Sounds/Command_End.wav",
            "Warning": "Sounds/Startup.wav",
            "Autosave": "Sounds/Autosave.wav"
        }

        for key, value in sound_dirs.items():
            if key not in _data["sounds"]:
                _data["sounds"][key] = value
            
        if "autosave" not in _data.keys():
            _data["autosave"] = {}

        autosave_settings = {
            "enabled": 1,
            "interval_seconds": 120,
            "max_autosaves": 10
        }

        for key, value in autosave_settings.items():
            if key not in _data["autosave"]:
                    _data["autosave"][key] = value

        f.truncate(0)
        f.seek(0)
        f.write(json.dumps(_data, indent=4))


async def fetch_saves(save_type=0) -> list:
    """Fetches the list of saved files from the specified directory."""
    folder_init()

    save_dir = f"{c.LPS_DOCUMENTS}/{['Poses','Faces','Hands'][save_type]}"
    save_files = []
    
    for filename in os.path.listdir(save_dir):
        if filename.endswith(".json"):
            save_files.append(filename[:-5])  # Remove the .json extension

    return save_files


async def wait_for_condition(_callable, timeout=0, debug=None, poll_rate=0.1) -> bool:
        """
        Wait for a function to return True. \n
        _callable - function-like object to check for True. \n
        timeout - time in seconds to return. \n
        debug - print `debug` per poll \n
        Returns False if timeout occured.
        """
        if poll_rate < 0.05:
            raise ValueError("Poll rate must be no less than 0.05 seconds to avoid locking up the event loop.")

        if timeout <= 0:
            timeout = 9999

        time_waited = 0
        while True:
            if debug: 
                print(debug)

            if callable(_callable):
                if asyncio.iscoroutinefunction(_callable):
                    if await _callable(): break
                else:
                    if _callable(): break
            else: 
                if _callable: break

            await asyncio.sleep(poll_rate)
            time_waited += poll_rate
            if time_waited >= timeout:
                return False
        
        return True
