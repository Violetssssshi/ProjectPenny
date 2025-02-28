# Project Penney

## Overview
Penney's Game is played by two players and one deck of cards. Each player chooses a three-card sequence of colors (i.e. Red or Black) and cards are drawn face-up until one of the selected sequences appear (i.e. RRR, or BRB). Penney's game has two variations. 

The **first variation** tallies the **total number of cards** from the initial draw until a chosen sequence appears. All cards in the pile are given to the player whose sequence appears. This is repeated until the deck runs out; any cards remaining in the pile at the end are not tallied.

The **second variation** counts the **number of "tricks" a player scores** in a game. Each time a player's sequence appears, their number of tricks increases by 1, repeated until the deck runs out.

Below, you may read the documentation on how our group approached simulating the game, managing/storing our data, and visualizing our data as a heatmap. The project includes four files:

- `RunSimulation.py`
- `DataManagement.py`
- `DataVisualization.py`
- `RunEverything.ipynb`

## RunSimulation.py
The RunSimulation file will simulate the shuffling of decks of cards and save the results as a `.npy` file.

`generate_simulation_results(num_iter, output_filename, path)`

Parameters:
- `num_iter` (`int`): the number of decks to create
- `output_filename` (`str`): the file to save the decks in
- `seed`: the seed to use for random generation
- `path` (`str`, optional): the path to save the file in. Defaults to `'data'`

Functionality:
- Creates decks of red and black cards, represented by 52 bits, where `0` is red and `1` is black.
- The 52 bits are shuffled, to represent a random deck with 26 black and 26 red cards.
- Saves the decks as integers and stores them in a `.npy` file.


---

## DataManagement.py
The DataManagement file has several functions associated with storing and processing data for visualization purposes.

`load_process_simulations(path)`

Parameter:
- `path` (`str`): the location of the simulation data from the previous step

  
Functionality:
- Loads simulation data from specified file
- Converts each integer in file to 52-bit binary string
- Returns a list of the binary strings


`variation1`

Parameters:
- `deck` (`str`): deck of cards as binary sequence
- `player1_sequence` (`str`): 3-bit sequence for player 1
- `player2_sequence` (`str`): 3-bit sequence for player 2

Functionality:
- Initialize card counts and pile size
- Iterates through the deck to check for matches with player sequences
- If match is found, matching player receives cards in pile
- Returns `player1_cards, player2_cards`: the number of **cards** collected by each player

`variation2`

Parameters:
- `deck` (`str`): deck of cards as binary sequence
- `player1_sequence` (`str`): 3-bit sequence for player 1
- `player2_sequence` (`str`): 3-bit sequence for player 2

Functionality:
- Initialize trick counters for both players
- Iterates through deck to check for matches with player sequences
- When a match is found, matching player scores one trick
- Returns `player1_tricks, player2_tricks`: number of **tricks** won by each player


`analyze_all_combinations`

Parameter:
- `simulations`: list of binary strings representing games

Functionality:
- Generates all possible player 1 and player 2 sequence combinations 
- For each unique pair of sequences it simulations both variations of the game for each deck in simulations, counts wins for each player in both variations, and calculates win percentages
- Compiles results into two DataFrames, one for each variation


`combine_past_data`

Parameters:
- `new_var1` (`pandas.DataFrame`): New simulation data to be added to old data for variation 1.
- `new_var2` (`pandas.DataFrame`): New simulation data to be added to old data for variation 2.
- `var1_existing_filename` (`str`): The CSV file containing the old data for variation 1.
- `var2_existing_filename` (`str`): The CSV file containing the old data for variation 2.
- `folder` (`str`, optional): Path to the folder containing the CSV files to process. Default is `data`.

  
Functionality:
- Initializes combined DataFrames for each variation using existing data
- Sets ‘Sequence 1’ and ‘Sequence 2’ as index
- Reads CSVs, ensures sequences are 3 digits long, determines which variation the file belongs to, updates corresponding combined DataFrame using `update_dataframe` function
- Resets index of combined DataFrames
- Saves updated DataFrames to CSV files 
- Returns the two updated DataFrames 


`update_dataframe`


Parameters:
- `existing_df` (`pandas.DataFrame`): Existing DataFrame to be updated
- `new_df` (`pandas.DataFrame`): DataFrame containing data to be merged


Functionality:
- If the existing DataFrame is empty, it returns the new DataFrame
- Finds common columns between existing and new DataFrames
- Updates existing DataFrame with values from common columns in new DataFrame
- Recalculates the ‘Player 1 Win %’ based on updated win counts 
- Returns updated DataFrame with merged data and recalculated win percentages 



---

## DataVisualization.py


The DataVisualization file helps with generating and saving heatmaps for the probability of player 1 winning for every possible combination of color card sequences.

Note that the **title of the heatmaps contains an approximation** of the amount of games played. This number is taken from one of the variations. It is approximate because ties are dropped from the data, meaning that each game variation may have slightly different amounts of actual finished, non-tying games.

`generate_heatmap`

Parameters:
- `data`: This is the DataFrame that contains the total results
- `filename`: Name of the file where the heatmap is saved
- `vmin`, `vmax`: Win percentage value bounds for the color scale in the heatmap
- `title`: Title text of the heatmap 


Functionality:

- Takes dataframe of the total Penney's game simulation
- Creates 8 by 8 matrix comparing Player 1 and Player 2
- Fills the matrix with each of the winning probabilities
- The heatmap is created after visualizing the annotated 8 by 8 matrix
- The dark diagonal on the heatmap is set for the sequences that match
- The heatmap is labeled with proper percentages of player 1 wins for each sequence 
- Darker colors represent a higher winning probability; lighter colors represent a lower winning probability

---

## RunEverything.ipynb
The RunEverything notebook allows you, the FLB, to simply run a few lines of code to add new simulations and produce the resulting heatmaps.

---


## The Goal / Moving Forward
Looking at the probabilities of the two version of the penney's game, we can see that while there are differences in some of the percentages for player 1 winning, overall the heatmap shows a similar pattern between both games. This may sort of highlight the idea that no matter what variation of the penney's game are played, the same pattern of some sequences having a more or less advantage exists. Based on our heatmaps, there are some clear instances where one type of sequence from player 1 may beat player 2, but collectively we thought that if the type of sequence chosen was privately that brings a lot of random chance into question. Which ever person chooses the optimal sequence at that point is more likely to win. This could also mean that since there are certain sequences that are more likely to win than others, that might lower the choices one player may take in order to have a more likely chance to win overall games played. 