#!/usr/bin/env python

__author__ = "Frederick Brunn"
__copyright__ = "Copyright 2016"
__license__ = "GPL"
__version__ = "1.0.1"

import os, os.path
import sys
import getopt
import struct

def main(argv):
	inputpath = ''
	outputpath = ''
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
			inputpath = arg
		elif opt in ("-o", "--ofile"):
			outputpath = arg
		else:
			exit(2)

	if(inputpath == '' or 
		outputpath == '' or
		not (os.path.isfile(inputpath))): exit(2)

	ifile = open(inputpath, "r")
	ofile = open(outputpath, "w")

	freqtable = []

	for i in range(256): 
		freqtable.append(0)

	while(1):
		iter = ifile.read(1)
		if(not iter): break

		index = ord(iter[0])
		freqtable[index] = freqtable[index] + 1;

	freqtuples = []

	for i in range(256):
		freqtuples.append([freqtable[i],i])	

	freqtuples.sort(key=lambda x: x[1])

	dirtytree = (buildTree(freqtuples))

	print(str(dirtytree))

	tree = tuplesToBST(dirtytree)

	print(str(tree))

	codes = dict()

	assignCodes(tree, codes)

	print(codes)



def buildTree(tuples):
	while len(tuples) > 1 :
		leastTwo = tuple(tuples[0:2])                  # get the 2 to combine
		theRest  = tuples[2:]                          # all the others
		combFreq = leastTwo[0][0] + leastTwo[1][0]     # the branch points freq
		tuples   = theRest + [(combFreq,leastTwo)]     # add branch point to the end
		tuples.sort(key=lambda x: x[0])                                  # sort it into place
	return tuples[0]            # Return the single tree inside the list

def tuplesToBST (tree):
	p = tree[1] #only the byte
	if type(p) == type(int(0)) : return p #leaf
	else : return (tuplesToBST(p[0]), tuplesToBST(p[1]))

def assignCodes (node, codes, pat=''):
	if type(node) == type(int(0)):
		codes[(node)] = pat
	else: 
		assignCodes(node[0], codes, pat + "0")    # Branch point. Do the left branch
		assignCodes(node[1], codes, pat + "1")    # then do the right branch.

def exit(status):
	print('usage: huffman.py -i <inputpath> -o <outputpath>')
	print('\nCompresses an input file using Huffman encoding.')
	sys.exit(status)

if __name__ == "__main__":
   main(sys.argv[1:])
