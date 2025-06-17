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

from aiofiles import open as aio_open
import constants as c

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

async def fetch_saves(save_type=0) -> list:
    """Fetches the list of saved files from the specified directory."""
    folder_init()

    save_dir = f"{c.LPS_DOCUMENTS}/{['Poses','Faces','Hands'][save_type]}"
    save_files = []
    
    for filename in os.path.listdir(save_dir):
        if filename.endswith(".json"):
            save_files.append(filename[:-5])  # Remove the .json extension

    return save_files


async def wait_for_condition(lambda_expression, timeout=9999, debug=None) -> bool:
        """
        Wait for a function to return True. \n
        lambda_expression - function-like object to check for True. \n
        timeout - time in seconds to return. \n
        debug - print `debug` per poll \n
        Returns whether or not timeout occured.
        """
        timed_out = False
        time_waited = 0
        while True:
            if debug: 
                print(debug)

            if callable(lambda_expression):
                if asyncio.iscoroutinefunction(lambda_expression):
                    if await lambda_expression(): break
                else:
                    if lambda_expression(): break
            else: 
                if lambda_expression: break

            await asyncio.sleep(0.1)
            time_waited += 0.1
            if time_waited >= timeout:
                timed_out = True
                break
        
        return not timed_out
