import numpy as np
import sys
import itertools
from deal import Deal

class Displayer:

	def print_hands(self, hands):
		north = sorted(hands['N'], reverse=True)
		east = sorted(hands['E'], reverse=True)
		south = sorted(hands['S'], reverse=True)
		west = sorted(hands['W'], reverse=True)

		north_spades = [i for i in north if 'S' in i]
		north_hearts = [i for i in north if 'H' in i]
		north_diamonds = [i for i in north if 'D' in i]
		north_clubs = [i for i in north if 'C' in i]
		north_zipped = list(itertools.zip_longest(
			north_spades, north_hearts, north_diamonds, north_clubs, fillvalue='   '))
		for row in north_zipped:
			print('\t\t', ' '.join(row))

		east_spades = [i for i in east if 'S' in i]
		east_hearts = [i for i in east if 'H' in i]
		east_diamonds = [i for i in east if 'D' in i]
		east_clubs = [i for i in east if 'C' in i]
		east_zipped = list(itertools.zip_longest(
			east_spades, east_hearts, east_diamonds, east_clubs, fillvalue='   '))
		west_spades = [i for i in west if 'S' in i]
		west_hearts = [i for i in west if 'H' in i]
		west_diamonds = [i for i in west if 'D' in i]
		west_clubs = [i for i in west if 'C' in i]
		west_zipped = list(itertools.zip_longest(
			west_spades, west_hearts, west_diamonds, west_clubs, fillvalue='   '))

		ew_zip = list(itertools.zip_longest(west_zipped, east_zipped))

		print('\n')
		for row in ew_zip:
			if not row[0]:
				print('\t'*4, ' '.join(row[1]))
			elif not row[1]:
				print(' '.join(row[0]), '\t'*4)
			else:
				print(' '.join(row[0]), '\t\t', ' '.join(row[1]))

		south_spades = [i for i in south if 'S' in i]
		south_hearts = [i for i in south if 'H' in i]
		south_diamonds = [i for i in south if 'D' in i]
		south_clubs = [i for i in south if 'C' in i]
		south_zipped = list(itertools.zip_longest(
			south_spades, south_hearts, south_diamonds, south_clubs, fillvalue='   '))
		print('\n')
		for row in south_zipped:
			print('\t\t', ' '.join(row))
		print('\n')

	def print_deal_info(self, d):
		# print(d.original_hands)

		print("Current hands:",d.current_hands)
		print("Current trick tally:", d.trick_tally)
		print("Current trick:", d.current_trick)
		print("Current turn:", d.play_order[d.current_turn_index])

