#!/usr/bin/env python

__author__ = "Frederick Brunn"
__copyright__ = "Copyright 2016"
__license__ = "GPL"
__version__ = "1.0.1"

import os
import sys
import getopt

def main(argv):
	inputfile = ''
	outputfile = ''
	verbose = 0;
	if(len(argv) < 1):
		exit(2)
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		exit(2)
	for opt, arg in opts:
		if opt == '-h' or arg[0] == '-':
			exit(0)
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		else:
			exit(2)

	if(inputfile == '' or outputfile == ''): exit(2)

	print('Input file is "', inputfile)
	print('Output file is "', outputfile)

def exit(status):
	print('usage: huffman.py -i <inputfile> -o <outputfile>')
	print('\nCompresses an input file using Huffman encoding.')
	sys.exit(status)


if __name__ == "__main__":
   main(sys.argv[1:])
