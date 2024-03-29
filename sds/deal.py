import numpy as np
import sys
from operator import itemgetter
from collections import Counter
import copy

class Deal:

    play_order = ['W', 'N', 'E', 'S']

    def __init__(
            self, seed=None, cards_each=4, trumps=None, hands=None, first_turn=None,
            current_turn_index=0, current_trick=None, trick_tally=0, trick_no=1, 
            ):

        self.all_cards = self.get_new_deck(cards_each)
        # Need either deal or seed
        if hands:
            self.original_hands = hands
        else:
            self.seed = seed
            np.random.seed(seed)
            self.original_hands = self.create_deal(cards_each)

        self.current_hands = copy.deepcopy(self.original_hands)
        self.trumps = trumps
        # self.contract = np.random.randint(0, 5)
        self.trick_tally = trick_tally
        self.trick_no = trick_no
        self.current_trick = [] if current_trick is None else current_trick
        self.current_turn_index = (
            self.play_order.index(first_turn) if first_turn else current_turn_index
            )
        self.first_turn = self.play_order[self.current_turn_index]

    def get_new_deck(self, cards_each):
        # Generate a deck of cards given the number of cards
        possible_cards = np.arange(14, 0, -1)
        subset = possible_cards[:cards_each]
        card_list = [i+str(j) for i in ['S', 'D', 'H', 'C'] for j in subset]
        return card_list

    def create_deal(self, cards_each):
        # Randomly distribute cards to the players
        full_deal = np.random.choice(self.all_cards, len(self.all_cards), replace=False)
        north, east, south, west = np.split(full_deal, 4)

        deal_dict = {
            'N': self.sort_hand(north), 'E': self.sort_hand(east), 
            'S': self.sort_hand(south), 'W': self.sort_hand(west)}
        return deal_dict

    def sort_hand(self, hand):
        # We put each hand in an order appropriate for pruning in our search tree
        return sorted(hand, key=lambda x: int(x[1:]), reverse=True)

    # @profile
    def play_card(self, player, card):
        self.current_trick.append((player, card))
        self.current_hands[player].remove(card)
        # If there are 4 cards played to this trick, tie it off.
        if len(self.current_trick) == 4:
            if self.trumps:
                self.complete_trick_suit(self.trumps)
            else:
                self.complete_trick_nt()
        else:
            # Next player's turn in the queue
            self.current_turn_index = (self.current_turn_index + 1) % 4

    def complete_trick_nt(self):
        # Get the biggest card which is the same suit as the first card played to trick
        valid_cards = [i for i in self.current_trick if i[1][0] == self.current_trick[0][1][0]]
        # Get the position of the winner of the trick (N, S, E, W)
        winner = max(valid_cards, key=lambda x: int(x[1][1:]))[0]

        self.current_turn_index = self.play_order.index(winner)

        if winner in ['N', 'S']:
            self.trick_tally += 1

        self.trick_no += 1
        self.current_trick = []

    def complete_trick_suit(self, trumps):
        # Get the trumps played to this trick
        valid_trumps = [i for i in self.current_trick if i[1][0] == trumps]

        if len(valid_trumps) == 1:
            winner = valid_trumps[0][0]
        elif len(valid_trumps) > 1:
            winner = max(valid_trumps, key=lambda x: int(x[1][1:]))[0]
        else:
            valid_cards = [
                i for i in self.current_trick if i[1][0] == self.current_trick[0][1][0]
                ]
            winner = max(valid_cards, key=lambda x: int(x[1][1:]))[0]

        self.current_turn_index = self.play_order.index(winner)

        if winner in ['N', 'S']:
            self.trick_tally += 1

        self.trick_no += 1
        self.current_trick = []

    # @profile
    def save_position(self):
        # This is much faster than doing a deep copy of the whole dict, probably can do 
        # much better still though
        current_hands_copy = [self.current_hands[i].copy() for i in self.play_order]
        idx = self.current_turn_index
        trick_copy = self.current_trick.copy()
        tally = self.trick_tally

        position = (current_hands_copy, idx, trick_copy, tally)
        return position


    def restore_position(self, position):
        hands_copy, self.current_turn_index, self.current_trick, self.trick_tally = position
        self.current_hands = {
            'N': hands_copy[1], 'E': hands_copy[2], 'S': hands_copy[3], 'W': hands_copy[0]
            } 

    # @profile
    def play_last_trick(self):
        # This just speeds up in our dds algorithm compared to go inside minimize and maximimize
        # when everyone has one card left

        for i in range(4):
            player = self.play_order[self.current_turn_index]
            card = self.current_hands[player].pop()
            self.current_trick.append((player, card))
            self.current_turn_index = (self.current_turn_index + 1) % 4

        valid_cards = [i for i in self.current_trick if i[1][0] == self.current_trick[0][1][0]]

        winner = max(valid_cards, key=itemgetter(1))[0]
        if winner in ['N', 'S']:
            self.trick_tally += 1


if __name__ == '__main__':
    d = Deal(2)
    # printer.print_current(d.current_hands)
    # d.play_card('N', 'S14')
    # print(d.current_hands)


