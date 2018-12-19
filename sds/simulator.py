import itertools
import json
import numpy as np
import sys



def generate_layouts(position, hand, dummy, all_cards, played):
	cards_taken = played + hand + dummy
	remaining = [i for i in all_cards if i not in cards_taken]
	# Distribute the remaining cards evenly among two hands. This handles an odd number of cards
	comb = itertools.combinations(remaining, len(remaining) // 2)
	unseen_layouts = []
	for hand_set in comb:
		# Sort by biggest card first
		sorted_hand_set = sorted(hand_set, key=lambda x: int(x[1:]), reverse=True)
		unsorted_compliment = [i for i in remaining if i not in sorted_hand_set]
		compliment = sorted(unsorted_compliment, key=lambda x: int(x[1:]), reverse=True)
		unseen_layouts.append([sorted_hand_set, compliment])

	# North's dummy is always exposed here
	if position == 'NS':
		all_layouts = [{'N': dummy, 'S': hand, 'W': i, 'E': j} for i, j in unseen_layouts]
	elif position == 'E':
		all_layouts = [{'N': dummy, 'S': j, 'W': i, 'E': hand} for i, j in unseen_layouts]
	elif position == 'W':
		all_layouts = [{'N': dummy, 'S': i, 'W': hand, 'E': j} for i, j in unseen_layouts]

	return all_layouts

def generate_layouts_lead(hand, all_cards):
	"""
	Generates all possible layouts given only one hand (the leaders hand). Here we need to do
	a double loop of itertools.combinations. The first gives us every combination for one player,
	the next gives us the combinations for the other two players.

	Note, the number of layouts for a n card game is (n-n/4)C(n/4) * (n-2n/4)C(n/4).
	For 16 card game - layouts = 12C4 * 8C4 = 34,650.
	For 20 card game - layouts = 15C5 * 10C5 = 756,756.
	For 24 card game - layouts = 18C6 * 12C6 = 17,153,136.
	For 52 card game - layouts = 39C13 * 26C13 = 8e9 * 1e7 = 8.4e16
	"""
	cards_remaining = [i for i in all_cards if i not in hand]

	unseen_layouts = []

	comb = itertools.combinations(cards_remaining, int(len(cards_remaining) / 3))
	for i in comb:
		current_remaining = [j for j in cards_remaining if j not in i]
		comb_remaining = itertools.combinations(
			current_remaining, int(len(current_remaining) / 2))

		for j in comb_remaining:
			final_remaining = [k for k in cards_remaining if k not in i + j]
			layout = [list(i), list(j), final_remaining]
			unseen_layouts.append(layout)

	all_layouts = [{'N': i, 'S': j, 'W': hand, 'E': k} for i, j, k in unseen_layouts]

	return all_layouts

def find_layouts(deal, player, on_lead=False):
	# Capable of find layouts at any point in hand, including the lead (when lead=True)

	if on_lead:
		all_layouts = generate_layouts_lead(deal.current_hands['W'], deal.all_cards)
		return all_layouts

	dummy = deal.current_hands['N']
	south = deal.current_hands['S']
	east = deal.current_hands['E']
	west = deal.current_hands['W']

	played = [i for i in deal.all_cards if i not in dummy + south + east + west]

	if player in ['N', 'S']:
		all_layouts = generate_layouts('NS', south, dummy, deal.all_cards, played)

	elif player == 'E':
		all_layouts = generate_layouts('E', east, dummy, deal.all_cards, played)

	elif player == 'W':
		all_layouts = generate_layouts('W', west, dummy, deal.all_cards, played)

	return all_layouts
