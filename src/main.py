"""
pitchpredict/src/main.py
Created by Addison Kline (akline@baseball-analytica.com) in October 2024
"""
import pandas as pd
import datetime
from src.logger_config import get_logger
from src.player_lookup import get_player_id_by_name
from src.fetch_pitch_data import (
    get_pitches_from_pitcher,
    get_most_similar_pitches
)
from src.analyze_pitch_data import (
    digest_pitch_data,
    digest_pitch_event_data,
    digest_pitch_batted_ball_data,
    digest_pitch_batted_ball_data_split
)
from src.models.pitch import Pitch

# logger stuff
logger = get_logger(__name__)

# config stuff
config = pd.read_json('config.json').iloc[0]

# so all information is visible
pd.options.display.max_columns = None

def main() -> None:
    version = "-1"
    with open('version', 'r') as f:
        version = f.read().strip()

    logger.info('PitchPredict started successfully')

    # preamble
    print(80 * '=')
    print(f'PitchPredict v{version}')
    print(f'Created by Addison Kline (akline@baseball-analytica.com)')
    print(80 * '=')

    # get user input for pitcher name
    pitcher_name = input("Please enter the pitcher's full name (first and last): ")
    pitcher_id = get_player_id_by_name(name=pitcher_name)

    # get pitch context from user
    batter_name = input("Please enter the batter's full name (first and last): ")
    batter_id = get_player_id_by_name(name=batter_name)

    # now get the rest of the context from user
    num_balls = int(input("Please enter the number of balls in the count: "))
    num_strikes = int(input("Please enter the number of strikes in the count: "))
    score_bat = int(input("Please enter the batting team's current score, in runs: "))
    score_fld = int(input("Please enter the pitching team's current score, in runs: "))
    game_year = int(input("Please enter the game year: "))

    # create context object with given information
    context = Pitch(
        pitcher_id=pitcher_id,
        batter_id=batter_id,
        balls=num_balls,
        strikes=num_strikes,
        score_bat=score_bat,
        score_fld=score_fld,
        game_year=game_year
    )
    logger.info(f'Context with pitcher_id={pitcher_id}, batter_id={batter_id}, balls={num_balls}, strikes={num_strikes}, score_bat={score_bat}, score_fld={score_fld}, game_year={game_year} created successfully')

    # get all pitches from this pitcher
    pitches = get_pitches_from_pitcher(pitcher_id=pitcher_id)

    # get pitcher's most relevant pitches to the given context
    most_similar_pitches = get_most_similar_pitches(pitches=pitches, this_pitch=context)

    logger.info('Attempting to digest and print pitch data')

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

    logger.info('Pitch data digested and printed successfully')

    # generate output files, if desired
    output = config.get('generate_output_files')
    if output:
        logger.info('Attempting to generate output files')

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        pitch_data.to_csv(f'outputs/data_pitch_{timestamp}.csv')
        pitch_event_data.to_csv(f'outputs/data_event_{timestamp}.csv')
        bbe_data_agg.to_csv(f'outputs/data_bbe_agg_{timestamp}.csv')
        bbe_data_split.to_csv(f'outputs/data_bbe_split_{timestamp}.csv')

        print(80 * '-')
        print(f'Generated output files with timestamp = {timestamp}')
        print(80 * '-')

        logger.info('Output files generated successfully')

    print(80 * '=')

    logger.info('PitchPredict finished executing successfully')

if __name__ == "__main__":
    main()

#print(statcast_pitcher(start_dt="2008-04-01", end_dt="2024-10-01", player_id=519242))