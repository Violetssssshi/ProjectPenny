# Project Penney

## Overview
Penney's Game is played by two players and one deck of cards. Each player chooses a three-card sequence of colors (i.e., Red or Black) and cards are drawn face-up until one of the selected sequences appears (e.g., RRR, or BRB). Penney's Game has two variations.

The **first variation** tallies the **total number of cards** from the initial draw until a chosen sequence appears. All cards in the pile are awarded to the player whose sequence is detected. The process repeats until the deck is exhausted; any remaining cards in the pile are discarded.

The **second variation** counts the **number of tricks** a player scores. Each time a player's sequence appears, their trick count increases by 1. This variation continues until the deck runs out.

Below, you can find details on how the project simulates the game, manages and stores our simulation data, and produces heatmaps for visual insights. The repository is organized into dedicated modules for data generation, management, and visualization, along with main scripts to run the simulation pipeline:

- `src/DataGeneration/DataGen.py`
- `src/Management/ProcessData.py`
- `src/Visualization/Visualization.py`
- `Penney.py`
- `RunSimExample.py`

## src/DataGeneration/DataGen.py
This module is responsible for generating shuffled decks of cards used in the simulations.

**Function:** `get_decks(n_decks, seed, half_deck_size, append=False)`

Parameters:
- `n_decks` (int): Number of decks to generate.

- `seed` (int): Seed for random number generation.

- `half_deck_size` (int): Number of cards in each half-deck (default is 26, forming a 52-card deck).

- `append` (bool): Indicates whether to append new decks to an existing simulation file.

Functionality:
- Creates the "data" directory if it does not exist.

- Generates decks by using NumPy to create an array containing 26 instances of `0` (one color) and 26 instances of `1` (the other color), then shuffles each deck.

- Supports appending to previous simulation data by restoring the random number generator (RNG) state from a JSON file, ensuring continuity between simulation runs.

- Saves the decks in a `.npy` file and also stores the current RNG state for future appending.

- Returns the file path of the saved decks.

This function forms the foundation of the simulation by ensuring that the decks are randomized reproducibly, reflecting the inherent randomness of Penney’s Game.

---

## src/Management/ProcessData.py
This module processes the simulation data, providing functions to load decks and analyze them using both game variations.

**Function**: `load_simulation(file_path)`

Parameter:
- `file_path` (str): Path to the `.npy` file containing deck data.

  
Functionality:
- Checks if the specified file exists.
- Loads the deck data into a NumPy array from the `.npy` file for further simulation analysis.


**Function**: `cards(decks, player1_sequence, player2_sequence)`

Parameters:
- `decks` (np.ndarray): Array of decks generated from the simulation.
- `player1_sequence` (str): Three-digit binary sequence selected by player 1.
- `player2_sequence` (str): Three-digit binary sequence selected by player 2.

Functionality:
- Iterates through each deck to simulate the pile-based scoring approach.

- Detects the occurrence of player sequences by examining every possible contiguous 3-card window.

- When a sequence match is found, awards the accumulated cards (plus additional fixed points) and resets the pile.

- Returns arrays with the cumulative card scores for player 1 and player 2 respectively.

**Function**: `tricks(decks, player1_sequence, player2_sequence)`

Parameters: As in the `cards` function.

Functionality:
- Similar to cards, but instead of tallying cards, counts each occurrence of a player's sequence as a "trick."

- Increments the trick counter every time a matching sequence is detected.

- Returns arrays containing the trick counts for player 1 and player 2.

**Function**: `all_combinations(decks)`

Parameter:
- `decks` (np.ndarray): Array of simulation decks.

Functionality:
- Generates all possible distinct pairs of 3-bit sequences (e.g., '000', '001', … '111').

- For each pair, simulates both the cards and tricks variations across all decks.

- Computes win counts and calculates Player 1 win percentages.

- Aggregates the results into two Pandas DataFrames – one for each variation.

- Utilizes tqdm to provide a progress bar during this potentially time-intensive computation.

This module offers a comprehensive processing pipeline that enables the analysis of every possible matchup between player sequences, mirroring the game’s strategic depth.


---

## src/Visualization/Visualization.py


The DataVisualization file helps with generating and saving heatmaps for the probability of player 1 winning for every possible combination of color card sequences.

**Function**: `generate_heatmaps(cards_data, tricks_data, filename, vmin=0, vmax=100)`

Parameters:
- `cards_data` (pd.DataFrame): Data from the pile-based game variation.

- `tricks_data` (pd.DataFrame): Data from the trick-based game variation.

- `filename` (str): Base name for the output heatmap image files.

- `vmin` (float): Minimum bound for the heatmap color scale.

- `vmax` (float): Maximum bound for the heatmap color scale.


Functionality:

- Converts binary sequences to more visually intuitive labels by replacing 0 with "B" (Black) and 1 with "R" (Red).

- Pivots the simulation results into matrices appropriate for heatmap visualization.

- Generates two separate heatmaps using Seaborn: one displaying the outcomes of the cards variation and another for the tricks variation.

- Configures the heatmaps with annotations, appropriate color scales, and axis labels.

- Saves the heatmaps as high-resolution PNG images in the "figures" directory.

- Returns the Matplotlib figure objects for further inspection or modification.

By transforming raw simulation data into visually accessible formats, this module helps highlight strategic patterns and probabilities inherent in Penney's Game.

---

## Penney.py
This module serves as the main driver for the simulation pipeline by integrating functions across data generation, management, and visualization.

**Function**:`run_sim(n_decks, seed, half_deck_size=26, append=False, filename="simulation_results", vmin=0, vmax=100)`

Parameters:
- `n_decks` (int): Number of decks to simulate.

- `seed` (int): Seed for reproducible shuffling.

- `half_deck_size` (int): Number of cards per half-deck.

- `append` (bool): Whether to append to existing simulation data.

- `filename` (str): Base filename for saving heatmaps.

- `vmin`, `vmax` (float): Bounds for the heatmap color scale.

Functionality:
- Step 1: Generates shuffled decks using get_decks and saves them.

- Step 2: Loads the generated deck data with load_simulation.

- Step 3: Analyzes all possible sequence matchups by calling all_combinations to simulate both game variations.

- Step 4: Produces heatmaps using generate_heatmaps to visually represent the winning probabilities of Player 1.

- Provides progress updates via print statements throughout the execution.

- Returns the Matplotlib figure objects containing the generated heatmaps.

This end-to-end pipeline encapsulates the simulation process, from deck generation through to result visualization, and is key to exploring the strategic dynamics of Penney's Game.

---
## RunSimExample.py
This script demonstrates how to use the simulation pipeline.

Functionality:

- Imports and reloads the Penney module to ensure the latest version is used.

- Executes the simulation by calling run_sim with specific parameters (e.g., simulating 10,000 decks with seed 42).

- Automatically produces and saves the heatmaps, making it easy to generate new simulation results with minimal setup.

You can run this script to quickly generate new simulation data and visualize the patterns observed in Penney’s Game.

---

## The Goal / Moving Forward
The heatmaps derived from both versions of Penney's Game indicate that despite slight differences in winning percentages between the two variations, there is a consistent pattern regarding the advantage of particular sequences. This insight supports the idea that even with inherent randomness, some sequences provide a statistically higher chance of winning. Future work will focus on further refining the simulation parameters and exploring additional visualization techniques to deepen our understanding of the strategic aspects of Penney's Game.