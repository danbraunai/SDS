import numpy as np
import sys
from operator import itemgetter
import copy

class Deal:

	all_cards = [
		'C14', 'C13', 'C12', 'C11', 'D14', 'D13', 'D12', 'D11',
		'H14', 'H13', 'H12', 'H11', 'S14', 'S13', 'S12', 'S11',
		]
	play_order = ['W', 'N', 'E', 'S']


	def __init__(
			self, seed=None, deal=None, lead=None, current_turn_index=0, current_trick=[], 
			trick_tally=0, trick_no=1, card_no=1, decision_points=[], last_decisions=[],
			leaf_nodes=0, full_history=[], card_history_str=''):
		# Need either deal or seed
		if deal:
			self.original_hands = deal
		else:
			self.seed = seed
			np.random.seed(seed)
			self.original_hands = self.create_deal()

		self.current_hands = copy.deepcopy(self.original_hands)
		self.lead = lead
		# self.contract = np.random.randint(0, 5)
		self.trick_tally = trick_tally
		self.trick_no = trick_no
		self.current_trick = current_trick
		self.current_turn_index = current_turn_index
		self.card_no = card_no
		self.decision_points = decision_points
		self.last_decisions = last_decisions
		self.completed_tricks = last_decisions
		self.leaf_nodes = leaf_nodes
		self.full_history = full_history
		self.card_history_str = card_history_str


	def create_deal(self):
		full_deal = np.random.choice(self.all_cards, len(self.all_cards), replace=False)
		north, east, south, west = np.split(full_deal, 4)
		deal_dict = {'N': set(north), 'E': set(east), 'S': set(south), 'W': set(west)}
		return deal_dict

	def make_lead(self, card=None):
		if not card:
			# Choose the max so that we always get the same lead when running experiments
			card = max(self.current_hands['W'])
		self.play_card('W', card)
		self.lead = card

	def play_card(self, player, card):
		self.current_trick.append((player, card))
		self.current_hands[player].discard(card)
		self.card_no += 1
		self.card_history_str += card
		# Next player's turn (unless it's the end of the trick which we deal with in play_to_lead)
		self.current_turn_index = (self.current_turn_index + 1) % 4
	# @profile
	def play_card_dds(self, player, card):
		self.current_trick.append((player, card))
		self.current_hands[player].discard(card)
		# Next player's turn (unless it's the end of the trick which we deal with in play_to_lead)
		self.current_turn_index = (self.current_turn_index + 1) % 4		

	def complete_trick(self):
		valid_cards = [i for i in self.current_trick if i[1][0] == self.current_trick[0][1][0]]
		# Get the position of the winner of the trick (N, S, E, W)
		winner = max(valid_cards, key=itemgetter(1))[0]
		self.current_turn_index = self.play_order.index(winner)
		if winner in ['N', 'S']:
			self.trick_tally += 1
		self.completed_tricks.append(self.current_trick.copy())
		self.trick_no += 1
		self.current_trick = []

	def save_position(self, decision, old_decision, player, hands, trick):
		if old_decision:
			# merge the two lists together to get a set of old decisions made at same point
			decision = decision + old_decision

		self.decision_points.append((
			self.card_no, decision, player, copy.deepcopy(hands), copy.deepcopy(trick), 
			self.trick_tally, self.trick_no, self.completed_tricks.copy(), self.card_history_str))
	# @profile
	def save_position_dds(self):
		# hand_copy = copy.deepcopy(self.current_hands)
		hand_copy = None
		trick_copy = self.current_trick.copy()
		idx = self.current_turn_index
		tally = self.trick_tally

		# position = (
		# 	self.current_turn_index, copy.deepcopy(self.current_hands), 
		# 	self.current_trick.copy(), self.trick_tally,
		# 	)
		position = (idx, hand_copy, trick_copy, tally)

		# print("Current state at save point: ", position)
		return position
	def restore_position(self, position):
		# Restore the deal back to a specific position
		self.card_no = position[0]
		self.last_decisions = position[1]
		self.current_turn_index = self.play_order.index(position[2])
		self.current_hands = position[3]
		self.current_trick = position[4]
		self.trick_tally = position[5]
		self.trick_no = position[6]
		self.completed_tricks = position[7]
		self.card_history_str = position[8]
		# Finally, delete the decision point so we don't reach it again (unless 
		# Decisions.make_decision indicates that we need to)
		del self.decision_points[-1]

	def restore_position_dds(self, position):
		self.current_turn_index, self.current_hands, self.current_trick, self.trick_tally = (
			position)
	# @profile
	def play_last_trick(self):
		"""
		This is just a speedup in our dds algorithm
		"""
		for i in range(4):
			player = self.play_order[self.current_turn_index]
			card = self.current_hands[player].pop()

			self.current_trick.append((player, card))
			self.current_turn_index = (self.current_turn_index + 1) % 4

		valid_cards = [i for i in self.current_trick if i[1][0] == self.current_trick[0][1][0]]
		# Get the position of the winner of the trick (N, S, E, W)
		winner = max(valid_cards, key=itemgetter(1))[0]
		if winner in ['N', 'S']:
			self.trick_tally += 1
		# self.completed_tricks.append(self.current_trick.copy())

	def save_leaf_node(self):
		# Save information about the gameplay leading to this leaf node
		self.leaf_nodes += 1
		self.full_history.append((self.card_history_str, self.trick_tally))
		self.completed_tricks = []
		self.card_history_str = ''

if __name__ == '__main__':
	np.random.seed(0)
	d = Deal(2)
	# printer.print_current(d.current_hands)
	# d.play_card('N', 'S14')
	# print(d.current_hands)


