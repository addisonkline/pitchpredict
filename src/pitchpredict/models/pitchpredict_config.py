"""
pitchpredict/src/models/pitchpredict_config.py
Created by Addison Kline (akline@baseball-analytica.com) in October 2024
"""
# external imports
from pydantic import BaseModel

class PitchPredictConfig(BaseModel):
    start_date: str # must be "YYYY-MM-DD"
    end_date: str # must be "YYYY-MM-DD" or "today"
    fuzzy_player_lookup: bool
    pitch_sample_pctg: float    