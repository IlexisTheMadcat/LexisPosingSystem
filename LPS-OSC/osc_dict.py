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

from collections.abc import MutableMapping

from pythonosc import udp_client
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.osc_bundle_builder import OscBundleBuilder
from pythonosc.osc_bundle_builder import IMMEDIATELY

import constants as c

class OSCParameterDict(MutableMapping):
    """
    A dict-like object for OSC parameters. Automatically sends OSC messages. \n
    osc_client: udp_client.SimpleUPDClient - client to send messages from. \n
    verbose: bool/callable - whether to print send and receive updates. \n
    address_prefix - `/address/like/this/` to send parameter changes too.
    preload: dict - preload the store without sending updates.
    ## Parameters must be URL friendly!
    All OSC parameters must not have spaces. \n
    In- and out-bound unicode escape sequences are translated inside the class, feel free to code with them. \n
    Not all characters are supported in OSC messages, so be careful with special characters.
    """

    def __init__(self, osc_client: udp_client.SimpleUDPClient, verbose=True, address_prefix="/avatar/parameters/", preload:dict=dict()):
        self._osc_client = osc_client
        self._store = preload  # Local mirror of the parameters
        self.address_prefix = address_prefix
        self.get_verbose = verbose

    @property
    def verbose(self):
        if callable(self.get_verbose):
            return self.get_verbose()
        else:
            return self.get_verbose

    def encode_name(self, name: str) -> str:
        """ Auto replace spaces with underscores. """
        name = name.replace(" ", "_")
        return name

    def __getitem__(self, key):
        if not isinstance(key, str):
            raise TypeError(f"OSC parameters can only be strings, not '{type(key).__name__}'.")
        
        encoded_name = self.encode_name(key)
        if encoded_name not in self._store:
            raise KeyError(f"{key}")

        return self._store[encoded_name]

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError(f"OSC parameters can only be strings, not '{type(key).__name__}'.")
        
        if not isinstance(value, (int,float)):
            raise TypeError(f"Value must be int or float for OSC, not '{type(value).__name__}'.")
        
        key = self.encode_name(key)
        self._store[key] = value
        if isinstance(value, bool):
            value = int(value)
        self.send_update(key, value)

    def items(self):
        item_dict = {}
        for key, value in self._store.items():
            item_dict[key] = value

        return item_dict.items()

    def keys(self):
        return self._store.keys()
    
    def values(self):
        return self._store.values()

    def __delitem__(self, key):
        key = self.encode_name(key)
        del self._store[key]
        self.send_update(key, 0)

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def update(self, other=(), /, **kwargs):
        """ Builds OSC bundle instead of sending individual messages. """
        if isinstance(other, dict):
            other = {key: value for key, value in other.items()}
            items = other.items()
        elif isinstance(other, tuple):
            if other and all(isinstance(item, tuple) for item in other) and all(len(item) == 2 for item in other):
                items = other
            else:
                raise TypeError(f"Invalid tuple contents for update: expected sequence of (key, value) tuples.")
        else:
            raise TypeError(f"Invalid type for update: {type(other)}. Expected dict or tuple.")

        combined_items = list(kwargs.items()) + list(items)
        for key, value in combined_items:
            if not isinstance(value, (int, float)):
                raise TypeError(f"Value must be int or float for OSC, not '{type(value).__name__}'.")
            
            key = self.encode_name(key)
            self._store[key] = value
            self.send_update(key, value)

        return self

    def clear(self):
        for key in self._store.keys():
            del self._store[key]
            self.send_update(key, 0)

        return self

    def copy(self):
        return self._store.copy()

    def pop(self, key, default=None):
        key = self.encode_name(key)
        value = self._store.items().pop(key, default)
        
        self.send_update(key, 0)

        return value

    def popitem(self):
        key, value = self._store.popitem()

        key = self.encode_name(key)

        del self._store[key]
        self.send_update(key, 0)
        
        return (key, value)

    def overwrite(self, new_data: dict = None):
        """
        Overwrites all stored parameters with new_data (sends them all).
        If new_data is None, just clears everything (resets).
        """
        self.clear()
        if new_data:
            self.update(new_data)

    def send_update(self, parameter: str, value) -> str:
        """ Send an OSC message to update a parameter. Re-encodes unicode characters. """
        parameter = parameter.encode('unicode_escape').decode()
        self._osc_client.send_message(f"{self.address_prefix}{parameter}", value)
        if self.verbose:
            print(f"Sent: {parameter} = {value}")
        
    def receive_update(self, address, value):
        """
        Call this when an OSC message is received. Updates the local dict store. Decodes unicode characters. \n
        Ignores addresses that don't start with `OSCParameterDict.address_prefix`.
        """
        if address.startswith(self.address_prefix):
            param_name = address.replace(self.address_prefix, "")
            param_name = self.encode_name(param_name)
            param_name = param_name.encode().decode('unicode_escape')
            self._store[param_name] = value
            if self.verbose:
                print(f"Received: {param_name} = {value}")
