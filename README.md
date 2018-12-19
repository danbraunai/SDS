# SDS
Simplified game of bridge created for AI analysis

This repository currently houses a single-dummy bridge solver created using a minimax algorithm. 
It is a complete solver, in that it searches the full game tree for every possible layout. 

The general process it uses is:
- Given a position, generate all possible distributions of the opponents cards
- For each distribution, run a double-dummy solver (DDS) and get the number of tricks for that card
- Aggregate the results to get the expected utility of playing each card. (Currently, utility = mean number of tricks.)

It is capable of solving NoTrumps and Suit contracts, and from any position in the hand (doesn't have to be trick 1).
Much optimization can be done to help solve games with more cards. It can solve most 5 cards positions in a few seconds on 
my machine using 6 cores. However, the main objective of this project is to create a base for experimentation with ILP/PILP techniques,
along with other methods which will be used to create the ultimate bridge AI.

To run the SDS:
Clone the repository.
Modfiy (or create new) files in sds/Examples to setup the position you want to solve.
Run the engine.py file with your example as a cmd line argument (e.g. python engine.py example1)
The output of the SDS will be saved to sds/Examples/example1_output.txt
Alternatively, tinker with the engine.py file and run whatever you like

The article 'Inferences from a SDS.ipynb' inside sds/ shows some fun I had with this, and illustrates something to think about for future work

The main code sits in sds:
displayer.py - Just used to print a hand to terminal or text file
deal.py - Creates a bridge deal, and maintains the state of a deal throughout the solver
simulator.py - Generates possible layouts given a player's cards (and the dummy, unless we want to run SDS on the lead)
dds.py - Contains the minimax algorithm
engine.py - A module used to play around with the solver

The 'deprecated' folder contains some code that is deprecated or not currently tweaked well enough to add to the main source files.
