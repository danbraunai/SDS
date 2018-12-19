import numpy as np
import sys
from operator import itemgetter
from collections import Counter
import copy

class Deal:

    play_order = ['W', 'N', 'E', 'S']


    def __init__(
            self, seed=None, cards_each=4, trumps=None, hands=None, lead=None, first_turn=None,
            current_turn_index=0, current_trick=None, trick_tally=0, trick_no=1, card_no=1, 
            decision_points=None, last_decisions=None, leaf_nodes=0, full_history=None, 
            card_history_str=''):

        self.all_cards = self.get_new_deck(cards_each)
        # Need either deal or seed
        if hands:
            self.original_hands = hands
        else:
            self.seed = seed
            np.random.seed(seed)
            self.original_hands = self.create_deal(cards_each)

        self.current_hands = copy.deepcopy(self.original_hands)
        self.lead = lead
        self.trumps = trumps
        # self.contract = np.random.randint(0, 5)
        self.trick_tally = trick_tally
        self.trick_no = trick_no
        self.current_trick = [] if current_trick is None else current_trick
        self.current_turn_index = (
            self.play_order.index(first_turn) if first_turn else current_turn_index
            )
        self.first_turn = self.play_order[self.current_turn_index]
        self.card_no = card_no
        self.decision_points = [] if decision_points is None else decision_points
        self.last_decisions = [] if last_decisions is None else last_decisions
        self.completed_tricks = []
        self.leaf_nodes = leaf_nodes
        self.full_history = [] if full_history is None else full_history
        self.card_history_str = card_history_str


    def get_new_deck(self, cards_each):
        # Generate a deck given the number of cards
        possible_cards = np.arange(14, 0, -1)
        subset = possible_cards[:cards_each]
        card_list = [i+str(j) for i in ['S', 'D', 'H', 'C'] for j in subset]
        return card_list

    def create_deal(self, cards_each):

        full_deal = np.random.choice(self.all_cards, len(self.all_cards), replace=False)
        north, east, south, west = np.split(full_deal, 4)

        deal_dict = {
            'N': self.sort_hand(north), 'E': self.sort_hand(east), 
            'S': self.sort_hand(south), 'W': self.sort_hand(west)}
        return deal_dict

    def sort_hand(hand):
        # We put each hand in an order appropriate for pruning in our search tree
        return sorted(hand, key=lambda x: int(x[1:]), reverse=True)

    def make_lead(self, card=None):
        if not card:
            # Choose the max so that we always get the same lead when running experiments
            card = self.current_hands['W'][0]
        self.play_card('W', card)
        self.lead = card

    def play_card(self, player, card):
        self.current_trick.append((player, card))
        self.current_hands[player].remove(card)
        self.card_no += 1
        self.card_history_str += card
        # Next player's turn (unless it's the end of the trick which we deal with in play_to_lead)
        self.current_turn_index = (self.current_turn_index + 1) % 4

        if len(self.current_trick) == 4:
            self.complete_trick()

    def complete_trick_nt(self):
        valid_cards = [i for i in self.current_trick if i[1][0] == self.current_trick[0][1][0]]
        # Get the position of the winner of the trick (N, S, E, W)
        # winner = max(valid_cards, key=itemgetter(1))[0]
        winner = max(valid_cards, key=lambda x: int(x[1][1:]))[0]

        self.current_turn_index = self.play_order.index(winner)
        if winner in ['N', 'S']:
            self.trick_tally += 1
        self.completed_tricks.append(self.current_trick.copy())
        self.trick_no += 1
        self.current_trick = []

    def complete_trick_suit(self, trumps):

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


