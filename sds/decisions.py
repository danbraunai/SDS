import sys
from deal import Deal

class Decisions:

	def make_decision(self, player, hand, trick, old_decision):
		# print("Current Player: ", player)
		# Work out which cards we can play

		if old_decision:
			hand = [i for i in hand if i not in old_decision]

		try:
			follow_suit_cards = [i for i in hand if trick[0][1][0] in i]
		except IndexError:
			# We are leading to this trick
			valid_cards = hand
		else:
			if follow_suit_cards:
				valid_cards = follow_suit_cards
			else:
				# No cards to follow suit with
				valid_cards = hand

		if len(valid_cards) > 1:
			decision_point = True
		else:
			decision_point = False
		# print("Valid Cards: ", valid_cards)

		decision = valid_cards[0]


		# if old_decision:
		# 	print(old_decision)
		# 	print(decision)
		# 	print(decision_point)
			# sys.exit(1)

		return decision, decision_point