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
            valid_cards = hand
        else:
            if follow_suit_cards:
                valid_cards = follow_suit_cards
            else:
                # No cards to follow suit with
                valid_cards = hand

        # valid_cards = sorted(list(valid_cards), reverse=True)
        valid_cards = list(valid_cards)
        return valid_cards

    # finds child with highest utility
    def get_decision(self):
        depth = 0
        player = self.deal.play_order[self.deal.current_turn_index]
        current_hand = self.deal.current_hands[player].copy()

        # Need to save the state of deal as it will change when we explore each possible action 
        current_position = self.deal.save_position_dds()
        valid_moves = self.get_valid_moves(player, self.deal.current_trick)

        utility_dict = {}
        # Play each card in the hand, and evaluate utility after that
        for card in valid_moves:

            # Need to save the state of deal, since we will be exploring leaves and changing it
            current_position = self.deal.save_position_dds()

            self.deal.play_card_dds(player, card)

            if player in ['N', 'S']:
                # It is now E or W's turn, they want to minimize 
                _, utility = self.minimize(depth, -np.inf, np.inf)
            else:
                # It is now N or S's turn they want to mazimize
                _, utility = self.maximize(depth, -np.inf, np.inf)

            utility_dict[card] = utility

            # restore the deal object to same state as before playing the first card
            self.deal.restore_position_dds(current_position)            

        return utility_dict

    # @profile
    def maximize(self, depth, alpha, beta):
        depth += 1
        current_player = self.deal.play_order[self.deal.current_turn_index]

        cards_left = set().union(*self.deal.current_hands.values())

        if len(cards_left) == 4:
            self.deal.play_last_trick()
            return (None, self.deal.trick_tally)

        # if len(self.deal.current_hands[current_player]) == 0:
        #     return (None, self.deal.trick_tally)

        (max_child, max_utility) = (None, -np.inf)

        valid_moves = self.get_valid_moves(current_player, self.deal.current_trick)

        for child in valid_moves:
            # Need to save the state of deal, since we will be exploring leaves and changing it
            current_position = self.deal.save_position_dds()

            # print(
            #     f"{current_player} playing card {child} at state" 
            #     f"{self.deal.current_hands[current_player]}\n")
            self.deal.play_card_dds(current_player, child)

            # If still N or S turn (they won the trick), maximize again, otherwise, minimize
            if self.deal.current_turn_index in [1, 3]:
                (_, utility) = self.maximize(depth, alpha, beta)
            else:
                (_, utility) = self.minimize(depth, alpha, beta)

            if utility > max_utility:
                (max_child, max_utility) = (child, utility)

            if max_utility >= beta:
                self.deal.restore_position_dds(current_position)
                pass
            if max_utility > alpha:
                alpha = max_utility

            # restore the deal object to same state as before exploring the child
            self.deal.restore_position_dds(current_position)

        depth -= 1

        return (max_child, max_utility)

    def minimize(self, depth, alpha, beta):
        depth += 1
        current_player = self.deal.play_order[self.deal.current_turn_index]

        cards_left = set().union(*self.deal.current_hands.values())


        if len(cards_left) == 4:
            self.deal.play_last_trick()
            return (None, self.deal.trick_tally)

        # if len(self.deal.current_hands[current_player]) == 0:
        #     return (None, self.deal.trick_tally)

        (min_child, min_utility) = (None, np.inf)

        valid_moves = self.get_valid_moves(current_player, self.deal.current_trick)

        for child in valid_moves:
            # Need to save the state of deal, since we will be exploring leaves and changing it
            current_position = self.deal.save_position_dds()
            # print(
            #     f"{current_player} playing card {child} at state" 
            #     f"{self.deal.current_hands[current_player]}\n")
            self.deal.play_card_dds(current_player, child)

            # If still E or W turn (they won the trick), minimize again, otherwise, minimize
            if self.deal.current_turn_index in [1, 3]:
                (_, utility) = self.maximize(depth, alpha, beta)
            else:
                (_, utility) = self.minimize(depth, alpha, beta)

            if utility < min_utility:
                (min_child, min_utility) = (child, utility)

            if min_utility <= alpha:
                self.deal.restore_position_dds(current_position)
                break
            if min_utility < beta:
                beta = min_utility

            # restore the deal object to same state as before exploring the child
            self.deal.restore_position_dds(current_position)

        depth -= 1
        return (min_child, min_utility)        