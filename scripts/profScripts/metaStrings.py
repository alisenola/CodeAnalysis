#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#===================================================================================================
# This script examines the header lines of a file for specific strings and regular expressions
# E.g. author attribution, license information, copyright and autogeneration.
# For each copyright, license, generated text, gathers it to an outfile, typing the line
# The filename, and what kind of message appeared.
# Each line in the input csv corresponds to a regex
# Semicolons in the csv file break the regex up into location
# Does not support looking specifically at comment files
#===================================================================================================

#Created mshakir@keystonestrategy.com
#Modified ssia@keystonestrategy.com
#Last Modified 09/21/2016

import os
import sys
import csv

def metaStrings(dirpath,outFile,stringDic):

	#Test if binary file. If binary, leave: no strings
	textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
	is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))

	with open(outFile, 'w') as out:
		writer = csv.writer(out, delimiter= ";", quotechar = '|', lineterminator='\n')
		headerRow = ["filename"] + list(stringDic.keys())
		writer.writerow(headerRow)

		for root, dirs, files in os.walk(dirpath, topdown=False):
			for name in files:
				filename = os.path.join(root,name)
				outList = [filename]
				contentsList = [0]* len(stringDic)
				if (not is_binary_string(open(filename,'rb').read(1024))):
					for line in open(filename, encoding="utf8"):
						lineLower = line.lower()
						for i,key in enumerate(stringDic.keys()):
							for regex in stringDic[key]:
								if regex.lower() in lineLower:
									contentsList[i] = 1
				writer.writerow(outList+contentsList)

if __name__ == "__main__":
	metaStringsDir(".", "metaOut.txt")