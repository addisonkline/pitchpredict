"""
pitchpredict/tests/test_api.py
Created by Addison Kline (akline@baseball-analytica.com) in December 2024
"""
# external imports
from datetime import (
    datetime,
    timedelta
)
# internal imports
from pitchpredict.api import PitchPredict
from pitchpredict.models.pitch import Pitch

# module constants
CONFIG_1 = {
    "start_date": "2015-04-01",
    "end_date": "today",
    "fuzzy_player_lookup": True,
    "pitch_sample_pctg": 0.005,
}
CONFIG_2 = {
    "start_date": "2015-04-01",
    "end_date": "today",
    "fuzzy_player_lookup": False,
    "pitch_sample_pctg": 0.005,
}
CONFIG_INVALID_1 = {
    "asfruhiqwer9ouhnsdfv": 19,
}
CONFIG_INVALID_2 = {
    "start_date": "sadgfuhashgiuosfbn",
    "end_date": "today",
    "fuzzy_player_lookup": True,
    "pitch_sample_pctg": 0.005,
}
CONFIG_INVALID_3 = {
    "start_date": "2015-04-01",
    "end_date": "sadgfuhashgiuosfbn",
    "fuzzy_player_lookup": True,
    "pitch_sample_pctg": 0.005,
}
CONFIG_INVALID_4 = {
    "start_date": "2015-04-01",
    "end_date": "today",
    "fuzzy_player_lookup": True,
    "pitch_sample_pctg": 0.0,
}

NAME_PITCHER = "Clayton Kershaw"
NAME_BATTER = "Aaron Judge"
BALLS = 0
STRIKES = 0
SCORE_BAT = 0
SCORE_FLD = 0
GAME_YEAR = 2024

NAME_PITCHER_MALFORMED = "tuiycdvjbnwqertguih"
NAME_BATTER_MALFORMED = "suethvijbnasdrtiugb"
BALLS_MALFORMED = -1
STRIKES_MALFORMED = -1
SCORE_BAT_MALFORMED = -1
SCORE_FLD_MALFORMED = -1
GAME_YEAR_MALFORMED = 2006

def test_invalid_config_1() -> None:
    """
    Test attempting to create a client with invalid config 1.
    """
    correct_err = False
    try:        
        _ = PitchPredict(
            config=CONFIG_INVALID_1
        )
    except ValueError:
        correct_err = True

    assert correct_err

    print("test_invalid_config_1 completed successfully")

def test_invalid_config_2() -> None:
    """
    Test attempting to create a client with invalid config 2.
    """
    correct_err = False
    try:        
        _ = PitchPredict(
            config=CONFIG_INVALID_2
        )
    except ValueError:
        correct_err = True

    assert correct_err

    print("test_invalid_config_2 completed successfully")

def test_invalid_config_3() -> None:
    """
    Test attempting to create a client with invalid config 3.
    """
    correct_err = False
    try:        
        _ = PitchPredict(
            config=CONFIG_INVALID_3
        )
    except ValueError:
        correct_err = True

    assert correct_err

    print("test_invalid_config_3 completed successfully")

def test_invalid_config_4() -> None:
    """
    Test attempting to create a client with invalid config 4.
    """
    correct_err = False
    try:        
        _ = PitchPredict(
            config=CONFIG_INVALID_4
        )
    except ValueError:
        correct_err = True

    assert correct_err

    print("test_invalid_config_4 completed successfully")

def test_all_inputs_valid(client: PitchPredict) -> None:
    """
    Run a prediction using all valid inputs.
    """
    response = client.predict(
        name_pitcher=NAME_PITCHER,
        name_batter=NAME_BATTER,
        balls=BALLS,
        strikes=STRIKES,
        score_bat=SCORE_BAT,
        score_fld=SCORE_FLD,
        game_year=GAME_YEAR
    )

    assert isinstance(response.input_pitch, Pitch)
    assert response.input_pitch.balls == BALLS
    assert response.input_pitch.strikes == STRIKES
    assert response.input_pitch.score_bat == SCORE_BAT
    assert response.input_pitch.score_fld == SCORE_FLD
    assert response.input_pitch.game_year == GAME_YEAR
    assert not response.basic_pitch_data.empty
    assert not response.pitch_event_data.empty
    assert not response.bbe_data_agg.empty
    assert not response.bbe_data_split.empty
    assert response.n_pitches > 0
    assert response.n_bbe > 0
    assert isinstance(response.timestamp, datetime)
    assert isinstance(response.time_elapsed, timedelta)

    print("test_all_inputs_valid completed successfully")

def test_invalid_pitcher(client: PitchPredict) -> None:
    """
    Attempt to run a prediction with a malformed input for pitcher name.
    """
    correct_err = False
    try:
        _ = client.predict(
            name_pitcher=NAME_PITCHER_MALFORMED,
            name_batter=NAME_BATTER,
            balls=BALLS,
            strikes=STRIKES,
            score_bat=SCORE_BAT,
            score_fld=SCORE_FLD,
            game_year=GAME_YEAR
        )
    except ValueError:
        correct_err = True

    assert correct_err

    print("test_invalid_pitcher completed successfully")

def test_invalid_batter(client: PitchPredict) -> None:
    """
    Attempt to run a prediction with a malformed input for batter name.
    """
    correct_err = False
    try:
        _ = client.predict(
            name_pitcher=NAME_PITCHER,
            name_batter=NAME_BATTER_MALFORMED,
            balls=BALLS,
            strikes=STRIKES,
            score_bat=SCORE_BAT,
            score_fld=SCORE_FLD,
            game_year=GAME_YEAR
        )
    except ValueError:
        correct_err = True

    assert correct_err

    print("test_invalid_batter completed successfully")

def test_invalid_balls(client: PitchPredict) -> None:
    """
    Attempt to run a prediction with a malformed input for balls.
    """
    correct_err = False
    try:
        _ = client.predict(
            name_pitcher=NAME_PITCHER,
            name_batter=NAME_BATTER,
            balls=BALLS_MALFORMED,
            strikes=STRIKES,
            score_bat=SCORE_BAT,
            score_fld=SCORE_FLD,
            game_year=GAME_YEAR
        )
    except ValueError:
        correct_err = True

    assert correct_err

    print("test_invalid_balls completed successfully")


def test_invalid_strikes(client: PitchPredict) -> None:
    """
    Attempt to run a prediction with a malformed input for strikes.
    """
    correct_err = False
    try:
        _ = client.predict(
            name_pitcher=NAME_PITCHER,
            name_batter=NAME_BATTER,
            balls=BALLS,
            strikes=STRIKES_MALFORMED,
            score_bat=SCORE_BAT,
            score_fld=SCORE_FLD,
            game_year=GAME_YEAR
        )
    except ValueError:
        correct_err = True

    assert correct_err

    print("test_invalid_strikes completed successfully")

def test_invalid_score_bat(client: PitchPredict) -> None:
    """
    Attempt to run a prediction with a malformed input for strikes.
    """
    correct_err = False
    try:
        _ = client.predict(
            name_pitcher=NAME_PITCHER,
            name_batter=NAME_BATTER,
            balls=BALLS,
            strikes=STRIKES,
            score_bat=SCORE_BAT_MALFORMED,
            score_fld=SCORE_FLD,
            game_year=GAME_YEAR
        )
    except ValueError:
        correct_err = True

    assert correct_err

    print("test_invalid_score_bat completed successfully")

def test_invalid_score_fld(client: PitchPredict) -> None:
    """
    Attempt to run a prediction with a malformed input for strikes.
    """
    correct_err = False
    try:
        _ = client.predict(
            name_pitcher=NAME_PITCHER,
            name_batter=NAME_BATTER,
            balls=BALLS,
            strikes=STRIKES,
            score_bat=SCORE_BAT,
            score_fld=SCORE_FLD_MALFORMED,
            game_year=GAME_YEAR
        )
    except ValueError:
        correct_err = True

    assert correct_err

    print("test_invalid_score_fld completed successfully")

def test_invalid_game_year(client: PitchPredict) -> None:
    """
    Attempt to run a prediction with a malformed input for strikes.
    """
    correct_err = False
    try:
        _ = client.predict(
            name_pitcher=NAME_PITCHER,
            name_batter=NAME_BATTER,
            balls=BALLS,
            strikes=STRIKES,
            score_bat=SCORE_BAT,
            score_fld=SCORE_FLD,
            game_year=GAME_YEAR_MALFORMED
        )
    except ValueError:
        correct_err = True

    assert correct_err

    print("test_invalid_game_year completed successfully")

def main():
    """
    Initiate and execute tests for the PitchPredict API.
    """
    # creat client objects, both valid and invalid
    client_valid_1 = PitchPredict(
        config=CONFIG_1
    )
    client_no_fuzzy = PitchPredict(
        config=CONFIG_2
    )

    # execute tests
    # invalid config
    test_invalid_config_1()
    test_invalid_config_2()
    test_invalid_config_3()
    test_invalid_config_4()
    # valid config
    test_all_inputs_valid(client_valid_1)
    test_invalid_pitcher(client_no_fuzzy)
    test_invalid_batter(client_no_fuzzy)
    test_invalid_balls(client_valid_1)
    test_invalid_strikes(client_valid_1)
    test_invalid_score_bat(client_valid_1)
    test_invalid_score_fld(client_valid_1)
    test_invalid_game_year(client_valid_1)

if __name__ == "__main__":
    main()