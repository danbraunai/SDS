import sys
import time
import numpy as np

class Decisions:
	def __init__(self):	
		self.player_sim_map = {'N': 0, 'S': 0, 'E': 1, 'W': 2}

	def make_decision(
		self, player, hand, trick, old_decision, history=None, sims=None, random=True):
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

		if random:
			# decision = valid_cards.pop()
			decision = max(list(valid_cards))

		else:
			current_sim = sims[self.player_sim_map[player]]
			# Other options decided against for the moment
			# result_str = [(his[6:], trick) for his,trick in sims[1] if his[:6] == history][:10]
			# result_arr = np.array(result_str)
			# results = [i.lstrip(history) for i in sims[1][:,0]]
			# 	results = [i.lstrip(history) for i in sims[1][:,0]]

			# See how many characters (no_cards * 3) in the history are already accounted for
			# in our sim. 
			chars_played_sim = 48 - len(current_sim[0,0])

			# Remove the cards already accounted for from the history
			recent_history = history[chars_played_sim:]

			bool_arr = np.core.defchararray.startswith(
				current_sim[:,0], recent_history)

			filtered_sim = current_sim[bool_arr,:]
			# Remove the recent cards played from our sims
			filtered_sim[:,0] = np.array([i[len(recent_history):] for i in filtered_sim[:,0]])

			if filtered_sim.size == 0:
				print(f'Our simulations for {player} are not valid')
				print(f'Current history is {history}')
				sys.exit(1)

			sims[self.player_sim_map[player]] = filtered_sim

			if player in ['E', 'W']:
				optimal_function = min
			else:
				optimal_function = max

			best_sims = filtered_sim[
				np.where(filtered_sim[:,1] == optimal_function(filtered_sim[:,1]))]

			decision = best_sims[len(best_sims)-1,0][:3]
			# decision = best_sims[0,0][:3]


		return decision, decision_point, sims