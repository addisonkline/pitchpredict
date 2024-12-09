"""
pitchpredict/src/_client.py
Created by Addison Kline (akline@baseball-analytica.com) in December 2024
"""
# external imports
import numpy as np
import pandas as pd
import datetime
# internal imports
from pitchpredict.analyze_pitch_data import (
    digest_pitch_batted_ball_data, 
    digest_pitch_data, 
    digest_pitch_event_data,
    digest_pitch_batted_ball_data_split
)
from pitchpredict.fetch_pitch_data import (
    get_most_similar_pitches, 
    get_pitches_from_pitcher
)
from pitchpredict.models.pitchpredict_config import PitchPredictConfig
from pitchpredict.models.pitchpredict_response import PitchPredictResponse
from pitchpredict.models.pitch import Pitch
from pitchpredict.player_lookup import get_player_id_by_name

class PitchPredict:
    _config: PitchPredictConfig

    def __init__(self, config: dict | PitchPredictConfig):
        """
        Constructor for the PitchPredict class.
        """
        if isinstance(config, PitchPredictConfig):
            self._config = config
        elif isinstance(config, dict):
            self._config = self.__generate_config_from_dict(config)
            self.__check_config_validity()
        else:
            raise TypeError(f"parameter `config` in PitchPredict is not a valid type: expected 'dict | PitchPredictConfig', got {type(config)}")
    
    # public methods
    def predict(self, name_pitcher: str, name_batter: str, balls: int, strikes: int, score_bat: int, score_fld: int, game_year: int) -> PitchPredictResponse:
        """
        Predict a pitch using parameters passed in directly.
        """
        pitcher_id = get_player_id_by_name(name=name_pitcher, config=self._config)
        batter_id = get_player_id_by_name(name=name_batter, config=self._config)

        # create context object with given information
        context = Pitch(
            pitcher_id=pitcher_id,
            batter_id=batter_id,
            balls=balls,
            strikes=strikes,
            score_bat=score_bat,
            score_fld=score_fld,
            game_year=game_year
        )

        return self.predict_from_pitch(context)

    def predict_from_pitch(self, pitch: Pitch) -> PitchPredictResponse:
        """
        Predict a pitch using parameters passed in via a `Pitch` object.
        """
        # check for malformed input
        if pitch.balls > 3 or pitch.balls < 0:
            raise ValueError(f"pitch.balls must be between 0 and 3 inclusive, not {pitch.balls}")
        if pitch.strikes > 2 or pitch.strikes < 0:
            raise ValueError(f"pitch.strikes must be between 0 and 2 inclusive, not {pitch.strikes}")
        if pitch.score_bat < 0:
            raise ValueError(f"pitch.score_bat must be at least 0")
        if pitch.score_fld < 0:
            raise ValueError(f"pitch.score_fld must be at least 0")
        if pitch.game_year < 2008:
            raise ValueError(f"pitch.game_year must be at least 2008")

        timestamp_start = datetime.datetime.now()

        # get all pitches from this pitcher
        pitches = get_pitches_from_pitcher(pitcher_id=pitch.pitcher_id, config=self._config)

        # get pitcher's most relevant pitches to the given context
        most_similar_pitches = get_most_similar_pitches(pitches=pitches, this_pitch=pitch, config=self._config)

        # create relevant dataframes
        pitch_data = digest_pitch_data(pitches=most_similar_pitches)
        pitch_event_data = digest_pitch_event_data(pitches=most_similar_pitches)
        bbe_data_agg, bbe_events = digest_pitch_batted_ball_data(pitches=most_similar_pitches)
        bbe_data_split, bbe_events = digest_pitch_batted_ball_data_split(pitches=most_similar_pitches)

        timestamp_end = datetime.datetime.now()

        return PitchPredictResponse(
            # input data
            input_pitch=pitch,
            # output data
            basic_pitch_data=pitch_data,
            pitch_event_data=pitch_event_data,
            bbe_data_agg=bbe_data_agg,
            bbe_data_split=bbe_data_split,
            n_pitches=most_similar_pitches.__len__(),
            n_bbe=bbe_events,
            # metadata
            timestamp=timestamp_start,
            time_elapsed=timestamp_end - timestamp_start
        )

    # private methods
    def __generate_config_from_dict(self, config: dict):
        """
        Given a `config` value of type `dict`, generate a `PitchPredictConfig` object.
        """
        keys = {
            "start_date": str,
            "end_date": str,
            "fuzzy_player_lookup": bool,
            "pitch_sample_pctg": float
        }
        # this one-liner checks that all of the above keys exist in given dictionary
        if np.mean([key in config for key in keys]) == 1:
            # now check the types of all given values
            for key in keys.keys():
                if not isinstance(config[key], keys[key]):
                    raise TypeError(f"config['{key}'] should have type '{keys[key]}', not '{type(config[key])}'")
            
            return PitchPredictConfig(
                start_date=config["start_date"],
                end_date=config["end_date"],
                fuzzy_player_lookup=config["fuzzy_player_lookup"],
                pitch_sample_pctg=config["pitch_sample_pctg"]
            )
        # otherwise, the given dict is malformed
        else:
            raise ValueError(f"parameter 'config' in PitchPredict does not have all the required parameters. params: {keys}")

    def __check_config_validity(self) -> None:
        """
        Assuming a `PitchPredictConfig` object has been successfully created, check that all input values are valid.
        """
        # first, check date params
        if not self._config.end_date == "today":
            if not isinstance(datetime.datetime.fromisoformat(self._config.end_date), datetime.datetime):
                raise ValueError("config.end_date must be be a valid string in the format 'YYYY-MM-DD'")
        if not isinstance(datetime.datetime.fromisoformat(self._config.start_date), datetime.datetime):
            raise ValueError("config.start_date must be be a valid string in the format 'YYYY-MM-DD'")
        
        # now ensure pitch_sample_pctg is valid
        if self._config.pitch_sample_pctg > 1 or self._config.pitch_sample_pctg <= 0:
            raise ValueError("config.pitch_sample_pctg must be between 0 and 1")