# Project Penney

## Overview
This **Version** of Penney's Game is played by two players and one deck of cards. More info about Penney's Game can be find: https://en.wikipedia.org/wiki/Penney%27s_game. Each player chooses a three-card sequence of colors (i.e., Red or Black) and cards are drawn face-up until one of the selected sequences appears (e.g., RRR, or BRB). The Game has two variations.

The **first variation** tallies the **total number of cards** from the initial draw until a chosen sequence appears. All cards in the pile are awarded to the player whose sequence is detected. The process repeats until the deck is exhausted; any remaining cards in the pile are discarded.

The **second variation** counts the **number of tricks** a player scores. Each time a player's sequence appears, their trick count increases by 1. This variation continues until the deck runs out.

Below, you can find details on how the project simulates the game, manages and stores our simulation data, and produces heatmaps for visual insights. The repository is organized into dedicated modules for data generation, management, and visualization, along with main scripts to run the simulation pipeline:

- `src/DataGeneration/DataGen.py`
- `src/Management/ProcessData.py`
- `src/Visualization/Visualization.py`
- `src/PenneyGame/Penney.py`
- `RunSim.py`

## src/DataGeneration/DataGen.py
This module is responsible for generating shuffled decks of cards used in the simulations.

**Function:** `get_decks(n_decks, seed, half_deck_size, append=False)`

Parameters:
- `n_decks` (int): Number of decks to generate.

- `seed` (int): Seed for random number generation.

- `half_deck_size` (int): Number of cards in each half-deck (default is 26, forming a 52-card deck).

- `append` (bool): Indicates whether to append new decks to an existing simulation file.

Functionality:
- Creates a "data" directory to store deck files and RNG state.

- Generates decks by using NumPy to create an array containing 26 instances of `0` (one color) and 26 instances of `1` (the other color), then shuffles each deck.

- Supports appending to previous simulation data by restoring the random number generator (RNG) state from a JSON file, ensuring continuity between simulation runs.

- Saves decks in multiple `.npy` files, each containing a maximum of 50,000 decks.

- Saves the final RNG state for future appending operations.

This function forms the foundation of the simulation by ensuring that the decks are randomized reproducibly, reflecting the inherent randomness of Penney’s Game.

---

## src/Management/ProcessData.py
This module processes the simulation data, providing functions to load decks and analyze them using both game variations.

**Function**: `load_simulation(data_dir, seed)`

Parameter:
- `data_dir` (str): The directory containing all the decks in `.npy` files.
- `seed` (int): The seed used for the simulation.

  
Functionality:
- Searches for all .npy files in the specified directory that match the pattern `decks_{seed}_*.npy`.
- Sorts the found files to ensure consistent loading order.
- Raises a `FileNotFoundError` if no matching deck files are found.
- Loads each `.npy` file and appends its contents to a list.
- Concatenates all loaded decks into a single NumPy array.

This function is crucial for retrieving previously generated deck data, allowing for efficient loading of large simulations split across multiple files. It ensures that all decks associated with a specific seed are properly loaded and combined, facilitating further analysis and processing in the Penney's Game simulation.

**Function**: `cards(decks, player1_sequence, player2_sequence)`

Parameters:
- `decks` (np.ndarray): Array of decks generated from the simulation.
- `player1_sequence` (str): Three-digit binary sequence selected by player 1.
- `player2_sequence` (str): Three-digit binary sequence selected by player 2.

Functionality:
- Iterates through each deck to simulate the pile-based scoring approach.

- Detects the occurrence of player sequences.

- When a sequence match is found, awards the accumulated cards (plus additional fixed points) and resets the pile.

- Returns arrays with the cumulative card scores for player 1 and player 2 respectively.

**Function**: `tricks(decks, player1_sequence, player2_sequence)`

Parameters: As in the `cards` function.

Functionality:
- Similar to cards, but instead of tallying cards, counts each occurrence of a player's sequence as a "trick."

- Increments the trick counter every time a matching sequence is detected.

- Returns arrays containing the trick counts for player 1 and player 2.

**Function**: `all_combinations(data_dir, seed, append=False)`

Parameter:
- `data_dir` (str): Directory containing the deck files.
- `seed` (int): Seed used for the simulation.
- `append` (bool): Whether to append to existing data or start fresh.

Functionality:
- Generates all possible distinct pairs of 3-bit sequences (e.g., '000', '001', … '111').

- Loads existing or creates new DataFrames for storing results.

- Processes new decks and combines results with existing data if appending.

- Calculates win percentages and tie rates for all sequence combinations.

- Utilizes tqdm to provide a progress bar during this potentially time-intensive computation.

- Saves updated results and processed deck counts.

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

**Function**:`display_processed_decks()`

Functionality:
- Scans the 'data' directory for files matching the pattern `processed_decks_count_*.txt`.
- Extracts the seed number from each filename.
- Loads and displays the count of processed decks for each seed.
- Provides a summary of previously processed simulations.


**Function**:`get_user_input()`

Functionality:
- Prompts the user to enter the number of decks to generate.
- Prompts the user to enter a seed for the simulation.
- Returns a tuple containing the number of decks and the seed as integers.


**Function**:`run_sim(n_decks, seed, half_deck_size=26, append=False, filename="simulation_results", vmin=0, vmax=100)`

Parameters:
- `n_decks` (int): Number of decks to simulate.

- `seed` (int): Seed for reproducible shuffling.

- `half_deck_size` (int): Number of cards per half-deck.

- `append` (bool): Whether to append to existing simulation data.

- `filename` (str): Base filename for saving heatmaps.

- `vmin`, `vmax` (float): Bounds for the heatmap color scale.

Functionality:
- Orchestrates the entire simulation pipeline:

    - Generates shuffled decks using the get_decks function.

    - Analyzes all combinations of sequences using the all_combinations function.

    - Produces heatmaps for visual insights using the generate_heatmaps function.

- Provides progress updates throughout the simulation process.

- Returns A tuple containing two matplotlib Figure objects: heatmaps for cards-based and tricks-based results.

This end-to-end pipeline encapsulates the simulation process, from deck generation through to result visualization, and is key to exploring the strategic dynamics of Penney's Game.

---
## RunSim.py
This script demonstrates how to use the simulation pipeline.

Functionality:

- Serves as the entry point for the Penney's Game simulation.

- Orchestrates the workflow:
    - Displays a welcome message.

    - Shows existing simulation data via `display_processed_decks()`.

    - Collects user input for deck count and seed via `get_user_input()`.

    - Automatically detects if the provided seed exists and sets `append=True` if applicable.

    - Executes the full simulation pipeline by calling `run_sim()`.


This function provides a user-friendly interface for interacting with the simulation system, abstracting complexity while maintaining full reproducibility and data continuity. You can run this script to quickly generate new simulation data and visualize the patterns observed in Penney’s Game.

---

## The Goal / Moving Forward
The heatmaps derived from both versions of Penney's Game indicate that despite slight differences in winning percentages between the two variations, there is a consistent pattern regarding the advantage of particular sequences. This insight supports the idea that even with inherent randomness, some sequences provide a statistically higher chance of winning. Future work will focus on further refining the simulation parameters and exploring additional visualization techniques to deepen our understanding of the strategic aspects of Penney's Game.