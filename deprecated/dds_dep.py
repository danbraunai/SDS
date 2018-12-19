import copy
import sys
import numpy as np


class DDS:

    def __init__(self, deal):
        self.deal = deal

    def get_valid_moves(self, player, trick, touching=False):
        hand = self.deal.current_hands[player]
        try:
            follow_suit_cards = [i for i in hand if trick[0][1][0] in i]
        except IndexError:
            # We are leading to this trick
            valid_cards = hand[:]
        else:
            if len(follow_suit_cards) == 1:
                valid_cards = follow_suit_cards
            # Check if we have cards to follow suit with
            elif len(follow_suit_cards) > 1:
                if touching:
                    diff_list = np.array(
                        [int(follow_suit_cards[i][1:]) - int(follow_suit_cards[i+1][1:]) 
                        for i in range(len(follow_suit_cards) - 1)])
                    drop_idxs = np.where(diff_list == 1)[0]
                    unique_cards = np.delete(follow_suit_cards, drop_idxs + 1)
                    valid_cards = unique_cards
                else:
                    valid_cards = follow_suit_cards 
                    
            else:
                # No cards to follow suit with. 
                if touching:
                    sorted_hand = sorted(hand, key=lambda x: x[0], reverse=True)
                    diff_value_list = np.array(
                        [int(sorted_hand[i][1:]) - int(sorted_hand[i+1][1:]) for i in range(len(sorted_hand) - 1)])
                    diff_suit_list = np.array(
                        [sorted_hand[i][0] == sorted_hand[i+1][0] for i in range(len(sorted_hand) - 1)])
                    comb = diff_value_list * diff_suit_list
                    drop_idxs = np.where(comb == 1)[0]
                    unique_cards = np.delete(sorted_hand, drop_idxs + 1)
                    valid_cards = unique_cards
                else:
                    # Reverse list as we probably want to search the space of low cards first
                    valid_cards = hand[::-1]
        return valid_cards