
#rampDownCurve.py
#Generates relative contribution curves from diff output.
#Created: mshakir@keystonestrategy.com
#Updated: ssia@keystonestrategy.com
#Last Updated: 09/30/2016

#FIXME: This is an ugly piece of code and should definitely be refactored.
#...Eventually.

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import print_function
from collections import defaultdict
import argparse
import time
import csv
from utilScripts.util import *
from utilScripts.addMetadata import *
import os

GIT_START_FLAGS = 17

#===================================================================================================
# This is the "main" class which builds the dependency curve from a given input.
# Parameters are:
#	input - an iterator which generates triples of the form (curve-id, version, item). Here `curve-id`
#			is any identificator needed in case we're building several curves at the same time; and
#			`version` is version to which dependency `item` belongs.
#	filter - a function that looks at a triple returned by `input` and decides whether this triple
#			should be ignored or not. Function should return False for ignored triples.
#
#===================================================================================================
class RampDownCurve:
	def __init__(self, paths, auxpaths, comparison, params):
		self.inputFile = os.path.join(paths["diffout"],("diffs-%03d_augmented.csv" % int(50)))
		print("Building RC curve from: %s" % (self.inputFile))
		self.comparison = comparison
		self.paths = paths
		self.auxpaths = auxpaths
		self.use_deployments = auxpaths["deployments"]
		self.use_thirdparty = auxpaths["thirdparty"]
		self.use_tools = auxpaths["tools"]
		self.use_code = auxpaths["code"]
		self.data = defaultdict(lambda:defaultdict(int))
		self.params = params
		self.comp_pairs = set([(self.comparison["fromID"], self.comparison["toID"])])
		self.get_output()
		getattr(self,"differ_curve_builder")()

	#-------------------------------------------------------------------------------------------
	# Help functions to determine validity of a package.
	#-------------------------------------------------------------------------------------------
	def get_output(self):
		filename = ["RC"]
		for key in self.params:
			filename.append(key+str(self.params[key]))

		filename.append(self.comparison["fromID"])
		filename.append(self.comparison["toID"])
		filename.append(self.comparison["percentage"])
		filenameTxt = "-".join(filename)
		filenameTxt = filenameTxt + ".csv"
		self.output_file = filenameTxt

	#-----------------------------------------------------------------------------------------------
	# Build ramp_down curve for "differ" input
	#-----------------------------------------------------------------------------------------------
	def differ_curve_builder(self):
		self.vnames = ["S", "E", "L", "D", "N", "pkg:S", "pkg:E"]
		
		# This function will read the input CSV file and produce output in package-level chunks.
		def read_packages():
			totals = defaultdict(lambda:defaultdict(int))

			for rowNum,row in enumerate(read_csv(self.inputFile, delimiter=";", header_rows=0)):
				if (rowNum == 0):
					flagToCol = createFlagToCol(GIT_START_FLAGS, row)
					continue
				version1, version2, file1, file2, status, rename_flag, copy_flag, \
					S, F, A, D, MA, MD, RA, RD, CA, CD = row[:GIT_START_FLAGS]
				cf  = int(copy_flag)
				y1  = version1
				y2  = version2
				y12 = (y1, y2)

				if (flagFilter(self.params, flagToCol,row)):
					totals[y1][y12]  += add_up(S) * (1-cf)
					totals[y2][y12]  += add_up(F)
					totals["L"][y12] += add_up(F) - add_up(A, MA, RA, CA)
					totals["D"][y12] += add_up(D, MD, RD) # should be zero if cf == 1
					totals["N"][y12] += add_up(A, MA, RA, CA)

			yield totals

		for totals in read_packages():
			y1 = self.comparison["fromID"]
			y2 = self.comparison["toID"]
			y12 = (y1,y2)
			self.data[y12]["S"] += totals[y1][y12]
			self.data[y12]["E"] += totals[y2][y12]
			self.data[y12]["L"] += totals["L"][y12]
			self.data[y12]["D"] += totals["D"][y12]
			self.data[y12]["N"] += totals["N"][y12]

#===================================================================================================
# Produce output in the form of a .csv file
#===================================================================================================
def report_xls(paths, auxpaths, curve):
	output_file = paths["rampout"] + curve.output_file

	with open(output_file, 'wt') as csvfile:
		writer = csv.writer(csvfile, delimiter=';', lineterminator='\n')
		writer.writerow(["","Type:",curve.inputFile])
		writer.writerow(["","Parameters:"," ".join(curve.params)])
		for category, filepath in auxpaths.items():
			writer.writerow(["",category+" list:", filepath])

		writer.writerow([""])
		for report_type in ["base"]:
			writer.writerow(["fromPackage", "toPackage", "RampDown%"]+curve.vnames)
			outList= ["",""]
			fromID = curve.comparison["fromID"]
			toID = curve.comparison["toID"]
			if (fromID, toID) in curve.data:
				data = curve.data[(fromID, toID)]
				outList=[fromID,toID]
				if data["E"]:
					outList.append(float(data["L"])/float(data["E"]))
					print("Source LOC", int(data["S"]))
					print("Target LOC", int(data["E"]))
					print("Relative Contribution, %03f" % float(data["L"]/float(data["E"])))
				for i, vn in enumerate(curve.vnames):
					outList.append(data[vn])
			writer.writerow(outList)

	print("%s written." % output_file)


