import copy
import sys
import numpy as np


class DDS:

    def __init__(self, deal):
        self.deal = deal

    def get_valid_moves(self, player, trick):
        hand = self.deal.current_hands[player]
        try:
            follow_suit_cards = [i for i in hand if trick[0][1][0] in i]
        except IndexError:
            # We are leading to this trick
            valid_cards = hand[:]
        else:
            # Check if we have cards to follow suit with
            if len(follow_suit_cards) >= 1:
                valid_cards = follow_suit_cards                    
            else:
                # No cards to follow suit with. 
                # Reverse list as we probably want to search the space of low cards first
                valid_cards = hand[::-1]
        return valid_cards

    def get_move(self):
        """
        This function doesn't care about the utilities of all possible moves, it just picks the 
        best one. This allows greater pruning capabilities
        """
        player = self.deal.play_order[self.deal.current_turn_index]

        if player in ['N', 'S']:
            # It is now N or S's turn, they want to maximize the number of tricks
            move, _ = self.maximize(-np.inf, np.inf)
        else:
            # It is now E or W's turn, they want to mazimize the number of tricks
            move, _ = self.minimize(-np.inf, np.inf)  

        return move

    def get_utilities(self):
        # find the card which gives us the highest utility (average number of tricks)
        # depth = 0
        player = self.deal.play_order[self.deal.current_turn_index] 
        current_hand = self.deal.current_hands[player].copy()

        valid_moves = self.get_valid_moves(player, self.deal.current_trick)

        utility_dict = {}
        # Play each card in the hand, and evaluate utility after that
        for card in valid_moves:
            # Need to save the state of deal, since we will be exploring leaves and changing it
            current_position = self.deal.save_position()

            self.deal.play_card(player, card)

            if self.deal.play_order[self.deal.current_turn_index] in ['N', 'S']:
                # It is now N or S's turn after the card was played they want to mazimize
                _, utility = self.maximize(-np.inf, np.inf)
            else:
                # It is now E or W's turn after the card was played, they want to minimize 
                _, utility = self.minimize(-np.inf, np.inf)

            utility_dict[card] = utility

            # restore the deal object to same state as before playing the first card
            self.deal.restore_position(current_position)          

        return utility_dict

    # @profile
    def maximize(self, alpha, beta):
        # depth += 1
        current_player = self.deal.play_order[self.deal.current_turn_index]

        cards_left = set().union(*self.deal.current_hands.values())

        if len(cards_left) == 4:
            self.deal.play_last_trick()
            return (None, self.deal.trick_tally)

        (max_child, max_utility) = (None, -np.inf)

        valid_moves = self.get_valid_moves(current_player, self.deal.current_trick)

        for child in valid_moves:
            current_position = self.deal.save_position()

            self.deal.play_card(current_player, child)

            # If still N or S turn (they won the trick), maximize again, otherwise, minimize
            if self.deal.current_turn_index in [1, 3]:
                (_, utility) = self.maximize(alpha, beta)
            else:
                (_, utility) = self.minimize(alpha, beta)

            if utility > max_utility:
                (max_child, max_utility) = (child, utility)

            if max_utility >= beta:
                self.deal.restore_position(current_position)
                break
            if max_utility > alpha:
                alpha = max_utility

            self.deal.restore_position(current_position)

        # depth -= 1
        return (max_child, max_utility)

    def minimize(self, alpha, beta):
        # depth += 1
        current_player = self.deal.play_order[self.deal.current_turn_index]

        cards_left = set().union(*self.deal.current_hands.values())


        if len(cards_left) == 4:
            self.deal.play_last_trick()
            return (None, self.deal.trick_tally)

        (min_child, min_utility) = (None, np.inf)

        valid_moves = self.get_valid_moves(current_player, self.deal.current_trick)

        for child in valid_moves:
            current_position = self.deal.save_position()

            self.deal.play_card(current_player, child)

            # If still E or W turn (they won the trick), minimize again, otherwise, minimize
            if self.deal.current_turn_index in [1, 3]:
                (_, utility) = self.maximize(alpha, beta)
            else:
                (_, utility) = self.minimize(alpha, beta)

            if utility < min_utility:
                (min_child, min_utility) = (child, utility)

            if min_utility <= alpha:
                self.deal.restore_position(current_position)
                break
            if min_utility < beta:
                beta = min_utility

            self.deal.restore_position(current_position)

        # depth -= 1
        return (min_child, min_utility)        