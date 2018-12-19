import numpy as np
import pandas as pd
import sys
import os
import time
import copy
from multiprocessing import Pool
import importlib

import displayer
import simulator
from deal import Deal
from dds import DDS

dir = os.path.dirname(__file__)


class Engine:

    def run_dds(self):
        # deal1 = {'N': ['C14', 'C13', 'C12', 'C11'], 'E': ['S14', 'S13', 'H12', 'H13'], 
        # 'S': ['D14', 'D11', 'H14', 'H11'], 'W': ['D12', 'D13', 'S12', 'S11']}
        # displayer.print_hands(deal1)
        # d = Deal(hands=deal1, current_trick=current_trick)
        # dds = DDS(d)

        # start_time = time.time()
        # utility_dict = dds.get_decision()
        # print(utility_dict)
        # # print(f"DDS says playing {decision} will bring {utility} tricks")
        # print(f"Time Taken = {time.time() - start_time}")
        # sys.exit(1)

        start_time = time.time()
        # Let south start this hand
        for i in range(0,800):
            # seed = np.random.randint(1000)
            d = Deal(seed=i, cards_each=4, current_turn_index=3, trumps=None)
            dds = DDS(d)
            # displayer.print_hands(d.original_hands)
            # print("Trumps:", d.trumps)
            # utility_dict = dds.get_utilities()
            move = dds.get_move()
            # print(move)
            # print(utility_dict)

        print(f"Time Taken = {time.time() - start_time}")

    def sds(self, layouts, deal):
        """
        This runs a dds for every possible layout as viewed from the current player. And then
        aggregates the results by taking the mean number of tricks for each card
        """

        results_list = []
        for layout in layouts:
            d = Deal(
                hands=layout, current_turn_index=deal.current_turn_index, 
                current_trick=deal.current_trick.copy(), trumps=deal.trumps)
            dds = DDS(d)
            # displayer.print_hands(d.original_hands)

            # displayer.print_deal_info(d)
            utility_dict = dds.get_utilities()
            # print(utility_dict)
            results_list.append(utility_dict.copy()) 

        df = pd.DataFrame(results_list)
        return df

    def sds_multiprocess(self, layout, deal):
            d = Deal(
                hands=layout, current_turn_index=deal.current_turn_index, 
                current_trick=deal.current_trick.copy(), trumps=deal.trumps)
            dds = DDS(d)
            # displayer.print_hands(d.original_hands)
            # displayer.print_deal_info(d)
            utility_dict = dds.get_utilities()
            return utility_dict


    def run_example(self):
        # Read in our example and import it as a module
        module_name = 'Examples.' + sys.argv[1]
        example = importlib.import_module(module_name, package=None)

        outfile_name = 'Examples/' + sys.argv[1] + '_output.txt'

        try:
            trumps = example.trumps
        except AttributeError:
            trumps = None
        try:
            first_turn = example.first_turn
        except AttributeError:
            first_turn = 'W'
        try:
            current_trick = example.current_trick
        except AttributeError:
            current_trick = None


        if hasattr(example, 'hands'):
            deal = Deal(hands=example.hands, trumps=example.trumps, 
                        first_turn=example.first_turn, current_trick=example.current_trick)
        else:
            # Probably want a random hand instead of a defined hand
            deal = Deal(seed=example.seed, cards_each=example.cards_each, 
                        trumps=example.trumps, first_turn=example.first_turn)


        # Note: make this write to output instead
        displayer.print_hands(deal.current_hands, outfile_name)
        # displayer.print_hands(deal.current_hands)

        outfile = open(outfile_name, 'a')
        outfile.write(f"Trumps: {deal.trumps}\n")
        outfile.write(f"Current trick: {deal.current_trick}\n")
        outfile.write(f"{first_turn}'s turn\n")
        # print("Trumps:", deal.trumps)
        player = deal.play_order[deal.current_turn_index]

        start_time = time.time()
        all_layouts = simulator.find_layouts(deal, player, on_lead=False)
        outfile.write(f"{len(all_layouts)} possible layouts\n\n")
        # print(f"{len(all_layouts)} possible layouts")

        if hasattr(example, 'multiprocessing') and example.multiprocessing:
            # if example.multiprocessing:
            all_args = [[i] + [deal] for i in all_layouts]
            start_time = time.time()
            with Pool() as pool:
                results = pool.starmap(self.sds_multiprocess, all_args)
            df = pd.DataFrame(results)
        else:
            df = self.sds(all_layouts, deal)

        # print(df.mean())
        # print(type(df.mean()))
        df.mean().to_csv(outfile, sep=' ')

        outfile.write(f"\nTime Taken = {time.time() - start_time}\n")
        # print(f"Time Taken = {time.time() - start_time}")
        outfile.close()
        sys.exit(1)


    def start(self):
        # start_time = time.time()
        seed = 14
        # seed = np.random.randint(100)
        deal1 = Deal(seed=seed, cards_each=4, first_turn='S')
        print("Seed =", seed)

        displayer.print_hands(deal1.current_hands)
        print("Trumps:", deal1.trumps)
        # deal1.play_card('W', deal1.current_hands['W'][0])
        # print("Lead of", deal1.lead)
        player = deal1.play_order[deal1.current_turn_index]

        # start_time = time.time()
        all_layouts = simulator.find_layouts(deal1, player, on_lead=False)

        print(f"{len(all_layouts)} possible layouts")
        # print(f"Time Taken = {time.time() - start_time}")
        # displayer.print_hands(all_layouts[0])
        start_time = time.time()
        df = self.sds(all_layouts, deal1)
        mean_df = df.mean()
        print(mean_df)
        print(f"Time Taken = {time.time() - start_time}")
        sys.exit(1)

        all_args = [[i] + [deal1] for i in all_layouts[:10000]]
        start_time = time.time()
        with Pool() as pool:
            results = pool.starmap(self.sds_multiprocess, all_args)

        df = pd.DataFrame(results)
        print(df.head())
        print(df.mean())
        print(f"Time Taken = {time.time() - start_time}")
        sys.exit(1)

        result_list = []
        for layout in all_layouts[:1000]:
            d = Deal(
                hands=layout, current_turn_index=deal1.current_turn_index, 
                current_trick=deal1.current_trick.copy())
            dds = DDS(d)
            # displayer.print_hands(d.original_hands)

            # displayer.print_deal_info(d)
            utility_dict = dds.get_decision()
            # print(utility_dict)
            result_list.append(utility_dict.copy()) 

        df = pd.DataFrame(result_list)
        print(df.mean())
        print(f"Time Taken = {time.time() - start_time}")
        sys.exit(1)


if __name__ == '__main__':

    game = Engine()

    game.run_example()
    # game.start()
    # game.run_dds()

