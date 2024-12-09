"""
pitchpredict/src/player_lookup.py
Created by Addison Kline (akline@baseball-analytica.com) in October 2024
"""
# external imports
from pybaseball import playerid_lookup
from pandas import read_json
# internal imports
from pitchpredict.models.pitchpredict_config import PitchPredictConfig

def get_player_id_by_name(name: str, config: PitchPredictConfig) -> int:
    """
    Gets the MLBAM ID for the player with the given name.
    This is basically just pybaseball's playerid_lookup with extra bells and whistles.

    Args:
        name (str): The full name (first AND last) of the player being searched.
    
    Returns:
        int: The MLBAM ID for the player with the name given.
    """
    name_first = name.split(' ')[0] if name.__contains__(' ') else ""
    name_last = name.split(' ')[1] if name.__contains__(' ') else name
    fuzzy = config.fuzzy_player_lookup # this parameter is specified in the config

    lookup = playerid_lookup(last=name_last, first=name_first, fuzzy=fuzzy)

    if lookup.empty:
        raise ValueError(f"No player was found for input name '{name}'.")

    mlbam_id = lookup.loc[0, 'key_mlbam'] # get the data from row 1, col key_mlbam
    
    return mlbam_id 