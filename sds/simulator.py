import itertools
import json
import numpy as np
import sys


class Simulator():

	def __init__(self):
		# We use this to specify the number of chars in numpy arrays when storing the card history
		# Equal to the number of cards in the deck times 3 (one for suit, two for the card)
		self.max_str = 16 * 3

	# def sort_hand(self, hand):
		
	def generate_layouts(self, position, hand, dummy, all_cards, played):
		taken = set().union(hand, dummy, played)
		remaining = set(all_cards) - taken

		comb = itertools.combinations(remaining, len(remaining) // 2)
		unseen_layouts = []
		for i in comb:
			unseen_layouts.append([set(i), remaining - set(i)])

		if position == 'NS':
			all_layouts = [{'N': dummy, 'S': hand, 'W': i, 'E': j} for i, j in unseen_layouts]
			# all_layouts_simple = [[dummy, j, hand, i] for i,j in unseen_layouts]
		elif position == 'E':
			all_layouts = [{'N': dummy, 'S': j, 'W': i, 'E': hand} for i, j in unseen_layouts]
			# all_layouts_simple = [[dummy, hand, j, i] for i,j in unseen_layouts]
		elif position == 'W':
			all_layouts = [{'N': dummy, 'S': i, 'W': hand, 'E': j} for i, j in unseen_layouts]
			# all_layouts_simple = [[dummy, j, i, hand] for i,j in unseen_layouts]

		return all_layouts

	def generate_layouts_lead(self, hand, all_cards):
		"""
		Generates all possible layouts given only one hand (the leaders hand). Note, the number
		of layouts for a n card game is (n-n/4)C(n/4) * (n-2n/4)C(n/4).
		For 16 card game - layouts = 12C4 * 8C4 = 34,650.
		For 20 card game - layouts = 15C5 * 10C5 = 756,756.
		For 24 card game - layouts = 18C6 * 12C6 = 17,153,136.
		For 52 card game - layouts = 39C13 * 26C13 = 8e9 * 1e7 = 8.4e16
		"""
		cards_remaining = set(all_cards) - hand

		# print("My hand: ", hand)
		# print("remaining cards:", cards_remaining)
		unseen_layouts = []
		comb = itertools.combinations(cards_remaining, int(len(cards_remaining) / 3))
		for i in comb:
			current_remaining = set(cards_remaining) - set(i)
			comb_remaining = itertools.combinations(
				current_remaining, int(len(current_remaining) / 2))

			for j in comb_remaining:
				layout = [set(i), set(j), set(cards_remaining) - set(i).union(set(j))]
				# layout = [list(i), list(j), [k for k in cards_remaining if k not in i + j]]
				# print(layout)
				# sys.exit(1)
				unseen_layouts.append(layout)

		all_layouts = [{'N': i, 'S': j, 'W': hand, 'E': k} for i, j, k in unseen_layouts]

		return all_layouts

	def find_layouts(self, deal, player, lead=False):
		""" 
		Capable of find layouts at any point in hand, including the lead (when lead=True)
		"""


		if lead:
			all_layouts = self.generate_layouts_lead(deal.current_hands['W'], deal.all_cards)
			return all_layouts

		played = set(deal.all_cards) - set().union(*deal.current_hands.values())

		dummy = deal.current_hands['N']

		if player in ['N', 'S']:
			south = deal.current_hands['S']
			all_layouts = self.generate_layouts('NS', south, dummy, deal.all_cards, played)

		elif player == 'E':
			east = deal.current_hands['E']
			all_layouts = self.generate_layouts('E', east, dummy, deal.all_cards, played)

		elif player == 'W':
			west = deal.current_hands['W']
			all_layouts = self.generate_layouts('W', west, dummy, deal.all_cards, played)

		return all_layouts


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