from src.Management.ProcessData import load_simulation,all_combinations
from src.DataGeneration.DataGen import get_decks
from src.Visualization.Visualization import generate_heatmaps


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
    print("Generating decks...")
    data_dir = get_decks(n_decks, seed, half_deck_size, append)

    # Step 2: Analyze all combinations of sequences
    print("Analyzing all combinations...")
    cards_data, tricks_data = all_combinations(data_dir, seed, append)

    # Step 3: Generate heatmaps
    print("Generating heatmaps...")
    fig_cards, fig_tricks = generate_heatmaps(cards_data, tricks_data, filename, vmin, vmax)

    print("Simulation complete!")
    return fig_cards, fig_tricks