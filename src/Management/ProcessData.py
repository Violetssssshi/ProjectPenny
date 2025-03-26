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
    # Convert decks to strings upfront for faster processing
    deck_strings = [''.join(deck.astype(str)) for deck in decks]
    seq_len = len(player1_sequence)
    
    # Preallocate score arrays
    player1_scores = np.zeros(len(decks), dtype=int)
    player2_scores = np.zeros(len(decks), dtype=int)
    
    for deck_idx, deck_str in enumerate(deck_strings):
        i = 0
        pile = 0
        p1_score = 0
        p2_score = 0
        n = len(deck_str)
        
        # Replicate original logic exactly
        while i <= n - seq_len:
            current_segment = deck_str[i:i+seq_len]
            pile += 1  # Original behavior: increment pile for every triplet checked
            
            if current_segment == player1_sequence:
                p1_score += pile + 2
                pile = 0
                i += seq_len  # Jump ahead after match
            elif current_segment == player2_sequence:
                p2_score += pile + 2
                pile = 0
                i += seq_len  # Jump ahead after match
            else:
                i += 1  # Move to next position
        
        player1_scores[deck_idx] = p1_score
        player2_scores[deck_idx] = p2_score
    
    return player1_scores, player2_scores



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
    # Convert all decks to strings upfront
    deck_strings = [''.join(deck.astype(str)) for deck in decks]
    
    # Initialize arrays for results
    player1_tricks = np.zeros(len(decks), dtype=int)
    player2_tricks = np.zeros(len(decks), dtype=int)
    
    # Get sequence length (should be 3)
    seq_len = len(player1_sequence)
    
    for deck_idx, deck_str in enumerate(deck_strings):
        pos = 0
        p1_count = 0
        p2_count = 0
        len_deck = len(deck_str)
        
        # Replicate original logic with string optimization
        while pos <= len_deck - seq_len:
            # Direct string slice comparison
            current_segment = deck_str[pos:pos+seq_len]
            
            if current_segment == player1_sequence:
                p1_count += 1
                pos += seq_len  # Jump ahead after match
            elif current_segment == player2_sequence:
                p2_count += 1
                pos += seq_len  # Jump ahead after match
            else:
                pos += 1  # Move to next position
        
        # Store results in preallocated arrays
        player1_tricks[deck_idx] = p1_count
        player2_tricks[deck_idx] = p2_count
    
    return player1_tricks, player2_tricks

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
        p1_wins, p2_wins, draws = 0, 0, 0

        # Simulate for each deck
        player1_scores, player2_scores = cards(decks, p1, p2)
        for p1_score, p2_score in zip(player1_scores, player2_scores):
            if p1_score > p2_score:
                p1_wins += 1
            elif p2_score > p1_score:
                p2_wins += 1
            else:
                draws += 1

        # Calculate percentages
        total_games = p1_wins + p2_wins + draws
        win_percentage = (p1_wins / total_games * 100) if total_games > 0 else 0
        tie_percentage = (draws / total_games * 100) if total_games > 0 else 0

        # Append results with percentages
        results_cards.append({
            "Sequence 1": p1,
            "Sequence 2": p2,
            "Player 1 Wins": p1_wins,
            "Player 2 Wins": p2_wins,
            "Draws": draws,
            "Player 1 Win %": round(win_percentage, 2),
            "Tie %": round(tie_percentage, 2)  # New tie probability
        })

    # Process each pair for the tricks game (variation2)
    for p1, p2 in tqdm(sequence_pairs, desc="Processing tricks game"):
        p1_wins, p2_wins, draws = 0, 0, 0

        # Simulate for each deck
        player1_tricks, player2_tricks = tricks(decks, p1, p2)
        for p1_trick, p2_trick in zip(player1_tricks, player2_tricks):
            if p1_trick > p2_trick:
                p1_wins += 1
            elif p2_trick > p1_trick:
                p2_wins += 1
            else:
                draws += 1

        # Calculate percentages
        total_games = p1_wins + p2_wins + draws
        win_percentage = (p1_wins / total_games * 100) if total_games > 0 else 0
        tie_percentage = (draws / total_games * 100) if total_games > 0 else 0

        # Append results with percentages
        results_tricks.append({
            "Sequence 1": p1,
            "Sequence 2": p2,
            "Player 1 Wins": p1_wins,
            "Player 2 Wins": p2_wins,
            "Draws": draws,
            "Player 1 Win %": round(win_percentage, 2),
            "Tie %": round(tie_percentage, 2)  # New tie probability
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