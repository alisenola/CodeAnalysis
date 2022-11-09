#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#summary.py
#Generates summaryScript
#Created: ssia@keystonestrategy.com
#Last Updated: 12/7/2016

from __future__ import print_function
import csv
from utilScripts.util import *
from utilScripts.addMetadata import *
from operator import add
from collections import OrderedDict
from collections import defaultdict

# Create big file
# For each analysis run, get the different datasets and put them into a single file
# An example would be file extensions.
# Let's start by creating a found, ignored, counted DONE
# Step two is getting 3 counts + total flag that represents the profile of each game
# Step three appending what its file extension is, what code it is
def createBigFile( inputfolder, versions ):
	categories = [ "engine", "tools" ]
	dates = [ 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]
	sortedVersions = generateSortedVersions( versions, categories, dates )
	dataheaders = ["category", "date", "Identifier", "fileType", "blank", "comment", "code", "found", "counted", "ignored", "whyIgnored" ]
	defaultHeaderList = ["added", "match", "removed", "exists", "ignored", "whyIgnored", 
			"blank == ", "blank != ", "blank + ", "blank - ",
			"comment == ", "comment != ", "comment + ", "comment - ",
			"code == ", "code != ", "code + ", "code - " ]

	for category in categories:
		dataheaders = ["category", "date", "Identifier", "fileType", "blank", "comment", "code", "found", "counted", "ignored", "whyIgnored" ]
		filename = category + "__summary.txt"

		for date in dates:
			identifier = sortedVersions[category][date]
			headerList = [ s + identifier for s in defaultHeaderList ]
			dataheaders = dataheaders + headerList

		with open(os.path.join(inputfolder, filename), 'a') as summaryFile:
			summaryFile.write( ';'.join(["filename"] + dataheaders) + '\n' )

		originFileDic = OrderedDefaultDict( lambda: OrderedDefaultDict( lambda: False ) )

		for (i,date) in enumerate(dates):	
			identifier = sortedVersions[category][date]
			headerList = [ s + identifier for s in defaultHeaderList ]
			#If origin dataset, we'll be going back to this often, so store it.
			if (i == 0):
				print("Taking ", identifier, "as the base version for code category:", category)
				originFileDic = getMetadata( category, date, sortedVersions, inputfolder, originFileDic )
			else:
				#Otherwise, start printing the summary and overwriting it.
				fileDic = OrderedDefaultDict( lambda: OrderedDefaultDict( lambda: False ) )
				originFileDic, fileDic = getDiffMetadata(category, date, dates, sortedVersions, inputfolder, headerList, originFileDic )
				fileDic = getMetadata( category, date, sortedVersions, inputfolder, fileDic )
				writeFileDic(inputfolder, dataheaders, fileDic, filename)
				#Print the fileDic, since it won't be affected

		#Print the originFileDic, once everything is done.
		writeFileDic( inputfolder, dataheaders, originFileDic, filename )

def writeFileDic(path, dataheaders, fileDic, filename):
	with open(os.path.join(path, filename), 'a') as summaryFile:
		for (file,metadata) in fileDic.items():
			dataList = []
			dataList.append(file)
			for header in dataheaders:
				dataList.append(str(metadata[header]))
			summaryFile.write(';'.join(dataList)+'\n')

def getDiffMetadata( key, date, dates, sortedVersions, inputfolder, headerList, originFileDic ):
	hl = headerList
	ignoredFile = os.path.join( inputfolder, sortedVersions[key][dates[0]] + "_" + sortedVersions[key][date] + "_ignored.txt")
	reportFile = os.path.join( inputfolder, sortedVersions[key][dates[0]] + "_" + sortedVersions[key][date] + "_report.csv")
	alignmentFile = os.path.join( inputfolder, sortedVersions[key][dates[0]] + "_" + sortedVersions[key][date] + "_diff_alignment.txt")
	fileDic = OrderedDefaultDict( lambda: OrderedDefaultDict( lambda: False ) )
	missfiles = []

	try:
		assert(os.path.exists(ignoredFile))
		assert(os.path.exists(reportFile))
		assert(os.path.exists(alignmentFile))
	except AssertionError:
		missfiles.append((key,date, ignoredFile))
		print(missfiles)
		return ( originFileDic, fileDic )

	#Add ignore location
	with open(ignoredFile) as ignoreFile:
		for line in ignoreFile:
			line = line.rstrip('\n')
			line = line.split(": ")
			#If in fileDic, set as fileDic, otherwise it's origin filedic
			if line[0] in originFileDic:
				metadata = originFileDic[line[0]]
			else:
				metadata = fileDic[line[0]]
			metadata[hl[4]] = True
			metadata["category"] = key
			if "zero sized file" in line[1]:
				metadata[hl[5]] = "ZeroSized"
			elif "language unknown" in line[1]:
				metadata[hl[5]] = "LangUnknown"
			elif "exceeds max" in line[1]:
				metadata[hl[5]] = "MaxSize"
			elif "listed in" in line[1]:
				metadata[hl[5]] = "NotCodeExt"
			elif "temporary" in line[1]:
				metadata[hl[5]] = "TempFile"
			elif "--exclude-dir=.git" in line[1] or "--exclude-dir=.svn" in line[1]:
				metadata[hl[5]] = "git/svnFile"
			else:
				print("Error it is unknown why file", line[0], "was excluded")

	with open(alignmentFile) as alignFile:
		for line in alignFile:
			line = line.rstrip('\n')
			metadata["category"] = key
			#Added: It's current dic info
			if "  + " in line:
				line = line.replace("  + ", "")
				line = line.split(" ; ")
				fileDic[line[0]][hl[0]] = True
				fileDic[line[0]]["Identifier"] = sortedVersions[key][date]
				fileDic[line[0]]["date"] = date
			#Subtracted: It's origin data information
			elif "  - " in line:
				line = line.replace("  - ", "")
				line = line.split(" ; ")
				originFileDic[line[0]][hl[2]] = True
				originFileDic[line[0]]["Identifier"] = sortedVersions[key][dates[0]]
				originFileDic[line[0]]["date"] = dates[0]
			#Modified: It's origin data information
			elif "  != " in line or "  == " in line:
				line = line.replace("  != ", "")
				line = line.replace("  == ", "")
				line = line.split(" | ")
				originFileDic[line[0]]["Identifier"] = sortedVersions[key][dates[0]]
				originFileDic[line[0]]["date"] = dates
				originFileDic[line[0]][hl[3]] = True
				originFileDic[line[0]][hl[1]] = line[1].split( " ; " )[0]

	headerList = hl[ 6: ]

	with open(reportFile) as rpFile:
		next(rpFile)
		for line in rpFile:
			line = line.rstrip('\n')
			line = line.split("; ")
			originFileDic[line[0]]["category"] = key
			for (i,header) in enumerate(headerList):
				originFileDic[line[0]][header] = line[i+1]

	return ( originFileDic, fileDic )

def getMetadata( key, date, sortedVersions, inputfolder, fileDic):
	ignoredFile = os.path.join( inputfolder, sortedVersions[key][date] + "_ignored.txt")
	countedFile = os.path.join( inputfolder, sortedVersions[key][date] + "_counted.txt")
	foundFile = os.path.join( inputfolder, sortedVersions[key][date] + "_found.txt")
	reportFile = os.path.join( inputfolder, sortedVersions[key][date] + "_report.csv")
	#Add counted location

	missfiles = []

	try:
		assert(os.path.exists(countedFile))
		assert(os.path.exists(ignoredFile))
		assert(os.path.exists(foundFile))
		assert(os.path.exists(reportFile))
	except AssertionError:
		missfiles.append((key,date, countedFile))
		print(missfiles)
		return fileDic

	with open(countedFile) as countFile:
		for line in countFile:
			line = line.rstrip('\n')
			fileDic[line]["counted"] = True
			fileDic[line]["category"] = key
			fileDic[line]["Identifier"] = sortedVersions[key][date]
			fileDic[line]["date"] = date

	#Add ignore location
	with open(ignoredFile) as ignoreFile:
		for line in ignoreFile:
			line = line.rstrip('\n')
			line = line.split(": ")
			fileDic[line[0]]["ignored"] = True
			fileDic[line[0]]["category"] = key
			fileDic[line[0]]["Identifier"] = sortedVersions[key][date]
			fileDic[line[0]]["date"] = date
			if "zero sized file" in line[1]:
				fileDic[line[0]]["whyIgnored"] = "ZeroSized"
			elif "language unknown" in line[1]:
				fileDic[line[0]]["whyIgnored"] = "LangUnknown"
			elif "exceeds max" in line[1]:
				fileDic[line[0]]["whyIgnored"] = "MaxSize"
			elif "listed in" in line[1]:
				fileDic[line[0]]["whyIgnored"] = "NotCodeExt"
			elif "temporary" in line[1]:
				fileDic[line[0]]["whyIgnored"] = "TempFile"
			elif "--exclude-dir=.git" in line[1] or "--exclude-dir=.svn" in line[1]:
				fileDic[line[0]]["whyIgnored"] = "git/svnFile"
			else:
				print("Error it is unknown why file", line[0], "was excluded")

	#Add foundFile
	with open(foundFile) as findFile:
		for line in findFile:
			line = line.rstrip('\n')
			fileDic[line]["found"] = True
			fileDic[line]["category"] = key
			fileDic[line]["Identifier"] = sortedVersions[key][date]
			fileDic[line]["date"] = date

	with open(reportFile) as reportData:
		next(reportData)
		for line in reportData:
			line = line.rstrip('\n')
			line = line.split(";")
			filename = fileDic[line[1]]
			filename["category"] = key
			filename["Identifier"] = sortedVersions[key][date]
			filename["date"] = date
			filename["fileType"] = line[0]
			filename["blank"] = line[2]
			filename["comment"] = line[3]
			filename["code"] = line[4]

	return fileDic

class OrderedDefaultDict(OrderedDict):
    # Source: http://stackoverflow.com/a/6190500/562769
    def __init__(self, default_factory=None, *a, **kw):
        if (default_factory is not None and
           not isinstance(default_factory, Callable)):
            raise TypeError('first argument must be callable')
        OrderedDict.__init__(self, *a, **kw)
        self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = self.default_factory,
        return type(self), args, None, None, self.items()

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo):
        import copy
        return type(self)(self.default_factory,
                          copy.deepcopy(self.items()))

    def __repr__(self):
        return 'OrderedDefaultDict(%s, %s)' % (self.default_factory,
                                               OrderedDict.__repr__(self))

#For each version, get summary statistics.
#We start by getting the LOC_found total.
#We continue with LOC of everythin
#This is sorted by category.
def getSummary( outputfolder, inputfolder, versions, task ):

	categories = [ "engine", "tools", "game" ]
	dates = [ 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015 ]
	sortedVersions = generateSortedVersions( versions, categories, dates )

	print( "\nConstructing Basic Profile of analyzed counts:" )
	missfiles = []
	summaryList = []
	
	#task["rowOfInterest"] could be Percentage, Source Lines, Target Lines, Overlap Lines
	rowOfInterest = task["rowOfInterest"]

	#Not looking through summary, but going down to the file level instead.
	granularity = task["granularity"]

	#Sorting style, by extensions, by code, by everything using a bunch of flags.
	extensions = task["extensions"]

	for key in sortedVersions:
		tempMatrix = []
		tempMatrix.append(["Date", "FileName", "Blanks", "Comments", "Code", "Total"])
		for (i,date) in enumerate(dates):
			if task["style"] == "diff" and i == 0:
				continue

			if task["style"] == "diff":
				filepath = os.path.join(outputfolder, sortedVersions[key][dates[0]] +"_"+ sortedVersions[key][date] + "_summary.csv")
			elif task["style"] == "prof":
				filepath = os.path.join(inputfolder, sortedVersions[key][date] + "_summary.csv")

			try:
				foundRow = False
				assert(os.path.exists(filepath))
				rows = read_csv(filepath, delimiter=";")
				for row in rows:
					if row[0] == rowOfInterest:
						if task["style"] == "diff":
							row[1] = "{:.2%}".format(float(row[1]) )
							row[2] = "{:.2%}".format(float(row[2]) )
							row[3] = "{:.2%}".format(float(row[3]) )
							row[4] = "{:.2%}".format(float(row[4]) )
							tlist = [ str(date), sortedVersions[key][date], row[1], row[2], row[3], row[4]]
						elif task["style"] == "prof":
							tlist = [ str(date), sortedVersions[key][date], row[1], row[2], row[3],
								int(row[1])+int(row[2])+int(row[3])]
						tempMatrix.append(tlist)
						foundRow = True
				assert(foundRow)
			except AssertionError:
				tlist = [ str(date), "Not_found", "N/A","N/A","N/A","N/A" ]
				tempMatrix.append(tlist)
				missfiles.append((key,date, filepath))

		rotatedMatrix = list(zip(*tempMatrix))

		summaryList.append(rotatedMatrix)

	#missPrint(missfiles)
	return ( categories, summaryList )