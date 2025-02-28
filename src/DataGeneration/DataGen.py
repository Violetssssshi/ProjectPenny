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
    Instead of returning the actual decks, the function returns the file name (path)
    of the final .npy file that stores the deck data.

    Parameters:
      - n_decks: Number of new decks to generate.
      - seed: Seed value for random number generation.
      - half_deck_size: Number of cards in each half of the deck (default is 26).
      - append: Whether to append to existing seed data (defaults to False).

    Returns:
      - A string representing the path to the .npy file containing the deck data.
    """
    # Ensure that the data directory exists.
    os.makedirs("data", exist_ok=True)
    deck_file = f"data/decks_{seed}.npy"
    state_file = f"data/state_{seed}.json"
    
    # Calculate total deck cards.
    deck_length = half_deck_size * 2
    
    if append and os.path.exists(deck_file) and os.path.exists(state_file):
        # Load the existing decks and RNG state.
        existing_decks = np.load(deck_file)
        with open(state_file, "r") as f:
            saved_state = json.load(f)
        
        # Restore RNG state.
        rng = np.random.default_rng()
        rng.bit_generator.state = saved_state
        
        # Generate the new decks.
        new_decks = np.tile([0] * half_deck_size + [1] * half_deck_size, (n_decks, 1))
        rng.permuted(new_decks, axis=1, out=new_decks)
        
        # Combine the existing decks with the newly generated decks.
        combined_decks = np.concatenate((existing_decks, new_decks))
        np.save(deck_file, combined_decks)
        
        # Save the updated RNG state.
        with open(state_file, "w") as f:
            json.dump(rng.bit_generator.state, f)
    else:
        # Create a fresh RNG with the provided seed.
        rng = np.random.default_rng(seed)
        decks = np.tile([0] * half_deck_size + [1] * half_deck_size, (n_decks, 1))
        rng.permuted(decks, axis=1, out=decks)
        
        # Save the new deck and initial RNG state.
        np.save(deck_file, decks)
        with open(state_file, "w") as f:
            json.dump(rng.bit_generator.state, f)
    
    # Return the file name/path where the deck data is stored.
    print(f"Shuffled decks saved to {deck_file}")
    return deck_file
