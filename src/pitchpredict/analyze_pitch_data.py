"""
pitchpredict/src/analyze_pitch_data.py
Created by Addison Kline (akline@baseball-analytica.com)
"""
import pandas as pd
from collections import Counter
from pitchpredict.logger_config import get_logger

logger = get_logger(__name__)

def digest_pitch_data(pitches: pd.DataFrame) -> pd.DataFrame:
    """
    Given the DataFrame of most similar pitches, analyze the data and return a DataFrame of the results (e.g. pitch type, velocity, and location).

    Args:
        pitches (DataFrame): The list of most similar pitches to the context given previously.
    
    Returns:
        DataFrame: The DataFrame of statistics related to the most likely pitches.
    """
    logger.info('Attempting to digest pitch data')

    df = pd.DataFrame({
        "pitch_type": [],
        "frequency": [],
        "avg_speed": [],
        "avg_release_x": [],
        "avg_release_y": [],
        "avg_release_z": [],
        "avg_plate_x": [],
        "avg_plate_z": [],
    })

    all_pitch_types = pitches['pitch_type'].unique()

    for pitch_type in all_pitch_types:
        frequency_this = pitches.loc[pitches['pitch_type'] == pitch_type, 'pitch_type'].__len__() / pitches.__len__()
        avg_speed_this = pitches.loc[pitches['pitch_type'] == pitch_type, 'release_speed'].mean()
        avg_release_x_this = pitches.loc[pitches['pitch_type'] == pitch_type, 'release_pos_x'].mean()
        avg_release_y_this = pitches.loc[pitches['pitch_type'] == pitch_type, 'release_pos_y'].mean()
        avg_release_z_this = pitches.loc[pitches['pitch_type'] == pitch_type, 'release_pos_z'].mean()
        avg_plate_x_this = pitches.loc[pitches['pitch_type'] == pitch_type, 'plate_x'].mean()
        avg_plate_z_this = pitches.loc[pitches['pitch_type'] == pitch_type, 'plate_z'].mean()

        row_this = pd.DataFrame({
            "pitch_type": [pitch_type],
            "frequency": [frequency_this],
            "avg_speed": [avg_speed_this],
            "avg_release_x": [avg_release_x_this],
            "avg_release_y": [avg_release_y_this],
            "avg_release_z": [avg_release_z_this],
            "avg_plate_x": [avg_plate_x_this],
            "avg_plate_z": [avg_plate_z_this],
        })

        df = pd.concat([df, row_this], ignore_index=True)
    
    df = df.sort_values(by='frequency', ascending=False)

    logger.info('Pitch data digested successfully')
    return df

def digest_pitch_event_data(pitches: pd.DataFrame) -> pd.DataFrame:
    """
    Given the DataFrame of most similar pitches, analyze the data and return a DataFrame of the results (e.g. event type, frequency, etc.).

    Args:
        pitches (DataFrame): The list of most similar pitches to the context given previously.
    
    Returns:
        DataFrame: The DataFrame of statistics related to the most likely events.
    """
    logger.info('Attempting to digest pitch event data')

    df = pd.DataFrame({
        "event": [],
        "frequency": [],
        "pitch_most_common": [],
        "pitch_most_common_frequency": [],
        "avg_speed": [],
        "avg_release_x": [],
        "avg_release_y": [],
        "avg_release_z": [],
        "avg_plate_x": [],
        "avg_plate_z": [],
    })

    all_event_types = pitches['description'].unique()

    for event_type in all_event_types:
        frequency_this = pitches.loc[pitches['description'] == event_type, 'description'].__len__() / pitches.__len__()
        pitch_most_common_this = Counter(pitches.loc[pitches['description'] == event_type, 'pitch_type']).most_common()[0][0]
        pitch_most_common_frequency_this = Counter(pitches.loc[pitches['description'] == event_type, 'pitch_type']).most_common()[0][1] / pitches.loc[pitches['description'] == event_type, 'description'].__len__()
        avg_speed_this = pitches.loc[pitches['description'] == event_type, 'release_speed'].mean()
        avg_release_x_this = pitches.loc[pitches['description'] == event_type, 'release_pos_x'].mean()
        avg_release_y_this = pitches.loc[pitches['description'] == event_type, 'release_pos_y'].mean()
        avg_release_z_this = pitches.loc[pitches['description'] == event_type, 'release_pos_z'].mean()
        avg_plate_x_this = pitches.loc[pitches['description'] == event_type, 'plate_x'].mean()
        avg_plate_z_this = pitches.loc[pitches['description'] == event_type, 'plate_z'].mean()
    
        row_this = pd.DataFrame({
            "event": [event_type],
            "frequency": [frequency_this],
            "pitch_most_common": [pitch_most_common_this],
            "pitch_most_common_frequency": [pitch_most_common_frequency_this],
            "avg_speed": [avg_speed_this],
            "avg_release_x": [avg_release_x_this],
            "avg_release_y": [avg_release_y_this],
            "avg_release_z": [avg_release_z_this],
            "avg_plate_x": [avg_plate_x_this],
            "avg_plate_z": [avg_plate_z_this],
        })

        df = pd.concat([df, row_this], ignore_index=True)

    df = df.sort_values(by='frequency', ascending=False)

    logger.info('Pitch event data digested successfully')
    return df

def digest_pitch_batted_ball_data(pitches: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """
    Given the DataFrame of most similar pitches, analyze the data and return a DataFrame of batted ball data for these pitches.

    Args:
        pitches (DataFrame): The list of most similar pitches to the context given previously.
    
    Returns:
        DataFrame: The DataFrame of statistics related to batted ball data.
        int: The number of batted balls being sampled.
    """
    logger.info('Attempting to digest batted ball data (aggregated)')

    bbe = pitches.loc[pitches['description'] == 'hit_into_play']

    ev = bbe['launch_speed'].mean()
    la = bbe['launch_angle'].mean()
    ba_est = bbe['estimated_ba_using_speedangle'].mean()
    woba_est = bbe['estimated_woba_using_speedangle'].mean()
    woba = bbe['woba_value'].mean()
    babip = bbe['babip_value'].mean()
    iso = bbe['iso_value'].mean()

    logger.info('Batted ball data (aggregated) digested successfully')
    return pd.DataFrame({
        "ev": [ev],
        "la": [la],
        "ba_est": [ba_est],
        "woba_est": [woba_est],
        "woba": [woba],
        "babip": [babip],
        "iso": [iso]
    }), bbe.__len__()

def digest_pitch_batted_ball_data_split(pitches: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """
    Similar to digest_pitch_batted_ball_data, but split by event type.

    Args:
        pitches (DataFrame): The list of most similar pitches to the context given previously.
    
    Returns:
        DataFrame: The DataFrame of statistics related to batted ball data.
        int: The number of batted balls in this sample.
    """
    logger.info('Attempting to digest batted ball data (split)')

    bbe = pitches.loc[pitches['description'] == 'hit_into_play']

    df = pd.DataFrame({
        "event": [],
        "frequency": [],
        "ev": [],
        "la": [],
        "ba_est": [],
        "woba_est": []
    })

    all_event_types = bbe['events'].unique()

    for event_type in all_event_types:
        frequency_this = bbe.loc[bbe['events'] == event_type, 'events'].__len__() / bbe.__len__()
        ev_this = bbe.loc[bbe['events'] == event_type, 'launch_speed'].mean()
        la_this = bbe.loc[bbe['events'] == event_type, 'launch_angle'].mean()
        ba_est_this = bbe.loc[bbe['events'] == event_type, 'estimated_ba_using_speedangle'].mean()
        woba_est_this = bbe.loc[bbe['events'] == event_type, 'estimated_woba_using_speedangle'].mean()

        row_this = pd.DataFrame({
            "event": [event_type],
            "frequency": [frequency_this],
            "ev": [ev_this],
            "la": [la_this],
            "ba_est": [ba_est_this],
            "woba_est": [woba_est_this]
        })

        df = pd.concat([df, row_this], ignore_index=True)

    df = df.sort_values(by='frequency', ascending=False)

    logger.info('Batted ball data (split) digested successfully')
    return df, bbe.__len__()