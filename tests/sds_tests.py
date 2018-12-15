from nose.tools import *
import sys
import scipy.special
from sds.decisions import Decisions
from sds.displayer import Displayer
from sds.engine import GameEngine
from sds.deal import Deal


def test_create_deal_random_and_defined():
	# This uses the create_deal function to test random and defined inputs for a deal
	d_random = Deal(seed=0)
	create_deal(d_random)

	deal = {'N': set(['C14', 'C13', 'C12', 'C11']), 'E': set(['S14', 'S13', 'H12', 'H11']), 
		'S': set(['D14', 'D13', 'H14', 'H13']), 'W': set(['D12', 'D11', 'S12', 'S11'])}
	d_defined = Deal(deal=deal)
	create_deal(d_defined)

def create_deal(d):

	for position in ['N', 'W', 'E', 'S']:
		# Check all have 4 cards
		assert_equal(len(d.original_deal[position]), 4)
		# Check unique
		assert_equal(len(d.original_deal[position]), len(set(d.original_deal[position])))
	# Check all hands add up to full deck
	assert_equal(set(d.all_cards), set().union(*d.original_deal.values()))


def test_make_lead_and_play_card():
	deal = {'N': set(['C14', 'C13', 'C12', 'C11']), 'E': set(['S14', 'S13', 'H12', 'H11']), 
		'S': set(['D14', 'D13', 'H14', 'H13']), 'W': set(['D12', 'D11', 'S12', 'S11'])}
	d = Deal(deal=deal)
	# This function also runs the play_card function
	d.make_lead()
	assert(d.lead in d.original_deal['W'])
	d.current_hands['W'].add(d.lead)
	assert_equal(d.original_deal, d.current_hands)
	assert_equal(d.card_no, 2)

def test_complete_trick():
	deal = {'N': set(['C14', 'C13', 'C12', 'C11']), 'E': set(['S14', 'S13', 'H12', 'H11']), 
		'S': set(['D14', 'D13', 'H14', 'H13']), 'W': set(['D12', 'D11', 'S12', 'S11'])}
	d = Deal(deal=deal)
	# This function also runs the play_card function
	d.play_card('W', 'S12')
	d.play_card('N', 'C14')
	d.play_card('E', 'S14')
	d.play_card('S', 'H13')
	d.complete_trick()
	# East won the trick
	assert_equal('E', d.play_order[d.current_turn_index])
	assert_equal(d.trick_tally, 0)
	assert_equal(d.card_no, 5)
	assert_equal(d.current_trick, [])

def test_make_decision():
	dec = Decisions()
	decision, decision_point = dec.make_decision(
		'E', set(['S13', 'S14', 'H11']), [('W', 'S12'), ('N', 'H12')], [])
	# This will only work for naive decision maker of picking first valid card
	assert(decision in ['S13', 'S14'])
	assert_equal(decision_point, True)

	decision, decision_point = dec.make_decision(
		'E', set(['H13', 'H14', 'H11']), [('W', 'S12'), ('N', 'H12')], ['H13'])
	# This will only work for naive decision maker of picking first valid card
	assert(decision in ['H14', 'H13', 'H11'])
	assert_equal(decision_point, True)

	decision, decision_point = dec.make_decision(
		'E', set(['S13', 'S14', 'H11']), [('W', 'S12'), ('N', 'H12')], ['S13'])
	# This will only work for naive decision maker of picking first valid card
	assert_equal(decision, 'S14')
	assert_equal(decision_point, False)

def test_play_to_leaf():
	deal = {'N': set(['C14', 'C13', 'C12', 'C11']), 'E': set(['S14', 'S13', 'H12', 'H11']), 
		'S': set(['D14', 'D13', 'H14', 'H13']), 'W': set(['D12', 'D11', 'S12', 'S11'])}
	d = Deal(deal=deal)
	disp = Displayer()
	dec = Decisions()
	e = GameEngine(d, disp, dec)
	e.play_to_leaf()
	assert_equal(d.trick_no, 5)
	assert_equal(d.card_no, 17)
	assert_equal(d.current_trick, [])
	assert_equal(d.leaf_nodes, 1)

def test_play_to_all_leaves():
	d = Deal(seed=0)
	# print(d.original_deal)
	disp = Displayer()
	dec = Decisions()
	e = GameEngine(d, disp, dec)
	e.play_to_all_leaves()
	assert_equal(d.trick_no, 5)
	assert_equal(d.card_no, 17)
	assert_equal(d.current_trick, [])
	# we save this number from a previous run. Good to check we always traverse the whole tree
	assert_equal(d.leaf_nodes, 10104)

def test_generate_possible_layouts():
	d = Deal(seed=0)
	disp = Displayer()
	dec = Decisions()
	e = GameEngine(d, disp, dec)

	layouts = e.generate_layouts(
		'NS', set(['D12', 'D11', 'S12', 'S11']), set(['C14', 'C13', 'C12', 'C11']), played=set([]))

	assert_equal(len(layouts), scipy.special.comb(8, 4))
	my_layout = {'N': set(['C14', 'C13', 'C12', 'C11']), 'E': set(['S14', 'S13', 'H12', 'H11']), 
		'S': set(['D12', 'D11', 'S12', 'S11']), 'W': set(['D14', 'D13', 'H14', 'H13'])}

