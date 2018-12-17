import itertools
import json
import numpy as np

class Simulator():

	def __init__(self):
		# We use this to specify the number of chars in numpy arrays when storing the card history
		# Equal to the number of cards in the deck times 3 (one for suit, two for the card)
		self.max_str = 16 * 3

	def generate_layouts(self, position, hand1, dummy, all_cards, lead=set([])):
		taken = set().union(hand1, dummy, lead)
		remaining = set(all_cards) - taken

		comb = itertools.combinations(remaining, len(remaining) // 2)
		unseen_layouts = []
		for i in comb:
			unseen_layouts.append([set(i), remaining - set(i)])

		if position == 'NS':
			all_layouts = [{'N': dummy, 'S': hand1, 'W': i, 'E': j} for i, j in unseen_layouts]
			# all_layouts_simple = [[dummy, j, hand1, i] for i,j in unseen_layouts]
		elif position == 'E':
			all_layouts = [{'N': dummy, 'S': j, 'W': i, 'E': hand1} for i, j in unseen_layouts]
			# all_layouts_simple = [[dummy, hand1, j, i] for i,j in unseen_layouts]
		elif position == 'W':
			all_layouts = [{'N': dummy, 'S': i, 'W': hand1, 'E': j} for i, j in unseen_layouts]
			# all_layouts_simple = [[dummy, j, i, hand1] for i,j in unseen_layouts]

		return all_layouts

	def find_layouts(self, deal):
		""" 
		This currently only works for deals (after the lead). Not too much restructure
		needed to be compatible with finding layouts at any point
		"""
		# played = set(
		# 	[deal.card_history_str[i:i+3] for i in range(0, len(deal.card_history_str), 3)])

		lead = [deal.lead]

		dummy = deal.current_hands['N']

		south = deal.current_hands['S']
		all_layouts_NS = self.generate_layouts('NS', south, dummy, deal.all_cards, lead)

		east = deal.current_hands['E']
		all_layouts_E = self.generate_layouts('E', east, dummy, deal.all_cards, lead)

		west = deal.current_hands['W']
		all_layouts_W = self.generate_layouts('W', west, dummy, deal.all_cards, lead)

		return all_layouts_NS, all_layouts_E, all_layouts_W


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