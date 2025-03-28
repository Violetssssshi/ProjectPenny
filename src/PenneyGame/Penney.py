import os
from src.Management.ProcessData import load_simulation, all_combinations, load_processed_decks_count
from src.DataGeneration.DataGen import get_decks
from src.Visualization.Visualization import generate_heatmaps


def display_processed_decks():
    """
    Display the number of previously processed decks for each seed.
    
    This function reads the 'processed_decks_count_*.txt' files in the 'data' directory
    and prints the number of decks processed for each seed.
    """

    print("Previously processed decks:")
    data_dir = "data"
    for file in os.listdir(data_dir):
         # Check if the file matches the expected format
        if file.startswith("processed_decks_count_") and file.endswith(".txt"):
             # Extract the seed from the filename
            seed = file.split("_")[-1].split(".")[0]
            # Load the count of processed decks for this seed
            count = load_processed_decks_count(int(seed))
            # Print the seed and its corresponding deck count
            print(f"Seed {seed}: {count} decks")

def get_user_input():
    """
    Prompt the user for input on the number of decks to generate and the seed for the simulation.
    
    Returns:
        tuple: A tuple containing the number of decks (int) and the seed (int).
    """
    n_decks = int(input("Enter the number of decks to generate: "))
    seed = int(input("Enter the seed for the simulation: "))
    return n_decks, seed

def run_sim(
    n_decks: int,
    seed: int,
    half_deck_size: int = 26,
    append: bool = False,
    filename: str = "simulation_results",
    vmin: float = 0,
    vmax: float = 100
):
    """
    Runs the entire simulation pipeline:
    1. Generates shuffled decks.
    2. Simulates both game variations (cards and tricks).
    3. Analyzes all combinations of sequences.
    4. Produces heatmaps for visual insights.

    Parameters:
        n_decks (int): Number of decks to generate.
        seed (int): Seed for reproducibility.
        half_deck_size (int): Number of cards in each half-deck (default is 26).
        append (bool): Whether to append to existing deck data (default is False).
        filename (str): Base filename for saving heatmaps (default is "simulation_results").
        vmin (float): Minimum value for heatmap color scale (default is 0).
        vmax (float): Maximum value for heatmap color scale (default is 100).

    Returns:
        tuple[plt.Figure, plt.Figure]: Heatmaps for cards-based and tricks-based results.
    """

     # Step 1: Generate shuffled decks
    print(f"Generating {n_decks} decks with seed {seed}...")
    data_dir = get_decks(n_decks, seed, half_deck_size, append)

    # Step 2: Analyze all combinations of sequences
    print("Analyzing all combinations...")
    cards_data, tricks_data = all_combinations(data_dir, seed, append)

    # Step 3: Generate heatmaps
    print("Generating heatmaps...")
    fig_cards, fig_tricks = generate_heatmaps(cards_data, tricks_data, filename, vmin, vmax)

    print("Simulation complete!")
    return fig_cards, fig_tricks