import itertools
import json
import numpy as np
import sys


class Simulator():

	def __init__(self):
		# We use this to specify the number of chars in numpy arrays when storing the card history
		# Equal to the number of cards in the deck times 3 (one for suit, two for the card)
		self.max_str = 16 * 3


	def save_sims(self, all_sims, seed):
		for position, sim in zip(['NS', 'E', 'W'], all_sims):
			with open(f'sims/{seed}{position}.json', 'w') as f:
				json.dump(sim, f, indent=4)

	def load_sims(self, seed):
		names = ['history', 'tricks']
		# max 48 char string for history, and unsigned (positive) on digit int for tricks
		formats = [f'U{self.max_str}', 'u2']
		dtype = dict(names = names, formats=formats)
		all_sims = []
		for position in ['NS', 'E', 'W']:
			with open(f'sims/{seed}{position}.json', 'r') as f:
				sim_dict = json.load(f)
				# Convert to numpy structured array
				# sim_arr = np.array(list(sim_dict.items()), dtype=dtype)
				# Convert to regular numpy array
				sim_arr = np.array(list(sim_dict.items()))
				all_sims.append(sim_arr)
		return all_sims