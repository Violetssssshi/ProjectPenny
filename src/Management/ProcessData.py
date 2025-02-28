import os
import numpy as np
import itertools
import pandas as pd
from tqdm import tqdm

def load_simulation(file_path: str) -> np.ndarray:
    """
    Loads simulation data from a NumPy (.npy) file containing the decks.

    Parameters:
        file_path (str): The path to the .npy file with the simulation data.

    Returns:
        np.ndarray: An array with all decks stored in the file.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The specified file '{file_path}' does not exist.")
    
    # Load and return the decks from the .npy file
    decks = np.load(file_path)
    return decks


def cards(decks: np.ndarray, player1_sequence: str, player2_sequence: str) -> tuple[np.ndarray, np.ndarray]:
    """
    Simulates the card game where two players compete to collect points based on specific 3-bit sequences.
    Scores are calculated separately for each deck.

    Parameters:
        decks (np.ndarray): An array of decks loaded from the `load_simulation` method.
        player1_sequence (str): The 3-bit sequence chosen by player 1.
        player2_sequence (str): The 3-bit sequence chosen by player 2.

    Returns:
        tuple[np.ndarray, np.ndarray]: Two arrays containing the cards scores for Player 1 and Player 2 for each deck.
    """
    # Initialize arrays to store scores for each deck
    player1_scores = []
    player2_scores = []

    # Iterate over each deck in the array
    for deck in decks:
        player1_cards = 0
        player2_cards = 0
        pile = 0
        i = 0

        # Traverse the deck while ensuring at least 3 cards remain
        while i <= len(deck) - 2:
            # Extract the current 3-character substring
            substring = ''.join(map(str, deck[i:i+3]))
            pile += 1

            if substring == player1_sequence:
                # Player 1 collects the pile
                player1_cards = player1_cards + pile + 2 
                pile = 0
                i += 3  # Jump ahead by 3 to avoid overlapping
            elif substring == player2_sequence:
                # Player 2 collects the pile
                player2_cards = player2_cards + pile + 2
                pile = 0
                i += 3  # Jump ahead by 3 to avoid overlapping
            else:
                # No match, move to the next card
                i += 1

        # Append scores for this deck to the results lists
        player1_scores.append(player1_cards)
        player2_scores.append(player2_cards)

    # Convert results to NumPy arrays and return them
    return np.array(player1_scores), np.array(player2_scores)



def tricks(decks: np.ndarray, player1_sequence: str, player2_sequence: str) -> tuple[np.ndarray, np.ndarray]:
    """
    Simulates a card game variant where points are awarded based on "tricks."
    Each successful sequence detection counts as one trick for the respective player.
    Scores are calculated separately for each deck.

    Parameters:
        decks (np.ndarray): An array of decks loaded from the `load_simulation` method.
        player1_sequence (int): The 3-bit sequence chosen by player 1.
        player2_sequence (int): The 3-bit sequence chosen by player 2.

    Returns:
        tuple[np.ndarray, np.ndarray]: Two arrays containing the trick counts for Player 1 and Player 2 for each deck.
    """
    # Initialize arrays to store trick counts for each deck
    player1_tricks = []
    player2_tricks = []

    # Iterate over each deck in the array
    for deck in decks:
        player1_trick_count = 0
        player2_trick_count = 0
        i = 0

        # Traverse the deck while ensuring at least 3 cards remain
        while i <= len(deck) - 3:
            # Extract the current 3-character substring
            substring = ''.join(map(str, deck[i:i+3]))

            if substring == player1_sequence:
                # Player 1 wins this trick
                player1_trick_count += 1
                i += 3  # Jump ahead by 3 to avoid overlapping
            elif substring == player2_sequence:
                # Player 2 wins this trick
                player2_trick_count += 1
                i += 3  # Jump ahead by 3 to avoid overlapping
            else:
                # No match, move to the next card
                i += 1

        # Append trick counts for this deck to the results lists
        player1_tricks.append(player1_trick_count)
        player2_tricks.append(player2_trick_count)

    # Convert results to NumPy arrays and return them
    return np.array(player1_tricks), np.array(player2_tricks)



def all_combinations(decks: np.ndarray) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Tests every possible pair of distinct 3-bit sequences for two players using both game variations (cards and tricks).
    Aggregates outcomes across all the simulations provided.

    Parameters:
        decks (np.ndarray): An array of decks loaded from the `load_simulation` method.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: Two Pandas DataFrames containing aggregated results for the cards and tricks variations.
    """
    # Generate all possible 3-bit sequences
    three_bit_sequences = [''.join(seq) for seq in itertools.product('01', repeat=3)]
    
    # Prepare empty lists for results
    results_cards = []
    results_tricks = []

    # Get all distinct pairs of sequences
    sequence_pairs = [(p1, p2) for p1 in three_bit_sequences for p2 in three_bit_sequences if p1 != p2]

    # Process each pair for the cards game (variation1)
    for p1, p2 in tqdm(sequence_pairs, desc="Processing cards game"):
        p1_wins, p2_wins = 0, 0

        # Simulate for each deck
        player1_scores, player2_scores = cards(decks, p1, p2)
        for p1_score, p2_score in zip(player1_scores, player2_scores):
            if p1_score > p2_score:
                p1_wins += 1
            elif p2_score > p1_score:
                p2_wins += 1

        # Calculate win percentage for Player 1
        total_wins = p1_wins + p2_wins
        win_percentage = (p1_wins / total_wins * 100) if total_wins > 0 else 0

        # Append results
        results_cards.append({
            "Sequence 1": p1,
            "Sequence 2": p2,
            "Player 1 Wins": p1_wins,
            "Player 2 Wins": p2_wins,
            "Player 1 Win %": round(win_percentage, 2)
        })

    # Process each pair for the tricks game (variation2)
    for p1, p2 in tqdm(sequence_pairs, desc="Processing tricks game"):
        p1_wins, p2_wins = 0, 0

        # Simulate for each deck
        player1_tricks, player2_tricks = tricks(decks, p1, p2)
        for p1_trick, p2_trick in zip(player1_tricks, player2_tricks):
            if p1_trick > p2_trick:
                p1_wins += 1
            elif p2_trick > p1_trick:
                p2_wins += 1

        # Calculate win percentage for Player 1
        total_wins = p1_wins + p2_wins
        win_percentage = (p1_wins / total_wins * 100) if total_wins > 0 else 0

        # Append results
        results_tricks.append({
            "Sequence 1": p1,
            "Sequence 2": p2,
            "Player 1 Wins": p1_wins,
            "Player 2 Wins": p2_wins,
            "Player 1 Win %": round(win_percentage, 2)
        })

    # Convert results to Pandas DataFrames
    results_cards_df = pd.DataFrame(results_cards)
    results_tricks_df = pd.DataFrame(results_tricks)

    # Ensure "Sequence 1" and "Sequence 2" are stored as strings
    results_cards_df["Sequence 1"] = results_cards_df["Sequence 1"].astype(str)
    results_cards_df["Sequence 2"] = results_cards_df["Sequence 2"].astype(str)

    results_tricks_df["Sequence 1"] = results_tricks_df["Sequence 1"].astype(str)
    results_tricks_df["Sequence 2"] = results_tricks_df["Sequence 2"].astype(str)

    return results_cards_df, results_tricks_df
