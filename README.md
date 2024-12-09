# PitchPredict
Cutting-edge MLB pitch-predicting software utilizing the latest Statcast data. Open-source and free to use. Brought to you by [baseball-analytica.com].

[baseball-analytica.com]: https://baseball-analytica.com

## Installation (Package)
1. Ensure you have Python v3.11 or above
2. Run the command `pip install pitchpredict`

## Installation (CLI)
1. Clone the repository
2. Create a Python v3.11+ virtual environment: `python3.11 -m venv {your venv name here}`
3. Activate your virtual environment: `source {your venv name here}/bin/activate`
4. Install the requirements: `pip intall -r requirements.txt`
5. You're all set!

## Using the API
To use the `PitchPredict` API in your project, first ensure it is installed correctly. More info coming soon!

## Running the CLI
To run `PitchPredict`, make sure the software is install correctly by following the directions above. Then, run the command `python -m pitchpredict.cli` and follow the prompts. For every successful query, resulting data is a) printed to the console and b) written to files in the designated `outputs` folder. For debugging purposes, `PitchPredict` generates log files in the `logs` folder. These may be helpful if you run into any issues.

## Methodology
Broadly speaking, `PitchPredict` estimates the most likely outcomes for a pitch in the given context by doing the following:
1. For a given pitcher, find all pitches they have thrown in the Statcast era.
2. Find the pitches thrown by this pitcher in contexts most similar to the one given by the user.
3. Analyze said set of pitches and return the resulting analysis to the pitcher
For more information on how similarity is defined and calculated, check out the Similarity section below. For more information on how `PitchPredict` works in general, feel free to check out the source code in the `src` folder.

## Similarity
`PitchPredict` asks the user to provide a given pitch context: the pitcher, the batter, the count, the game score, and the game date. All these are then compared to the list of all pitches thrown previously by the pitcher, and the ones that are most similar (the 0.5% of pitches most similar, based on context, by default) are returned. Similarity scores are calculated for all pitches thrown by the pitcher based on the following factors:
1. Whether or not the batter faced was the same as the one specified by the user.
2. Whether or not the count is the same as the count specified by the user.
3. The difference between the net score (fielding team runs - batting team runs) and the net score specified by the user.
4. The difference between the year the game took place and the year specified by the user.
The final similarity score for each pitch is a weighted average of the individual similarity values calculated above.

## Acknowledgements
`PitchPredict` would not be possible without [pybaseball], the open-source and MIT-licensed baseball data scraping library. The baseball data itself largely comes from [Statcast], but [Baseball-Reference] and [FanGraphs] are sources as well. 

[pybaseball]: https://github.com/jldbc/pybaseball
[Statcast]: https://baseballsavant.mlb.com/statcast_search
[Baseball-Reference]: https://www.baseball-reference.com/
[FanGraphs]: https://www.fangraphs.com/
