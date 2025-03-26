import src.PenneyGame.Penney as Penney
import importlib
importlib.reload(Penney)

Penney.run_sim(
    n_decks=100000,
    seed=42,
    half_deck_size=26,
    append=True,
    filename="simulation_results",
    vmin=0,
    vmax=100
)