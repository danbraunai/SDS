import numpy as np
import sys
import itertools

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
		ew_zip = list(zip(west_zipped, east_zipped))
		print('\n')
		for row in ew_zip:
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



