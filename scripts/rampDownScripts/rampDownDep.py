#rampDownDep.py
# This script accepts stitch.csv files from each version
# Finds dependencies which are similar between each of them
# Outputs a list of dependencies for each version
# Outputs a rampdown for the specified comparisons

#Created: ssia@keystonestrategy.com
#Last Updated: 10/25/2016

import os

from utilScripts.util import read_csv
from utilScripts.addMetadata import *

STITCH_ENTROW = 0
STITCH_DEPROW = 10
DEP_START_FLAGS = 15
#Peel out initial 

#For a csvFile, returns a set of deduplicated dependencies
#Deletes Preamble to have comparative folder/file names
def getDepsFromStitch(inputFile, preamble, flags):
	depSet = set()

	for i,row in enumerate(read_csv(inputFile, header_rows=0, delimiter=";")):
		if (i == 0):
			flagToCol = createFlagToCol(DEP_START_FLAGS,row)
		else:
			entFile = row[STITCH_ENTROW]
			depFile = row[STITCH_DEPROW]

			if (entFile == depFile):
				continue
			if (entFile == "unknown" or depFile == "unknown"):
				continue

			#Continue if either fail the flag test
			if (flagFilter(flags, flagToCol, row)):

				#Horrible Hack Workaround for Github naming conventions in posix and nt
				preamble = preamble.replace("Github","GitHub")

				entFile = entFile.replace(preamble,"")
				depFile = depFile.replace(preamble,"")
				depSet.add((entFile,depFile))

	return depSet

def singleRampDown( outputpath, inputfolder, comparison, params, stitchAugment1, stitchAugment2 ):
	preamble1 = os.path.join( inputfolder, comparison["fromFolder"] )
	preamble2 = os.path.join( inputfolder, comparison["toFolder"] )

	preamble1 = os.path.abspath( preamble1 )
	preamble2 = os.path.abspath( preamble2 )
	depSet1 = getDepsFromStitch( stitchAugment1, preamble1, params )
	depSet2 = getDepsFromStitch( stitchAugment2, preamble2, params )
	outputfile = os.path.join( outputpath,
		comparison["fromID"] + "_" + comparison["toID"] + "_" + "depmatch.csv" )

	outputRows = []
	outputRows.append( ["Params: ", params] )
	outputRows.append( ["DepSet1 count: ", str(len(depSet1))] )
	outputRows.append( ["DepSet2 count: ", str(len(depSet2))] )
	outputRows.append( ["Overlap count: ", str(len(depSet1 & depSet2))] )

	print("Comparison of %s and %s:" % (comparison["fromID"], comparison["toID"]) )

	#Currently dependencies outputpath is not used. Write some code so that it is indeed used.

	for row in outputRows:
		print(row)

	with open(outputfile, 'w') as out:
		writer = csv.writer(out, delimiter = ";", quotechar = '|', lineterminator = '\n')
		for row in outputRows:
			writer.writerow( row )

	print("Output written to: ", outputfile)


#Calculate the set of deduplicated dependencies
#Calculate the overlap and print
def rampDownDep( outputpath, inputfolder, deppath, comparisons, params, auxpaths ):
	for comparison in comparisons:
		stitchAugment1 = os.path.join( deppath, comparison["fromID"] + "_stitch_augmented.csv")
		stitchAugment2 = os.path.join( deppath, comparison["toID"] + "_stitch_augmented.csv")

		stitchFile1 = os.path.join( deppath, comparison["fromID"] + "_stitch.csv")
		stitchFile2 = os.path.join( deppath, comparison["toID"] + "_stitch.csv")
		fileCols = [STITCH_ENTROW, STITCH_DEPROW]

		addMetadata( stitchFile1, stitchAugment1, auxpaths, fileCols )
		addMetadata( stitchFile2, stitchAugment2, auxpaths, fileCols )
		singleRampDown( outputpath, inputfolder, comparison, params, stitchAugment1, stitchAugment2 )

if __name__ == "__main__":
	print("Run This with the main flow.")
	