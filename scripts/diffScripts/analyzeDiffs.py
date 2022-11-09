#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#===================================================================================================
# This script scans through all diff files produced by diffs-pipeline.py, and combines them into a
# single CSV file. This CSV file is arranged by package, and then by year-pair (only for those pairs
# for which differ was run). For each package-year-pair we list all files in both packages that were
# both modified and not modified.
#===================================================================================================

#Created mshakir@keystonestrategy.com
#Modified ssia@keystonestrategy.com
#Last Modified 08/16/2016

from __future__ import print_function
from collections import defaultdict
import os
import re
import csv
from utilScripts.util import *

#===================================================================================================
# Various helper functions
#===================================================================================================

# From filename, remove the directory name
def reduce_filename(filename,fromFolder,toFolder,inputFolder):
	ans = filename
	if filename != "" and filename != "/dev/null":
		exclude1 = "/".join([inputFolder, fromFolder])
		exclude2 = "/".join([inputFolder, toFolder])
		if (not exclude1 in filename and not exclude2 in filename):
			print(exclude1)
			print("Error", filename)
		ans = filename.replace(exclude1,"").replace(exclude2,"")
	return ans

# Parse a line from "--numstats" part of differ output
def parse_num_stats_line(line,fromFolder, toFolder, inputFolder, simple_files=True):
	row = line.rstrip().split("\t")
	lines_added   = check_int(row[0])
	lines_deleted = check_int(row[1])
	file1, file2  = split_files(row[2])
	if simple_files:
		file1 = reduce_filename(file1,fromFolder,toFolder, inputFolder)
		file2 = reduce_filename(file2,fromFolder,toFolder, inputFolder)
	return (lines_added, lines_deleted, file1, file2)

# Parse a line from "--raw" part of differ output
def parse_raw_line(line,fromFolder,toFolder,inputFolder):
	row = line[1:].rstrip().split("\t")
	row1 = row[0].split()
	status = row1[4]
	file1 = row[1]
	file2 = row[2] if len(row) == 3 else ""
	return (status, reduce_filename(file1,fromFolder,toFolder,inputFolder),
	 reduce_filename(file2,fromFolder,toFolder,inputFolder))


def all_packages(inputFolder):
	for pkg in sorted(next(os.walk(inputFolder))[1]):
		if pkg != ".empty":
			yield pkg

def diff_files_in_package(package,inputFolder):
	pkg_dir = os.path.join(inputFolder, package)
	for shortfile in sorted(next(os.walk(pkg_dir))[2]):
		mm = re.match(r"^([\w\-\.]+)--(.*)--(.*)\.txt$", shortfile)
		assert mm and mm.group(1) == package
		yield (os.path.join(pkg_dir, shortfile), mm.group(2), mm.group(3))



#===================================================================================================
# "Main" function
#===================================================================================================

def analyzeDiffs(output_file, threshold, versions,paths):

	headers = [ "fromVersion", "toVersion", "file1", "file2", "status", "rename_flag",
				"copy_flag", "S", "F", "A", "D", "MA", "MD", "RA", "RD", "CA", "CD"]
	diffDir = paths["diffout"]
	inputFolder = paths["inputFolder"]
	with open(output_file, "w") as csvfile:
		out = csv.writer(csvfile, delimiter=";", lineterminator='\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		out.writerow(headers)
		for package in all_packages(diffDir):

			# Intended structure for {info} dictionary:
			# info[year] = dictionary of {longfile: #lines} pairs,
			# where longfile is relative to the package.
			info = defaultdict(dict)
			used_versions = set()

			# 1. Read all diff files, and store their data in the {info} dictionary
			for diff_file, fromVersion, toVersion in diff_files_in_package(package,diffDir):
				for version in versions:
					if version["id"] == fromVersion:
						fromFolder = version["folder"]
					if version["id"] == toVersion:
						toFolder = version["folder"]
					if "0000" == fromVersion:
						fromFolder = "0000"

				with open(diff_file, "r") as input_file:
					
					# "null" diff mode -- just count all lines in all files
					if fromVersion == "0000":
						for line in input_file:
							if line[0] == ":": 
								status, _, _ = parse_raw_line(line,fromFolder,toFolder,inputFolder)
								assert status == "A"
							else:
								lines_added, lines_deleted, file1, file2 = \
								parse_num_stats_line(line, fromFolder, toFolder, inputFolder, simple_files=False)
								filename = reduce_filename(file2,fromFolder,toFolder,inputFolder)
								assert lines_deleted == "0" or lines_deleted == ""
								assert file1 == "/dev/null"
								info[toVersion][filename] = lines_added

					# "base" or "cont" diff mode
					else:
						used_versions.add(fromVersion)
						used_versions.add(toVersion)
						out_lines = []
						def record_added_file(file0):
							nlines = info[toVersion][file0]
							out_lines.append([
								fromVersion, toVersion, "", file0, "A", 0, 0, 
								0, nlines, nlines, 0, None, None, None, None, None, None
								])
						def record_deleted_file(file0):
							nlines = info[fromVersion][file0]
							out_lines.append([
								fromVersion, toVersion, file0, "", "D", 0, 0,
								nlines, 0, 0, nlines, None, None, None, None, None, None
								])
						def record_modified_file(file1, file2):
							added, deleted = numstats[(file1, file2)]
							lines1 = info[fromVersion][file1]
							lines2 = info[toVersion][file2]
							out_lines.append([
								fromVersion, toVersion, file1, file2, "M", 0, 0,
								lines1, lines2, None, None, added, deleted, None, None, None, None
								])
						def record_renamed_file(file1, file2):
							added, deleted = numstats[(file1, file2)]
							lines1 = info[fromVersion][file1]
							lines2 = info[toVersion][file2]
							out_lines.append([
								fromVersion, toVersion, file1, file2, "R", 1, 0,
								lines1, lines2, None, None, None, None, added, deleted, None, None
								])
						def record_copied_file(file1, file2):
							added, deleted = numstats[(file1, file2)]
							lines1 = info[fromVersion][file1]
							lines2 = info[toVersion][file2]
							out_lines.append([
								fromVersion, toVersion, file1, file2, "C", 0, 1,
								lines1, lines2, None, None, None, None, None, None, added, deleted
								])
						def record_unmodified_file(file0):
							nlines = info[toVersion][file0]
							out_lines.append([
								fromVersion, toVersion, file0, file0, "U", 0, 0, 
								nlines, nlines, None, None, None, None, None, None, None, None
								])


						numstats = {}
						raw_lines = []
						for line in input_file:
							if line[0] == ":":
								raw_lines.append(parse_raw_line(line,fromFolder,toFolder,inputFolder))
							else:
								lines_added, lines_deleted, file1, file2 = \
								parse_num_stats_line(line,fromFolder,toFolder,inputFolder)
								numstats[(file1, file2)] = (lines_added, lines_deleted)

						for status, file1, file2 in raw_lines:
							if status == "T":
								record_modified_file(file1, file1) #FIXME: Bug?
							elif status == "A":
								record_added_file(file1)
							elif status == "D":
								record_deleted_file(file1)
							elif status == "M":
								record_modified_file(file1, file1) #FIXME: Bug?
							elif status[0] == "R":
								similarity = int(status[1:])
								if similarity >= threshold:
									record_renamed_file(file1, file2)
								else:
									record_deleted_file(file1)
									record_added_file(file2)
							elif status[0] == "C":
								similarity = int(status[1:])
								if similarity >= threshold:
									record_copied_file(file1, file2)
								else:
									record_added_file(file2)
							else:
								print("Unknown status: ", status, file1, file2)

						# Add unmodified files
						for file1 in info[fromVersion]:
							if file1 in info[toVersion] and (file1, file1) not in numstats:
								record_unmodified_file(file1)

						# Write information into the output CSV file
						out.writerows(sorted(out_lines, key=lambda r: r[3]+r[4]))

			# 2. Account for files that have only null diffs
			for version in sorted(info.keys()):
				if version not in used_versions:
					for filename in sorted(info[version].keys()):
						nlines = info[version][filename]
						out.writerow([
							0, version, "", filename, "A", 0, 0, 
							0, nlines, nlines, 0, None, None, None, None, None, None
							])
