"""
pitchpredict/src/fetch_pitch_data.py
Created by Addison Kline (akline@baseball-analytica.com) in October 2024
"""
# external imports
from pybaseball import statcast_pitcher
import pandas as pd
import datetime
# internal imports
from pitchpredict.logger_config import get_logger
from pitchpredict.models.pitch import Pitch
from pitchpredict.models.pitchpredict_config import PitchPredictConfig
from pitchpredict.similarity import calculate_similarity

logger = get_logger(__name__)

def get_pitches_from_pitcher(pitcher_id: int, config: PitchPredictConfig) -> pd.DataFrame:
    """
    Given a pitcher's MLBAM ID, get a list of all their pitches thrown since the start_date specified.
    Note that this returns a large list of pitches that will be narrowed down later.

    Args:
        pitcher_id (int): The MLBAM ID for the pitcher in question.
    
    Returns:
        DataFrame: A list of all pitches thrown by the given pitcher between start_date and today.
    """
    logger.info(f'Attempting to fetch all pitches from pitcher with id={pitcher_id}')

    date_start = config.start_date
    date_end = config.end_date
    date_end = datetime.datetime.today().strftime(format="%Y-%m-%d") if date_end == 'today' else date_end
    pitches = statcast_pitcher(start_dt=date_start, end_dt=date_end, player_id=pitcher_id)

    if pitches.empty:
        raise ValueError(f"No pitches found for player with id = {pitcher_id}")

    logger.info(f'Successfully retrieved all pitches from pitcher with id={pitcher_id}')
    return pitches
    
def get_most_similar_pitches(pitches: pd.DataFrame, this_pitch: Pitch, config: PitchPredictConfig) -> pd.DataFrame:
    """
    Given a list of all a pitcher's previous pitches as well as the parameters for a new pitch, find a list of most similar pitches previously thrown by the pitcher.

    Args:
        pitches (DataFrame): The list of all pitches thrown previously by this pitcher (in the Statcast era), plus accompanying data.
        this_pitch (Pitch): The desired context to compare all previous pitches to.

    Returns:
        DataFrame: The list of only the most similar pitches to the pitch context given.
    """
    logger.info('Attempting to get most similar pitches to given context')

    pitches['similarity'] = calculate_similarity(pitches=pitches, context=this_pitch)
    pitches = pitches.sort_values(by='similarity', ascending=False)

    pitch_limit = int(config.pitch_sample_pctg * pitches.__len__())

    most_similar_pitches = pitches.iloc[:pitch_limit]
    
    logger.info('Most similar pitches to given context found successfully')
    return most_similar_pitches
    