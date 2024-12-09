"""
pitchpredict/src/main.py
Created by Addison Kline (akline@baseball-analytica.com) in October 2024
"""
# external imports
from typing import Any
import pandas as pd
import datetime
# internal imports
# from pitchpredict.logger_config import get_logger
from pitchpredict.models.pitchpredict_config import PitchPredictConfig
from pitchpredict.player_lookup import get_player_id_by_name
from pitchpredict.fetch_pitch_data import (
    get_pitches_from_pitcher,
    get_most_similar_pitches
)
from pitchpredict.analyze_pitch_data import (
    digest_pitch_data,
    digest_pitch_event_data,
    digest_pitch_batted_ball_data,
    digest_pitch_batted_ball_data_split
)
from pitchpredict.models.pitch import Pitch

# logger stuff
#logger = get_logger(__name__)

# config stuff
_config = pd.read_json('config.json').iloc[0]

# so all information is visible
pd.options.display.max_columns = 16

def generate_config_object_from_series(series: pd.Series) -> PitchPredictConfig:
    """
    Attempt to turn the info stored in `config.json` for the CLI into a valid `PitchPredictConfig` format.
    """
    keys = {
        "start_date": str,
        "end_date": str,
        "fuzzy_player_lookup": bool,
        "pitch_sample_pctg": float,
        "generate_output_files": bool
    }
    results: list = []

    for key in keys.keys():
        value = series.get(key)

        #assert isinstance(value, keys[key])

        results.append(value)
    
    return PitchPredictConfig(
        start_date=results[0],
        end_date=results[1],
        fuzzy_player_lookup=results[2],
        pitch_sample_pctg=results[3]
    )

def validate_year(year: str) -> bool:
    """
    Validator fucntion for verifying if a given year is a valid input.
    """
    if not year.isdigit():
        return False
    # only goes here if year is int
    return int(year) >= 2008

def validate_score(score: str) -> bool:
    """
    Validator function for verifying if a given score is a valid input.
    """
    if not score.isdigit():
        return False
    # only goes here if score is int
    return int(score) >= 0

def validate_balls(balls: str) -> bool:
    """
    Validator function for verifying if a given ball is a valid input.
    """
    if not balls.isdigit():
        return False
    # only goes here if balls is int
    return int(balls) < 4 and int(balls) >= 0

def validate_strikes(strikes: str) -> bool:
    """
    Validator function for verifying if a given strike is a valid input.
    """
    if not strikes.isdigit():
        return False
    # only goes here if strikes is int
    return int(strikes) < 3 and int(strikes) >= 0

def validate_player_name(player_name: str) -> bool:
    """
    Validator function for verifying if a given player_name is a valid input.
    """
    # TODO
    return True

def attempt_user_input(prompt: str, validator) -> str | int:
    """
    Given a prompt, attempt to get the relevant user input.
    """
    while True:
        user_input = input(prompt)
        if validator(user_input):
            return user_input
        else:
            print("Input invalid, please try again.")

def main() -> None:
    version = "-1"
    with open('version', 'r') as f:
        version = f.read().strip()

    #logger.info('PitchPredict started successfully')

    # refactor config file
    config = generate_config_object_from_series(_config)

    # preamble
    print(80 * '=')
    print(f'PitchPredict v{version}')
    print(f'Created by Addison Kline (akline@baseball-analytica.com)')
    print(80 * '=')

    # get user input for pitcher name
    pitcher_name = attempt_user_input("Please enter the pitcher's full name (first and last): ", validate_player_name)
    assert isinstance(pitcher_name, str)
    pitcher_id = get_player_id_by_name(name=pitcher_name, config=config)

    # get pitch context from user
    batter_name = attempt_user_input("Please enter the batter's full name (first and last): ", validate_player_name)
    assert isinstance(batter_name, str)
    batter_id = get_player_id_by_name(name=batter_name, config=config)

    # now get the rest of the context from user
    num_balls = attempt_user_input("Please enter the number of balls in the count: ", validate_balls)
    num_strikes = attempt_user_input("Please enter the number of strikes in the count: ", validate_strikes)
    score_bat = attempt_user_input("Please enter the batting team's current score, in runs: ", validate_score)
    score_fld = attempt_user_input("Please enter the pitching team's current score, in runs: ", validate_score)
    game_year = attempt_user_input("Please enter the game year: ", validate_year)

    # create context object with given information
    context = Pitch(
        pitcher_id=pitcher_id,
        batter_id=batter_id,
        balls=int(num_balls),
        strikes=int(num_strikes),
        score_bat=int(score_bat),
        score_fld=int(score_fld),
        game_year=int(game_year)
    )
    #logger.info(f'Context with pitcher_id={pitcher_id}, batter_id={batter_id}, balls={num_balls}, strikes={num_strikes}, score_bat={score_bat}, score_fld={score_fld}, game_year={game_year} created successfully')

    # get all pitches from this pitcher
    pitches = get_pitches_from_pitcher(pitcher_id=pitcher_id, config=config)

    # get pitcher's most relevant pitches to the given context
    most_similar_pitches = get_most_similar_pitches(pitches=pitches, this_pitch=context, config=config)

    #logger.info('Attempting to digest and print pitch data')

    # print basic pitch data
    pitch_data = digest_pitch_data(pitches=most_similar_pitches)
    print(80 * '-')
    print(f'Basic Pitch Data (n = {most_similar_pitches.__len__()})')
    print(80 * '-')
    print(pitch_data)
    
    # print pitch event data
    pitch_event_data = digest_pitch_event_data(pitches=most_similar_pitches)
    print(80 * '-')
    print(f'Pitch Event Data (n = {most_similar_pitches.__len__()})')
    print(80 * '-')
    print(pitch_event_data)

    # print batted ball data (agg)
    bbe_data_agg, bbe_events = digest_pitch_batted_ball_data(pitches=most_similar_pitches)
    print(80 * '-')
    print(f'Batted Ball Event Data (Aggregated) (n = {bbe_events})')
    print(80 * '-')
    print(bbe_data_agg)

    # print batted ball data (split)
    bbe_data_split, bbe_events = digest_pitch_batted_ball_data_split(pitches=most_similar_pitches)
    print(80 * '-')
    print(f'Batted Ball Event Data (Split) (n = {bbe_events})')
    print(80 * '-')
    print(bbe_data_split)

    #logger.info('Pitch data digested and printed successfully')

    # generate output files, if desired
    output = _config.get('generate_output_files')
    if output:
        #logger.info('Attempting to generate output files')

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        pitch_data.to_csv(f'outputs/data_pitch_{timestamp}.csv')
        pitch_event_data.to_csv(f'outputs/data_event_{timestamp}.csv')
        bbe_data_agg.to_csv(f'outputs/data_bbe_agg_{timestamp}.csv')
        bbe_data_split.to_csv(f'outputs/data_bbe_split_{timestamp}.csv')

        print(80 * '-')
        print(f'Generated output files with timestamp = {timestamp}')
        print(80 * '-')

        #logger.info('Output files generated successfully')

    print(80 * '=')

    #logger.info('PitchPredict finished executing successfully')

if __name__ == "__main__":
    main()

#print(statcast_pitcher(start_dt="2008-04-01", end_dt="2024-10-01", player_id=519242))