#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#===================================================================================================
# This script checks if the diff method has a likelihood of mismatches
# It does so by doing a sort of all filenames, and for each filename
# Finding its match, and if there is match, bucketing it as either in the same dir
# Or in a different dir.
#===================================================================================================

#Created ssia@keystonestrategy.com
#Last Modified 09/15/2016

from os import walk
import pprint

def diffDiagnostic(dir1path,dir2path):
	dir1 = {}
	dir2 = {}

	#Create list of all files in Folder 1, and Folder 2
	#Push into folder 1 and folder 2 dictionary:
	#filename -> Dir (or dirs) #Dirs is extension
	for (dirpath, dirnames, filenames) in walk(dir1path):
	    for file in filenames:
	    	tailpath = dirpath.replace(dir1path,"")
	    	dir1[file] = tailpath
	for (dirpath, dirnames, filenames) in walk(dir2path):
	    for file in filenames:
	    	tailpath = dirpath.replace(dir2path,"")
	    	dir2[file] = tailpath

	#For each filename in 1, check filename in 2.
	dirMatch = 0
	fileMatch = 0
	noMatch = 0
	for key in dir1:
		if key in dir2:
			if dir1[key] == dir2[key]:
				dirMatch += 1
			else:
				fileMatch += 1
		else:
			noMatch += 1

	error = False
	if (noMatch > dirMatch+fileMatch):
		print("Caution: many files have no match")
		print("Analyzing", dir1path, "and", dir2path)
		print("Directory and File Matches: ", dirMatch)
		print("File name Matches: ", fileMatch)
		print("Files with no match: ", noMatch)
		error = True
	if (fileMatch * 4 > dirMatch):
		error = True
		print("Caution: significant filename matches without directory matches")
		print("Analyzing", dir1path, "and", dir2path)
		print("Directory and File Matches: ", dirMatch)
		print("File name Matches: ", fileMatch)
		print("Files with no match: ", noMatch)
	return error