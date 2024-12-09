"""
pitchpredict/src/models/pitch.py
Created by Addison Kline (akline@baseball-analytica.com) in October 2024
"""
# external imports
from pydantic import BaseModel

class Pitch(BaseModel):
    pitcher_id: int
    batter_id: int
    balls: int
    strikes: int
    score_bat: int
    score_fld: int
    game_year: int
    # game_month: int
