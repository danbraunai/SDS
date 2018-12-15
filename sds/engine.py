import numpy as np
import copy
import sys
import time
import itertools
from sds.displayer import Displayer
from sds.deal import Deal
from sds.decisions import Decisions

class GameEngine:
	def __init__(self, deal, displayer, decisions):
		self.deal = deal
		self.displayer = displayer
		self.decisions = decisions

	def play_to_leaf(self):

		# print("Lead: ", self.deal.lead)
		# print(self.displayer.print_hands(self.deal.original_deal))

		# Play the lead automatically
		# self.deal.play_card('W', self.current_hands['W'][0])

		while self.deal.trick_no < 5:
			current_player = self.deal.play_order[self.deal.current_turn_index]
			current_hands = self.deal.current_hands
			current_trick = self.deal.current_trick
			current_card_no = self.deal.card_no
			last_decisions = self.deal.last_decisions

			decision, decision_point = (
				self.decisions.make_decision(
					current_player, current_hands[current_player].copy(), current_trick, 
					last_decisions))

			# if there were other potential cards to play, save the state of the game at this card.
			if decision_point:
				self.deal.save_position(
					[decision], last_decisions, current_player, current_hands, current_trick)

			# Once we've used the old decision to make a new decision, we don't need it anymore
			self.deal.last_decisions = None

			self.deal.play_card(current_player, decision)

			if len(self.deal.current_trick) == 4:
				self.deal.complete_trick()
			else:
				self.deal.next_player()

		self.deal.save_leaf_node()

	def play_to_all_leaves(self):
		# Play hand for the first time, reaching our first leaf node and noting down all other
		# decision nodes in self.decision_points 
		self.play_to_leaf()
		# While there are still unexplored areas of game tree, go back to most recent decision
		# and make another one
		# for decision in self.deal.decision_points:
		# 	print(decision)
		# print('\n')

		while self.deal.decision_points:
			# for decision in self.deal.decision_points:
			# 	print(decision)
			# print('\n')
			last_decision_position = self.deal.decision_points[-1]

			# print(last_decisions)
			# print("Decisions left = ", len(self.deal.decision_points), '\n')
			# print(self.deal.decision_points)
			# sys.exit(1)
			self.deal.restore_position(last_decision_position)
			# print(last_decisions_position)
			# Play the hand again from a specific position, noting down the card number and card
			# of the last decision made
			self.play_to_leaf()

			# print(self.deal.completed_tricks)
			# print(self.deal.full_history)
			# sys.exit(1)
		# print(self.deal.leaf_nodes)
		# print(self.deal.completed_tricks)
		# print(len(self.deal.full_history))

	def generate_layouts(self, position, hand1, dummy, played=set([])):
		taken = set().union(hand1, dummy, played)
		remaining = set(self.deal.all_cards) - taken

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

	def start(self):
		played = [self.deal.lead]
		dummy = self.deal.current_hands['N']

		south = self.deal.current_hands['S']
		all_layouts_NS = self.generate_layouts('NS', south, dummy, played)

		east = self.deal.current_hands['E']
		all_layouts_E = self.generate_layouts('E', east, dummy, played)

		west = self.deal.current_hands['W']
		all_layouts_W = self.generate_layouts('W', west, dummy, played)

		# print(all_layouts_NS[0])
		for deal in all_layouts_NS:
			self.deal = Deal(deal=deal, lead=played[0])
			# print(self.deal.original_deal)
			# print(self.deal.lead)
			# sys.exit(1)
			self.play_to_all_leaves()
			print("Found leaf: ", self.deal.leaf_nodes)
		sys.exit(1)

		for i in [all_layouts_NS, all_layouts_W, all_layouts_E]:
			print(len(i))

		# This is kind of silly, only one layout where they are all the same (the true layout)
		# unique_layouts = all_layouts_NS.copy()
		# unique_layouts += [i for i in all_layouts_E if i not in unique_layouts]
		# unique_layouts += [i for i in all_layouts_W if i not in unique_layouts]
		# print(len(unique_layouts))
		# sys.exit(1)


if __name__ == '__main__':

	displayer = Displayer()
	decisions = Decisions()
	start_time = time.time()

	seed = 0
	deal = Deal(seed=seed)
	game = GameEngine(deal, displayer, decisions)
	game.start()
	# game.play_to_leaf()
	# game.play_to_all_leaves()

	# start_time = time.time()
	# for seed in np.arange(100000):
	# 	deal = Deal(seed)
	# 	game = GameEngine(deal, displayer)
	# 	game.play_hand()
	# print("Time Taken: ", time.time() - start_time)
