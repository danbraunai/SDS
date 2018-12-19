import numpy as np

# Set whether you want python to utilize all available cores on your machine.
# Note, this usually only gives a speed increase for deals with 5 or more cards each
multiprocessing = False

# If you want to use a random position, set a 'seed' and 'cards_each'. 
# seed = np.random.randint(1000)
seed = 5
cards_each = 4

# If you want to seea particular position solved. 
# hands = {'N': ['C14', 'C13', 'C12', 'C11'], 'E': ['S14', 'S13', 'H12', 'H13'], 
#     'S': ['D14', 'D11', 'H14', 'H11'], 'W': ['D12', 'D13', 'S12', 'S11']}

# **Must have either 'seed' and 'cards_each' or 'hands' set**

# Select the trump suit. use None for notrumps, otherwise 'S', 'D', 'H', 'C'. 
trumps = 'S'

# Which player plays the next card.
first_turn = 'S'

# This indicates whether the player can see the dummy or not. (Dummy always set as north)
# on_lead = False

# Set the current cards that have been played in a trick before this decision (in order)
# Make sure these cards are not included in the 'hands' dictionary, and that each player
# has the right amount of cards given a trick is incomplete. See example2.py
# current_trick = [('N', 'H12'), ('E', 'H14')]
