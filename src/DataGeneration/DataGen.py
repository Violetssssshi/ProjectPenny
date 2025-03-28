import numpy as np
import os
import json
from src.DEBUGGER.HELPERS import debugger_factory




@debugger_factory()
def get_decks(n_decks: int,
              seed: int,
              half_deck_size: int,
              append: bool = False) -> str:
    """
    Generates shuffled card decks with the ability to append to existing decks.
    Instead of returning the actual decks, the function returns the file directory
    of the final .npy files that store the deck data. Each file containing maximum 50,000 decks.

    Parameters:
      - n_decks: Number of new decks to generate.
      - seed: Seed value for random number generation.
      - half_deck_size: Number of cards in each half of the deck (default is 26).
      - append: Whether to append to existing seed data (defaults to False).

    Returns:
      - A string representing the path to the file directory containing the deck data.
    """
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)  # Create data directory if it doesn't exist
    state_file = f"{data_dir}/state_{seed}.json"  # File to store RNG state
    decks_per_file = 50000  # Maximum number of decks per file

    if append and os.path.exists(state_file):
        # If appending and state file exists, load previous state
        with open(state_file, "r") as f:
            saved_state = json.load(f)
        rng = np.random.default_rng()
        rng.bit_generator.state = saved_state  # Restore RNG state
        
        # Find existing deck files and determine the last file number
        existing_files = sorted([f for f in os.listdir(data_dir) if f.startswith(f"decks_{seed}_") and f.endswith(".npy")],key=lambda x: int(x.split("_")[-1].split(".")[0]))
        last_file_num = int(existing_files[-1].split("_")[-1].split(".")[0]) if existing_files else 0
        last_file_path = os.path.join(data_dir, existing_files[-1]) if existing_files else None
        
        if last_file_path:
            # Calculate remaining space in the last file
            last_file_decks = np.load(last_file_path)
            remaining_space = decks_per_file - len(last_file_decks)
        else:
            remaining_space = 0
    else:
        # If not appending or no state file, start fresh
        rng = np.random.default_rng(seed)
        last_file_num = 0
        remaining_space = 0

    decks_generated = 0
    while decks_generated < n_decks:
        if remaining_space > 0:
            # Fill remaining space in the last file
            batch_size = min(remaining_space, n_decks - decks_generated)
            new_decks = np.tile([0] * half_deck_size + [1] * half_deck_size, (batch_size, 1))
            rng.permuted(new_decks, axis=1, out=new_decks)  # Shuffle the decks
            
            # Combine with existing decks and save
            file_path = os.path.join(data_dir, f"decks_{seed}_{last_file_num:04d}.npy")
            existing_decks = np.load(file_path) if os.path.exists(file_path) else np.empty((0, half_deck_size * 2))
            combined_decks = np.concatenate((existing_decks, new_decks))
            np.save(file_path, combined_decks)
            
            decks_generated += batch_size
            remaining_space -= batch_size
        else:
            # Create a new file
            last_file_num += 1
            batch_size = min(decks_per_file, n_decks - decks_generated)
            new_decks = np.tile([0] * half_deck_size + [1] * half_deck_size, (batch_size, 1))
            rng.permuted(new_decks, axis=1, out=new_decks)  # Shuffle the decks
            
            # Save new decks to a new file
            file_path = os.path.join(data_dir, f"decks_{seed}_{last_file_num:04d}.npy")
            np.save(file_path, new_decks)
            
            decks_generated += batch_size
            remaining_space = decks_per_file - batch_size

    # Save the final RNG state
    with open(state_file, "w") as f:
        json.dump(rng.bit_generator.state, f)

    print(f"Shuffled decks saved to {data_dir}/")
    return data_dir