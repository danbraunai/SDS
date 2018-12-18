import numpy as np
import pandas as pd
import sys
import time

from displayer import Displayer
from deal import Deal
from decisions import Decisions
from simulator import Simulator
from dds import DDS

class GameEngine:

    def __init__(self, displayer, decisions, simulator):
        self.displayer = displayer
        self.decisions = decisions
        self.simulator = simulator

    def play_to_leaf(self, deal, sims=None, random=True):
        """
        The sims argument contains the complete game trees of all possible layouts from the 
        perspective of each player. When left blank, the player will just play randomly/naively
        """

        # print("Lead: ", self.deal.lead)
        # print(self.displayer.print_hands(self.deal.original_hands))

        # Play the lead automatically
        # self.deal.play_card('W', self.current_hands['W'][0])

        while deal.trick_no < 5:
            current_player = deal.play_order[deal.current_turn_index]
            current_hands = deal.current_hands
            current_trick = deal.current_trick
            last_decisions = deal.last_decisions

            decision, decision_point, sims = (
                self.decisions.make_decision(
                    current_player, current_hands[current_player].copy(), current_trick, 
                    last_decisions, deal.card_history_str, sims, random))

            # if there were other potential cards to play, save the state of the game at this card.
            if decision_point:
                deal.save_position(
                    [decision], last_decisions, current_player, current_hands, current_trick)

            # Once we've used the old decision to make a new decision, we don't need it anymore
            deal.last_decisions = None

            deal.play_card(current_player, decision)

            if len(deal.current_trick) == 4:
                deal.complete_trick()

        deal.save_leaf_node()
        return deal

    def play_to_all_leaves(self, deal):
        # Play hand for the first time, reaching our first leaf node and noting down all other
        # decision nodes in self.decision_points 
        deal = self.play_to_leaf(deal, random=True)
        # While there are still unexplored areas of game tree, go back to most recent decision
        # and make another one

        while deal.decision_points:
            last_decision_position = deal.decision_points[-1]

            # print(last_decisions)
            # print("Decisions left = ", len(deal.decision_points), '\n')
            # print(deal.decision_points)
            # sys.exit(1)
            deal.restore_position(last_decision_position)
            # print(last_decisions_position)
            # Play the hand again from a specific position, noting down the card number and card
            # of the last decision made
            deal = self.play_to_leaf(deal, random=True)

        # print(deal.leaf_nodes)
        # print(deal.completed_tricks)

        # print(np.array(deal.full_history))
        # print(np.array(deal.full_history, dtype=[('x', str), ('y', int)]))
        # print(np.array([('1.0', 2), ('3.0', 4)], dtype=[('x', f'U{self.max_str}'), ('y', int)]))
        # sys.exit(1)
        # game_tree_results = np.array(
        #   deal.full_history, dtype=[('hands', f'U{self.max_str}'), ('tricks', int)])

        return deal.full_history

    def run_sims_position(self, player_layouts, lead):
        """
        For each player (NS combined), we solve the full game tree for every possible
        combination of hands that their opponents may have after the lead
        """
        all_sims = []

        for position_layouts in player_layouts:
            simulations = {}
            for full_hands in position_layouts:
                new_deal = Deal(deal=full_hands)
                new_deal.make_lead(lead)
                simulations.update(self.play_to_all_leaves(new_deal))

            all_sims.append(simulations)

        return all_sims

    def run_dds(self):
        deal1 = {'N': set(['C14', 'C11']), 'E': set(['C13', 'S13']), 
            'S': set(['D14', 'H13']), 'W': set(['S14', 'S11'])}
        deal2 = {'N': set(['C14', 'C13', 'C12', 'C11']), 'E': set(['S14', 'S13', 'H12', 'H13']), 
        'S': set(['D14', 'D11', 'H14', 'H11']), 'W': set(['D12', 'D13', 'S12', 'S11'])}
        deal3 = {'N': set(['C14', 'S13']), 'E': set(['D14']), 'S': set(['D11']), 
            'W': set(['S14', 'S11'])}
        current_trick = [('E', 'S10'), ('S', 'H10')]
        # self.displayer.print_hands(deal2)
        # d = Deal(deal=deal3, current_turn_index=0, current_trick=current_trick)
        # dds = DDS(d)
        # self.displayer.print_hands(d.original_hands)
        # start_time = time.time()
        # utility_dict = dds.get_decision()
        # print(utility_dict)
        # # print(f"DDS says playing {decision} will bring {utility} tricks")
        # print(f"Time Taken = {time.time() - start_time}")
        # sys.exit(1)

        # Let south start this hand
        for i in range(10,11):
            d = Deal(seed=i, current_turn_index=3)
            dds = DDS(d)
            self.displayer.print_hands(d.original_hands)
            start_time = time.time()
            utility_dict = dds.get_decision()
            print(utility_dict)
            # print(f"DDS says playing {decision} will bring {utility} tricks")
            print(f"Time Taken = {time.time() - start_time}")

    def start(self):
        # start_time = time.time()
        seed = 5
        deal1 = Deal(seed=seed)
        self.displayer.print_hands(deal1.current_hands)

        # deal1.make_lead()
        # self.displayer.print_hands(deal1.current_hands)
        # print("Lead of", deal1.lead)
        player = deal1.play_order[deal1.current_turn_index]
        start_time = time.time()
        all_layouts = self.simulator.find_layouts(deal1, player, lead=True)

        print(f"{len(all_layouts)} possible layouts")
        print(f"Time Taken = {time.time() - start_time}")
        sys.exit(1)
        # print(all_layouts)
        # sys.exit(1)
        # self.displayer.print_deal_info(deal1)
        # sys.exit(1)
        start_time = time.time()
        result_list = []
        for layout in all_layouts:
            d = Deal(
                hands=layout, current_turn_index=deal1.current_turn_index, 
                current_trick=deal1.current_trick.copy())
            dds = DDS(d)
            # self.displayer.print_hands(d.original_hands)

            # self.displayer.print_deal_info(d)
            utility_dict = dds.get_decision()
            # print(utility_dict)
            result_list.append(utility_dict.copy()) 

        df = pd.DataFrame(result_list)
        # print(df)
        print(df.mean())
        print(f"Time Taken = {time.time() - start_time}")
        sys.exit(1)
        # all_sims = self.run_sims_position([layouts_NS, layouts_E, layouts_W], deal1.lead)
        # self.simulator.save_sims(all_sims, seed)

        # sims = self.simulator.load_sims(seed)
        # history = self.play_to_all_leaves(deal1)
        # print(history)
        # sys.exit(1)

        # d = self.play_to_leaf(deal1, sims, random=False)
        # print(self.displayer.print_hands(d.original_hands))
        # print(d.full_history)



if __name__ == '__main__':

    displayer = Displayer()
    decisions = Decisions()
    simulator = Simulator()
    # start_time = time.time()

    game = GameEngine(displayer, decisions, simulator)
    game.start()
    # game.run_dds()
    # game.play_to_leaf()
    # game.play_to_all_leaves()

    # start_time = time.time()
    # for seed in np.arange(100000):
    #   deal = Deal(seed)
    #   game = GameEngine(deal, displayer)
    #   game.play_hand()
    # print("Time Taken: ", time.time() - start_time)
