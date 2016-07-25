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
	freqtable = []

	for i in range(256): 
		freqtable.append(0)

	while(1):
		iter = ifile.read(1)
		if(not iter): break

		index = ord(iter[0])
		freqtable[index] = freqtable[index] + 1;

	ifile.close()
	freqtuples = []

	for i in range(256):
		freqtuples.append([freqtable[i],i])	

	freqtuples.sort(key=lambda x: x[1])

	dirtytree = (buildTree(freqtuples))

	tree = tuplesToBST(dirtytree)

	codes = dict()

	assignCodes(tree, codes)

	buf = ''
	ofile = open(outputpath, "wb")	
	ifile = open(inputpath, "r")

	while(1):
		iter = ifile.read(1)
		if(not iter):
			while(len(buf) < 8):
				buf = buf + "0"
			
		buf = buf + (encode(iter, codes))

		if(len(buf) >= 8):
			data = bytes([int(buf[:8], 2)]) # problem here? 8?
			ofile.write(data)
			buf = buf[8:]
		

		if(not iter):
			break

	tfile = open(outputpath+(".tree"), "w")
	tfile.write(str(freqtuples))
	print("^ Encoded string v Encoded, then decoded")
	print(decode(encode("Hello, world!", codes), tree))


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

def encode (s, codes) :
    output = ""
    for ch in s : 
    	output += codes[ord(ch)]
    	print((ord(ch)))
    return output

def decode (s, tree) :
    output = ""
    p = tree
    for bit in s :
        if bit == '0' : p = p[0]     # Head up the left branch
        else          : p = p[1]     # or up the right branch
        if type(p) == type(int(0)) :
            output += chr(p)              # found a character. Add to output
            p = tree                 # and restart for next character
    return output

def exit(status):
	print('usage: huffman.py -i <inputpath> -o <outputpath>')
	print('\nCompresses an input file using Huffman encoding.')
	sys.exit(status)

if __name__ == "__main__":
   main(sys.argv[1:])
