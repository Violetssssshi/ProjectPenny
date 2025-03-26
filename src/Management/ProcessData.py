import os
import numpy as np
import itertools
import pandas as pd
import glob
from tqdm import tqdm

def load_simulation(data_dir: str, seed: int) -> np.ndarray:
    """
    Loads simulation data from multiple NumPy (.npy) files containing the decks.

    Parameters:
        data_dir (str): The directory containing the .npy files.
        seed (int): The seed used for the simulation.

    Returns:
        np.ndarray: An array with all decks stored in the files.
    """
    file_pattern = f"{data_dir}/decks_{seed}_*.npy"
    deck_files = sorted(glob.glob(file_pattern))
    
    if not deck_files:
        raise FileNotFoundError(f"No deck files found for seed {seed} in directory '{data_dir}'.")
    
    decks = []
    for file in deck_files:
        decks.append(np.load(file))
    
    return np.concatenate(decks)


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

def all_combinations(data_dir: str, seed: int, append: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Tests every possible pair of distinct 3-bit sequences for two players using both game variations (cards and tricks).
    Aggregates outcomes across all the simulations provided.

    Parameters:
        data_dir (str): The directory containing the deck files.
        seed (int): The seed used for the simulation.
        append (bool): Whether to append to existing data or start fresh.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: Two Pandas DataFrames containing aggregated results for the cards and tricks variations.
    """
    if append:
        existing_cards, existing_tricks = load_scoring_data(seed)
        processed_decks = load_processed_decks_count(seed)
    else:
        existing_cards = pd.DataFrame(columns=['Sequence 1', 'Sequence 2', 'Player 1 Wins', 'Player 2 Wins', 'Draws', 'Player 1 Win %', 'Tie %'])
        existing_tricks = pd.DataFrame(columns=['Sequence 1', 'Sequence 2', 'Player 1 Wins', 'Player 2 Wins', 'Draws', 'Player 1 Win %', 'Tie %'])
        processed_decks = 0

    decks = load_simulation(data_dir, seed)
    new_decks = decks[processed_decks:]

    all_sequences = ['{:03b}'.format(i) for i in range(8)]
    new_cards_results = []
    new_tricks_results = []

    total_iterations = len(all_sequences) * (len(all_sequences) - 1)

    with tqdm(total=total_iterations, desc="Processing Pairs") as pbar:
        for p1 in all_sequences:
            for p2 in all_sequences:
                if p1 != p2:
                    p1_wins_cards, p2_wins_cards, draws_cards = 0, 0, 0
                    p1_wins_tricks, p2_wins_tricks, draws_tricks = 0, 0, 0

                    p1_scores_cards, p2_scores_cards = cards(new_decks, p1, p2)
                    p1_scores_tricks, p2_scores_tricks = tricks(new_decks, p1, p2)

                    for s1, s2 in zip(p1_scores_cards, p2_scores_cards):
                        if s1 > s2:
                            p1_wins_cards += 1
                        elif s2 > s1:
                            p2_wins_cards += 1
                        else:
                            draws_cards += 1

                    for s1, s2 in zip(p1_scores_tricks, p2_scores_tricks):
                        if s1 > s2:
                            p1_wins_tricks += 1
                        elif s2 > s1:
                            p2_wins_tricks += 1
                        else:
                            draws_tricks += 1

                    total_games_cards = p1_wins_cards + p2_wins_cards + draws_cards
                    total_games_tricks = p1_wins_tricks + p2_wins_tricks + draws_tricks

                    new_cards_results.append({
                        'Sequence 1': p1,
                        'Sequence 2': p2,
                        'Player 1 Wins': p1_wins_cards,
                        'Player 2 Wins': p2_wins_cards,
                        'Draws': draws_cards,
                        'Player 1 Win %': round((p1_wins_cards / total_games_cards) * 100, 2) if total_games_cards > 0 else 0,
                        'Tie %': round((draws_cards / total_games_cards) * 100, 2) if total_games_cards > 0 else 0
                    })

                    new_tricks_results.append({
                        'Sequence 1': p1,
                        'Sequence 2': p2,
                        'Player 1 Wins': p1_wins_tricks,
                        'Player 2 Wins': p2_wins_tricks,
                        'Draws': draws_tricks,
                        'Player 1 Win %': round((p1_wins_tricks / total_games_tricks) * 100, 2) if total_games_tricks > 0 else 0,
                        'Tie %': round((draws_tricks / total_games_tricks) * 100, 2) if total_games_tricks > 0 else 0
                    })

                    pbar.update(1)

    new_cards_df = pd.DataFrame(new_cards_results)
    new_tricks_df = pd.DataFrame(new_tricks_results)

    final_cards = update_dataframe(existing_cards, new_cards_df)
    final_tricks = update_dataframe(existing_tricks, new_tricks_df)

    total_decks = processed_decks + len(new_decks)
    save_processed_decks_count(seed, total_decks)
    save_scoring_data(seed, final_cards, final_tricks)

    return final_cards, final_tricks


def load_processed_decks_count(seed: int) -> int:
    count_file = f"data/processed_decks_count_{seed}.txt"
    if os.path.exists(count_file):
        with open(count_file, 'r') as f:
            return int(f.read())
    return 0

def save_processed_decks_count(seed: int, count: int):
    count_file = f"data/processed_decks_count_{seed}.txt"
    with open(count_file, 'w') as f:
        f.write(str(count))


def update_dataframe(existing_df: pd.DataFrame, new_df: pd.DataFrame) -> pd.DataFrame:
    if existing_df.empty:
        return new_df

    existing_df['Sequence 1'] = existing_df['Sequence 1'].apply(lambda x: x.zfill(3))
    existing_df['Sequence 2'] = existing_df['Sequence 2'].apply(lambda x: x.zfill(3))

    existing_df['Player 1 Wins'] += new_df['Player 1 Wins']
    existing_df['Player 2 Wins'] += new_df['Player 2 Wins']
    existing_df['Draws'] += new_df['Draws']

    total_games = existing_df['Player 1 Wins'] + existing_df['Player 2 Wins'] + existing_df['Draws']
    existing_df['Player 1 Win %'] = (existing_df['Player 1 Wins'] / total_games * 100).fillna(0).round(2)
    existing_df['Tie %'] = (existing_df['Draws'] / total_games * 100).fillna(0).round(2)

    return existing_df

def save_scoring_data(seed: int, cards_data: pd.DataFrame, tricks_data: pd.DataFrame):
    os.makedirs("data", exist_ok=True)
    cards_data.to_csv(f"data/scoring_cards_{seed}.csv", index=False)
    tricks_data.to_csv(f"data/scoring_tricks_{seed}.csv", index=False)

def load_scoring_data(seed: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    cards_file = f"data/scoring_cards_{seed}.csv"
    tricks_file = f"data/scoring_tricks_{seed}.csv"
    
    if os.path.exists(cards_file) and os.path.exists(tricks_file):
        cards_data = pd.read_csv(cards_file, dtype={'Sequence 1': str, 'Sequence 2': str})
        tricks_data = pd.read_csv(tricks_file, dtype={'Sequence 1': str, 'Sequence 2': str})
        return cards_data, tricks_data
    else:
        return pd.DataFrame(), pd.DataFrame()