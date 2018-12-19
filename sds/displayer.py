import numpy as np
import sys
import itertools
import copy


def print_hands(hands, filename=None):
	# Make a nice display for a deal
	hands_copy = copy.deepcopy(hands)

	# If we have single digit values, add a trailing space to them
	for position in hands_copy:
		hands_copy[position] = [i + ' ' if (len(i) == 2) else i for i in hands_copy[position]]

	north_spades = [i for i in hands_copy['N'] if 'S' in i]
	north_hearts = [i for i in hands_copy['N'] if 'H' in i]
	north_diamonds = [i for i in hands_copy['N'] if 'D' in i]
	north_clubs = [i for i in hands_copy['N'] if 'C' in i]
	north_zipped = list(itertools.zip_longest(
		north_spades, north_hearts, north_diamonds, north_clubs, fillvalue='   '))
	east_spades = [i for i in hands_copy['E'] if 'S' in i]
	east_hearts = [i for i in hands_copy['E'] if 'H' in i]
	east_diamonds = [i for i in hands_copy['E'] if 'D' in i]
	east_clubs = [i for i in hands_copy['E'] if 'C' in i]
	east_zipped = list(itertools.zip_longest(
		east_spades, east_hearts, east_diamonds, east_clubs, fillvalue='   '))
	west_spades = [i for i in hands_copy['W'] if 'S' in i]
	west_hearts = [i for i in hands_copy['W'] if 'H' in i]
	west_diamonds = [i for i in hands_copy['W'] if 'D' in i]
	west_clubs = [i for i in hands_copy['W'] if 'C' in i]
	west_zipped = list(itertools.zip_longest(
		west_spades, west_hearts, west_diamonds, west_clubs, fillvalue='   '))

	ew_zip = list(itertools.zip_longest(west_zipped, east_zipped))

	south_spades = [i for i in hands_copy['S'] if 'S' in i]
	south_hearts = [i for i in hands_copy['S'] if 'H' in i]
	south_diamonds = [i for i in hands_copy['S'] if 'D' in i]
	south_clubs = [i for i in hands_copy['S'] if 'C' in i]
	south_zipped = list(itertools.zip_longest(
		south_spades, south_hearts, south_diamonds, south_clubs, fillvalue='   '))

	if filename:
		with open(filename, 'a') as f:	
			f.write('\n')
			for row in north_zipped:
				f.write(f"\t\t\t\t{' '.join(row)}\n")
			f.write('\n')
			for row in ew_zip:
				if not row[0]:
					f.write(f"\t\t\t\t\t\t\t\t{' '.join(row[1])}\n")
				elif not row[1]:
					f.write(f"{' '.join(row[0])}\n")
				else:
					f.write(f"{' '.join(row[0])}\t\t\t\t\t{' '.join(row[1])}\n")
			f.write('\n')
			for row in south_zipped:
				f.write(f"\t\t\t\t{' '.join(row)}\n")
			f.write('\n')
	else:
		for row in north_zipped:
			print('\t\t', ' '.join(row))
		print('\n')
		for row in ew_zip:
			if not row[0]:
				print('\t'*4, ' '.join(row[1]))
			elif not row[1]:
				print(' '.join(row[0]), '\t'*4)
			else:
				print(' '.join(row[0]), '\t\t', ' '.join(row[1]))
		print('\n')
		for row in south_zipped:
			print('\t\t', ' '.join(row))
		print('\n')

def print_deal_info(d):
	print("Current hands:",d.current_hands)
	print("Current trick tally:", d.trick_tally)
	print("Current trick:", d.current_trick)
	print("Current turn:", d.play_order[d.current_turn_index])

