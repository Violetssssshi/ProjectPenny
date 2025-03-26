import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os

def generate_heatmaps(cards_data: pd.DataFrame, tricks_data: pd.DataFrame, filename: str, vmin: float = 0, vmax: float = 100):
    """
    Generates two heatmaps for cards-based and tricks-based results with Player 1 on the x-axis and Player 2 on the y-axis.
    Includes tie percentages in parentheses, shows sample size in the title, and saves as SVG files.

    Parameters:
        cards_data (pd.DataFrame): DataFrame with cards-based simulation data.
        tricks_data (pd.DataFrame): DataFrame with tricks-based simulation data.
        filename (str): Base filename for the generated heatmaps (without extension).
        vmin (float): Minimum value for the heatmap color scale.
        vmax (float): Maximum value for the heatmap color scale.

    Returns:
        tuple[plt.Figure, plt.Figure]: Two Matplotlib figures for the cards and tricks heatmaps.
    """
    # Ensure the output directory exists
    os.makedirs("figures", exist_ok=True)

    # Calculate total number of samples (N) from the first row of cards_data
    try:
        n_samples = (cards_data["Player 1 Wins"] + cards_data["Player 2 Wins"] + cards_data["Draws"]).iloc[0]
    except (KeyError, IndexError):
        n_samples = 0  # Fallback if data is missing

    # Replace '0' with 'B' and '1' with 'R' in sequences for display
    def replace_sequence(seq):
        return seq.replace('0', 'B').replace('1', 'R')

    cards_data["Sequence 1"] = cards_data["Sequence 1"].apply(replace_sequence)
    cards_data["Sequence 2"] = cards_data["Sequence 2"].apply(replace_sequence)
    tricks_data["Sequence 1"] = tricks_data["Sequence 1"].apply(replace_sequence)
    tricks_data["Sequence 2"] = tricks_data["Sequence 2"].apply(replace_sequence)

    # Pivot data for cards-based results (Player 1 on x-axis, Player 2 on y-axis)
    cards_heatmap_data = cards_data.pivot(index="Sequence 2", columns="Sequence 1", values="Player 1 Win %")
    cards_heatmap_ties = cards_data.pivot(index="Sequence 2", columns="Sequence 1", values="Tie %")

    # Pivot data for tricks-based results (Player 1 on x-axis, Player 2 on y-axis)
    tricks_heatmap_data = tricks_data.pivot(index="Sequence 2", columns="Sequence 1", values="Player 1 Win %")
    tricks_heatmap_ties = tricks_data.pivot(index="Sequence 2", columns="Sequence 1", values="Tie %")

    # Replace NaN values with zeros before formatting annotations
    cards_heatmap_ties.fillna(0, inplace=True)
    tricks_heatmap_ties.fillna(0, inplace=True)

    # Format annotations to include tie percentages
    def format_annotation(win_percentages, tie_percentages):
        return win_percentages.astype(str) + "(" + tie_percentages.astype(int).astype(str) + ")"

    cards_annotations = format_annotation(cards_heatmap_data.fillna(0), cards_heatmap_ties)
    tricks_annotations = format_annotation(tricks_heatmap_data.fillna(0), tricks_heatmap_ties)

    # Create and save the cards-based heatmap
    fig_cards, ax_cards = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        cards_heatmap_data,
        annot=cards_annotations.values,
        fmt="",
        cmap="Blues",
        vmin=vmin,
        vmax=vmax,
        ax=ax_cards,
        mask=cards_heatmap_data.isnull(),
        linewidths=.5,
        linecolor='black',
        cbar=False
    )
    ax_cards.set_facecolor('black')
    
    # Add title with dynamically calculated sample size
    title_cards = f"Cards-Based Player 1 Winning Probabilities\nN = {n_samples:,}"
    ax_cards.set_title(title_cards, fontsize=16)
    
    ax_cards.set_xlabel("Player 1 Sequence", fontsize=12)
    ax_cards.set_ylabel("Player 2 Sequence", fontsize=12)
    
    # Rotate y-axis labels to horizontal
    ax_cards.set_yticklabels(
        ax_cards.get_yticklabels(),
        rotation=0,
        ha='right'
    )
    
    plt.tight_layout()
    fig_cards.savefig(f"figures/{filename}_cards.svg", format="svg")

    # Create and save the tricks-based heatmap
    fig_tricks, ax_tricks = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        tricks_heatmap_data,
        annot=tricks_annotations.values,
        fmt="",
        cmap="Blues",
        vmin=vmin,
        vmax=vmax,
        ax=ax_tricks,
        mask=tricks_heatmap_data.isnull(),
        linewidths=.5,
        linecolor='black',
        cbar=False
    )
    ax_tricks.set_facecolor('black')
    
    # Add title with dynamically calculated sample size
    title_tricks = f"Tricks-Based Player 1 Winning Probabilities\nN = {n_samples:,}"
    ax_tricks.set_title(title_tricks, fontsize=16)
    
    ax_tricks.set_xlabel("Player 1 Sequence", fontsize=12)
    ax_tricks.set_ylabel("Player 2 Sequence", fontsize=12)
    
    # Rotate y-axis labels to horizontal
    ax_tricks.set_yticklabels(
        ax_tricks.get_yticklabels(),
        rotation=0,
        ha='right'
    )
    
    plt.tight_layout()
    fig_tricks.savefig(f"figures/{filename}_tricks.svg", format="svg")

    return fig_cards, fig_tricks
