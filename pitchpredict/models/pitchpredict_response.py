"""
pitchpredict/src/models/pitchpredict_response.py
Created by Addison Kline (akline@baseball-analytica.com) in December 2024
"""
# external imports
from pydantic import BaseModel
from pandas import DataFrame
from datetime import datetime, timedelta
# internal imports
from pitchpredict.models.pitch import Pitch

class PitchPredictResponse(BaseModel):
    # data (input)
    input_pitch: Pitch
    # data (output)
    basic_pitch_data: DataFrame
    pitch_event_data: DataFrame
    bbe_data_agg: DataFrame
    bbe_data_split: DataFrame
    n_pitches: int
    n_bbe: int
    # metadata
    timestamp: datetime
    time_elapsed: timedelta

    class Config:
        arbitrary_types_allowed=True