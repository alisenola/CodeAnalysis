#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#===================================================================================================
# This script holds DClocParams, which are the parameter class for Cloc diff
#===================================================================================================

#Created ssia@keystonestrategy.com
#Last Modified 10/28/2016

import os

class DClocParams:
	#Creates the strings and arguments required for the Cloc Diffs function
	def __init__(self, outputpath, inputfolder, langdef, comparison):
		self.dir1path = os.path.join( inputfolder, comparison["fromFolder"] )
		self.dir2path = os.path.join( inputfolder, comparison["toFolder"] )
		self.outPath = os.path.join( outputpath, comparison["fromID"]+ "_" + comparison["toID"] )
		self.diffAlign = "--diff-alignment=" + self.outPath +"_diff_alignment.txt"
		self.ignored="--ignored=" + self.outPath + "_ignored.txt"
		self.outfile="--out=" + self.outPath + "_report.csv"
		self.readDef="--read-lang-def=" + langdef