from deal import Deal
from decisions import Decisions
from simulator import Simulator

class Engine:

    def __init__(self, decisions, simulator):
        self.decisions = decisions
        self.simulator = simulator

    def run_sims_position(self, player_layouts, lead):
        """
        For each player (NS combined), we play out the full game tree for every possible
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

    def play_to_leaf(self, deal, sims=None, random=True):
        """
        The sims argument contains the complete game trees of all possible layouts from the 
        perspective of each player. When left blank, the player will just play randomly/naively
        """

        # print("Lead: ", self.deal.lead)
        # print(displayer.print_hands(self.deal.original_hands))

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

            deal.restore_position(last_decision_position)

            # Play the hand again from a specific position, noting down the card number and card
            # of the last decision made
            deal = self.play_to_leaf(deal, random=True)

        return deal.full_history


if __name__ == '__main__':

    decisions = Decisions()
    simulator = Simulator()

    game = Engine(decisions, simulator)
    # game.play_to_leaf()
    # game.play_to_all_leaves()