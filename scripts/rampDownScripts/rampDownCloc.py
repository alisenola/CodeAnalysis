#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#rampDownCloc.py
#Generates relative contribution curves from cloc diff output.
#Created: ssia@keystonestrategy.com
#Last Updated: 10/25/2016

from __future__ import print_function
from collections import defaultdict
import csv
from utilScripts.util import *
from utilScripts.addMetadata import *
from operator import add

#==============================================================
# Given input file, print stuff
#==============================================================
CLOC_START_FLAGS = 14

def rampDownCloc(inputFile, flags, outPathID):
	#Old, new, overlap, percentage
	total = [0,0,0,0,0,0]
	code = [0,0,0,0,0,0]
	blank = [0,0,0,0,0,0]
	comm = [0,0,0,0,0,0]
	for i,row in enumerate(read_csv(inputFile, header_rows=0, delimiter=";")):
		if (i == 0):
			flagToCol = createFlagToCol(CLOC_START_FLAGS,row)
		else:
			if (flagFilter(flags,flagToCol,row)):
				filename, \
				blankSame, blankModded, blankAdded, blankRemoved, \
				commSame, commModded, commAdded, commRemoved, \
				codeSame, codeModded, codeAdded, codeRemoved, __UNUSED__ = row[0:CLOC_START_FLAGS]

				blankSame, blankModded, blankAdded, blankRemoved = int(blankSame), int(blankModded), int(blankAdded), int(blankRemoved)
				commSame, commModded, commAdded, commRemoved = int(commSame), int(commModded), int(commAdded), int(commRemoved)
				codeSame, codeModded, codeAdded, codeRemoved = int(codeSame), int(codeModded), int(codeAdded), int(codeRemoved)

				blank = [x + y for x, y in zip(blank, [ blankSame+blankModded+blankRemoved, blankSame+blankModded+blankAdded, blankSame,  blankModded, 0, 0])]
				comm = [x + y for x, y in zip(comm, [ commSame+commModded+commRemoved, commSame+commModded+commAdded, commSame, commModded, 0, 0])]
				code = [x + y for x, y in zip(code, [ codeSame+codeModded+codeRemoved, codeSame+codeModded+codeAdded, codeSame, codeModded, 0, 0])]

	for flag in flags:
		outPathID = outPathID + "_" + flag[0] + str(int(flag[1]))

	calcPercentage(blank, comm, code, total, outPathID+"_summary.csv")

def calcPercentage(blank, comm, code, total, outfile):
	with open(outfile, 'w') as out:
		writer = csv.writer(out, delimiter = ";", quotechar = '|', lineterminator='\n')
		blank[4] = 0 if blank[1] == 0 else float(blank[2]) / float(blank[1])
		comm[4] = 0 if comm[1] == 0 else float(comm[2]) / float(comm[1])
		code[4] = 0 if code[1] == 0 else float(code[2]) / float(code[1])
		blank[5] = 0 if blank[1] == 0 else float(blank[3]) / float(blank[1])
		comm[5] = 0 if comm[1] == 0 else float(comm[3]) / float(comm[1])
		code[5] = 0 if code[1] == 0 else float(code[3]) / float(code[1])

		total[0] = code[0] + comm[0] + blank[0]
		total[1] = code[1] + comm[1] + blank[1]
		total[2] = code[2] + comm[2] + blank[2]
		total[3] = code[3] + comm[3] + blank[3]
		total[4] = 0 if total[1] == 0 else float(total[2]) / float(total[1])
		total[5] = 0 if total[1] == 0 else float(total[3]) / float(total[1])

		printList = []
		printList.append(["Category", "Blanks", "Comments", "Code", "Total"])
		printList.append(["Source Lines", blank[0], comm[0], code[0], total[0]])
		printList.append(["Target Lines", blank[1], comm[1], code[1], total[1]])
		printList.append(["Overlap Lines", blank[2], comm[2], code[2], total[2]])
		printList.append(["Modded Lines", blank[3], comm[3], code[3], total[3]])
		printList.append(["Overlap Percentage", blank[4], comm[4], code[4], total[4]])
		printList.append(["Modded Percentage", blank[5], comm[5], code[5], total[5]])

		for row in printList:
			writer.writerow(row)

		print("Report written to: ", outfile)
		prettyPrint(printList)
		