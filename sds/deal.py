import numpy as np
import sys
from operator import itemgetter
import copy

class Deal:

	all_cards = [
		'C14', 'C13', 'C12', 'C11', 'D14', 'D13', 'D12', 'D11',
		'H14', 'H13', 'H12', 'H11', 'S14', 'S13', 'S12', 'S11',
		]
	play_order = ['N', 'E', 'S', 'W']


	def __init__(self, seed=None, deal=None, lead=None):
		if seed is not None:
			np.random.seed(seed)
			self.original_deal = self.create_deal()
			self.lead = self.original_deal['W'][0]
			self.current_hands = copy.deepcopy(self.original_deal)
			self.current_hands['W'].remove(self.lead)
		else:
			self.original_deal = deal
			self.lead = lead
			self.current_hands = copy.deepcopy(self.original_deal)

		self.contract = np.random.randint(0, 5)
		# self.lead = np.random.choice(self.original_deal['W'])
		self.trick_tally = 0
		self.trick_no = 1
		self.current_trick = [('W', self.lead)]
		self.current_turn_index = 0
		self.card_no = 2
		self.decision_points = []
		self.last_decisions = None
		self.completed_tricks = []
		self.leaf_nodes = 0
		self.full_history = []

	def create_deal(self):
		full_deal = np.random.choice(self.all_cards, len(self.all_cards), replace=False)
		north, east, south, west = np.split(full_deal, 4)
		deal_dict = {'N': list(north), 'E': list(east), 'S': list(south), 'W': list(west)}
		return deal_dict

	def play_card(self, player, card):
		self.current_trick.append((player, card))
		self.current_hands[player].remove(card)
		self.card_no += 1

	def complete_trick(self):
		valid_hands = [i for i in self.current_trick if i[1][0] == self.current_trick[0][1][0]]
		# Get the position of the winner of the trick (N, S, E, W)
		winner = max(valid_hands, key=itemgetter(1))[0]
		self.current_turn_index = self.play_order.index(winner)
		if winner in ['N', 'S']:
			self.trick_tally += 1
		self.completed_tricks.append(self.current_trick.copy())
		self.trick_no += 1
		self.current_trick = []

	def next_player(self):
		self.current_turn_index = (self.current_turn_index + 1) % 4

	def save_position(self, decision, old_decision, player, hands, trick):
		if old_decision:
			# merge the two lists together to get a set of old decisions made at same point
			decision = decision + old_decision

		self.decision_points.append((
			self.card_no, decision, player, copy.deepcopy(hands), copy.deepcopy(trick), 
			self.trick_tally, self.trick_no, self.completed_tricks.copy()))

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
		# Finally, delete the decision point so we don't reach it again (unless 
		# Decisions.make_decision indicates that we need to)
		del self.decision_points[-1]

	def save_leaf_node(self):
		# Save information about the gameplay leading to this leaf node
		self.leaf_nodes += 1
		self.full_history.append([self.trick_tally, self.completed_tricks.copy()])
		self.completed_tricks = []

if __name__ == '__main__':
	np.random.seed(0)
	d = Deal(2)
	# printer.print_current(d.current_hands)
	# d.play_card('N', 'S14')
	# print(d.current_hands)


