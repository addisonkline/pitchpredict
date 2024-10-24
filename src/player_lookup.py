"""
pitchpredict/src/player_lookup.py
Created by Addison Kline (akline@baseball-analytica.com) in October 2024
"""
from pybaseball import playerid_lookup
from pandas import read_json

config = read_json('config.json').iloc[0]

def get_player_id_by_name(name: str) -> int:
    """
    Gets the MLBAM ID for the player with the given name.
    This is basically just pybaseball's playerid_lookup with extra bells and whistles.

    Args:
        name (str): The full name (first AND last) of the player being searched.
    
    Returns:
        int: The MLBAM ID for the player with the name given.
    """
    name_first = name.split(' ')[0]
    name_last = name.split(' ')[1]
    fuzzy = config.get('fuzzy_player_lookup') # this parameter is specified in the config

    mlbam_id = playerid_lookup(last=name_last, first=name_first, fuzzy=fuzzy).loc[0, 'key_mlbam'] # get the data from row 1, col key_mlbam
    
    return mlbam_id 