import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os

def generate_heatmaps(cards_data: pd.DataFrame, tricks_data: pd.DataFrame, filename: str, vmin: float = 0, vmax: float = 100):
    """
    Generates two separate heatmaps: one for cards-based results and one for tricks-based results.
    Saves each heatmap to a separate file and returns the figures.

    Parameters:
        cards_data (pd.DataFrame): DataFrame with cards-based simulation data (from all_combinations).
        tricks_data (pd.DataFrame): DataFrame with tricks-based simulation data (from all_combinations).
        filename (str): Base filename for the generated heatmaps (without extension).
        vmin (float): Minimum value for the heatmap color scale.
        vmax (float): Maximum value for the heatmap color scale.

    Returns:
        tuple[plt.Figure, plt.Figure]: Two Matplotlib figures for the cards and tricks heatmaps.
    """
    # Ensure the output directory exists
    os.makedirs("figures", exist_ok=True)

    # Replace '0' with 'B' and '1' with 'R' in sequences for display
    def replace_sequence(seq):
        return seq.replace('0', 'B').replace('1', 'R')

    cards_data["Sequence 1"] = cards_data["Sequence 1"].apply(replace_sequence)
    cards_data["Sequence 2"] = cards_data["Sequence 2"].apply(replace_sequence)
    tricks_data["Sequence 1"] = tricks_data["Sequence 1"].apply(replace_sequence)
    tricks_data["Sequence 2"] = tricks_data["Sequence 2"].apply(replace_sequence)

    # Pivot data for cards-based results
    cards_heatmap_data = cards_data.pivot(index="Sequence 1", columns="Sequence 2", values="Player 1 Win %")
    
    # Pivot data for tricks-based results
    tricks_heatmap_data = tricks_data.pivot(index="Sequence 1", columns="Sequence 2", values="Player 1 Win %")

    # Create and save the cards-based heatmap
    fig_cards, ax_cards = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        cards_heatmap_data,
        annot=True,
        fmt=".1f",
        cmap="Blues",  # All-blue color scheme
        vmin=vmin,
        vmax=vmax,
        cbar_kws={'label': 'Player 1 Win %'},
        ax=ax_cards,
        mask=cards_heatmap_data.isnull(),  # Mask missing data
        linewidths=.5, linecolor='black'   # Add black lines around cells
    )
    ax_cards.set_facecolor('black')  # Set background color to black for missing data
    ax_cards.set_title("Cards-Based Player 1 Winning Probabilities", fontsize=16)
    ax_cards.set_xlabel("Player 2 Sequence", fontsize=12)
    ax_cards.set_ylabel("Player 1 Sequence", fontsize=12)
    plt.tight_layout()
    fig_cards.savefig(f"figures/{filename}_cards.png", dpi=300)

    # Create and save the tricks-based heatmap
    fig_tricks, ax_tricks = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        tricks_heatmap_data,
        annot=True,
        fmt=".1f",
        cmap="Blues",  # All-blue color scheme
        vmin=vmin,
        vmax=vmax,
        cbar_kws={'label': 'Player 1 Win %'},
        ax=ax_tricks,
        mask=tricks_heatmap_data.isnull(),  # Mask missing data
        linewidths=.5, linecolor='black'   # Add black lines around cells
    )
    ax_tricks.set_facecolor('black')  # Set background color to black for missing data
    ax_tricks.set_title("Tricks-Based Player 1 Winning Probabilities", fontsize=16)
    ax_tricks.set_xlabel("Player 2 Sequence", fontsize=12)
    ax_tricks.set_ylabel("Player 1 Sequence", fontsize=12)
    plt.tight_layout()
    fig_tricks.savefig(f"figures/{filename}_tricks.png", dpi=300)

    # Return both figures for further use if needed
    return fig_cards, fig_tricks
