#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#===================================================================================================
# This script calculates the sum of information for python based on whatever flags might be in place.
# For each comparison flag, parameterizes the data.
# Provides a dataset breakdown based on Programming Language, and then finally a total.
#===================================================================================================

#Created ssia@keystonestrategy.com
#Last Modified 10/28/2016

from utilScripts.util import read_csv
from collections import defaultdict
from utilScripts.addMetadata import *

PROF_START_FLAGS = 6
PROF_LANG_ROW = 0


#Given a version ID and a version folder,
#Given an input folder to look into, and an output folder to spit output
#Given a language definition,
#Does a line count profiling and outputs that into the output folder
class PClocParams:
	def __init__(self, outputpath, inputfolder, langdef, version):
		pathID = os.path.join( outputpath, version["id"] )

		self.found = "--found=" + pathID +"_found.txt"
		self.ignored="--ignored=" + pathID + "_ignored.txt"
		self.counted="--counted=" + pathID+"_counted.txt"
		self.readDef="--read-lang-def=" + langdef
		self.filesize="--max-file-size=10"
		self.outfile="--out=" + pathID + "_report.csv"
		self.inFolder = os.path.join( inputfolder, version["folder"] )
		self.rpFile = pathID + "_report.csv"
		self.rpaugFile = pathID + "_report_augmented.csv"

def sumProfiler( comparison, params, outputpath ):
	pathID = os.path.join( outputpath, comparison["fromID"] )
	outPathID = os.path.join( outputpath, comparison["fromID"] )
	augFile = pathID + "_report_augmented.csv"
	print("Profiling from %s", augFile)
	print("Params:", params)
	sumProfile(augFile,params,outPathID)
	if (not comparison["toID"] == comparison["fromID"] ):
		pathID = os.path.join( outputpath, comparison["toID"] )
		outPathID = os.path.join( outputpath, comparison["toID"] )
		augFile = pathID + "_report_augmented.csv"
		print("Profiling from %s", augFile)
		print("Params:", params)
		sumProfile(augFile,params,outPathID)


def sumProfile( inputFile, flags, outPathID ):
	#dictionary of languages
	dicLang = defaultdict(lambda: [0,0,0] )
	for i,row in enumerate(read_csv(inputFile, header_rows=0, delimiter=";")):
		if (i == 0):
			flagToCol = createFlagToCol(PROF_START_FLAGS,row)
		else:
			if (flagFilter(flags,flagToCol,row)):
				lang = row[PROF_LANG_ROW]
				dicLang[lang] = [x + y for x, y in zip(dicLang[lang], list(map(int, row[2:5])))]
	for flag in flags:
		outPathID = outPathID + "_" + flag[0] + str(int(flag[1]))
	calcSum(dicLang,outPathID+"_summary.csv")

def calcSum(dicLang,outfile):
	with open(outfile, 'w') as out:
		writer = csv.writer(out, delimiter = ";", quotechar = '|', lineterminator='\n')
		print("Language, Blanks, Comments, Code")
		writer.writerow(["Language", "Blanks", "Comments", "Code"])
		totalSum = [0,0,0]
		for key in dicLang:
			print(key, dicLang[key])
			writer.writerow([key, dicLang[key][0], dicLang[key][1], dicLang[key][2]])
			totalSum = [x + y for x, y in zip(dicLang[key], totalSum)]

		print("Total", totalSum, "\n")
		writer.writerow(["Total", totalSum[0], totalSum[1], totalSum[2]])