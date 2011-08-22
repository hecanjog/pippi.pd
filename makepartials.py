#!/usr/lib/env python

import time, os, random

def main():
	# loop until death
	while True:
		for i in range(3):
			rank = random.randrange(1, 16, 5)
			energy = random.random()
			os.system('echo "partial' + str(i) + ' ' + str(rank) + ' ' + str(energy) + ';" | pdsend 3005')
			print rank, energy
		time.sleep(0.1)

if __name__ == '__main__':
	main()
