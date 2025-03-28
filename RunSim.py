from src.PenneyGame.Penney import display_processed_decks,get_user_input,run_sim
import os

def main():
    print("Welcome to the Penney Game Simulation!")
    
    # Show previously processed deck counts
    display_processed_decks()
    
    n_decks, seed = get_user_input()

    # Initialize append flag
    append = False

    # Check if data for the given seed already exists
    if os.path.exists(f"data/processed_decks_count_{seed}.txt"):
        append = True
        print(f"Seed {seed} already exists. Appending new decks to existing data.")
    
    run_sim(n_decks, seed, append=append)

if __name__ == "__main__":
    main()