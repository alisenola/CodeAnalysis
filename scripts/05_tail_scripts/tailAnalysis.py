#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#tail-analysis.py
#Tail Analysis Scripts
#Created: mshakir@keystonestrategy.com
#Updated: ssia@keystonestrategy.com
#Last Updated: 10/25/2016


from __future__ import print_function
from collections import defaultdict
import argparse
import time
import csv

from utilScripts.util import *

def is_pkg_deployed(package, year):
	if deployments:
		return (package, year) in deployments
	else:
		return True

def track_info(package, year, filename, status,info,rename_tracker):
	if (package, filename) in rename_tracker:
		filename = rename_tracker[(package, filename)]
	info[package][filename][year] = status

def track_existence(package, year, filename,info,rename_tracker):
	if (package, filename) in rename_tracker:
		filename = rename_tracker[(package, filename)]
	if year not in info[package][filename]:
		info[package][filename][year] = "N"

def track_rename(package, file1, file2,rename_tracker):
	if (package, file1) in rename_tracker:
		rename_tracker[(package, file2)] = rename_tracker[(package, file1)]
	else:
		rename_tracker[(package, file2)] = file1

def tailOutput(info,args):
	thirdparty  = set([r[0] for r in read_csv(args.thirdparty)])
	deployments = set([
		(package, int(year))
		for package,year,ndeployments,thirdparty in read_csv(args.deployments)
		if thirdparty == "0" and ndeployments != "0"
		]) if args.deployments else None

	stats = defaultdict(int)
	with open(args.output, "w") as out:
		f = csv.writer(out, delimiter="\t")
		f.writerow(["%02d" % year for year in range(args.ybase, args.ylast+1)] + 
			       ["is_deployed", "is_3rdparty", "package", "file"])
		for package in sorted(info.keys()):
			for filename in sorted(info[package].keys()):
				is_deployed = int(is_pkg_deployed(package, args.ybase) and is_pkg_deployed(package, args.ylast))
				is_3rdparty = int(package in thirdparty)
				f.writerow([info[package][filename][year] for year in range(args.ybase, args.ylast+1)] +
						   [is_deployed, is_3rdparty, package, filename])

				if info[package][filename][args.ylast] != "-" and info[package][filename][args.ybase] != "-" and \
				   is_deployed and not is_3rdparty:
					file_age = 0
					for year in range(args.ylast, args.ybase-1, -1):
						if info[package][filename][year] == "U":
							file_age += 1
						else:
							break
					stats[file_age] += 1

	with open(args.outstats, "w") as out:
		f = csv.writer(out, delimiter="\t")
		f.writerow(["age", "count"])
		for age in sorted(stats.keys()):
			f.writerow([age, stats[age]])

def genInfo(args):
	# This function will read the input CSV file and produce output in package-level chunks.
	# info = defaultdict(lambda: defaultdict(list))
	info = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: "-")))
	rename_tracker = {}

	f = read_csv(args.input, header_rows=1, delimiter="\t")
	for row in f:
		package, year1, year2, file1, file2, status, rename_flag, copy_flag, \
			S, F, A, D, MA, MD, RA, RD, CA, CD, path1, name1, ext1, path2, name2, ext2 = row

		if year1 == "0000":
			assert status == "A"
			assert file1 == ""
			track_info(package, year2, file2, "N",info,rename_tracker)
		else:
			if status == "U":
				assert file1 == file2
				track_existence(package, year1, file1,info,rename_tracker)
				track_info(package, year2, file1, "U",info,rename_tracker)
			elif status == "M":
				assert file1 == file2
				track_existence(package, year1, file1,info,rename_tracker)
				track_info(package, year2, file1, "M",info,rename_tracker)
			elif status == "D":
				assert file2 == ""
				track_existence(package, year1, file1,info,rename_tracker)
				track_info(package, year2, file1, "-",info,rename_tracker)
			elif status == "A":
				assert file1 == ""
				track_info(package, year2, file2, "N",info,rename_tracker)
			elif status == "R":
				assert file1 != file2
				track_rename(package, file1, file2,rename_tracker)
				track_existence(package, year1, file2,info,rename_tracker)
				track_info(package, year2, file2, "U",info,rename_tracker)
			elif status == "C":
				track_existence(package, year1, file1,info,rename_tracker)
				track_info(package, year2, file2, "N",info,rename_tracker)
			else:
				raise ValueError("Unknown status: " + status)

def tailAnalysis(args):
	start_time = time.time()
	print("Generating tail info from %s..." % args.input)
	info = genInfo(args)
	print("Writing tail info to %s..." % args.output)
	tailOutput(info,args)

	print("\n tailAnalysis done. Run time: %.3fs" % (time.time() - start_time))


if __name__ == "__main__":
	#===================================================================================================
	# Parse command-line parameters
	#===================================================================================================
	ap = argparse.ArgumentParser(description = "")
	ap.add_argument("--input", required=True, help="input data file")
	ap.add_argument("--output", required=True, help="output .csv file with raw input")
	ap.add_argument("--outstats", help=".xls file where the tail analysis report will be written")
	ap.add_argument("--deployments", required=False, help="file with deployed packages information")
	ap.add_argument("--thirdparty", required=True,  help="file with the list of third-party packages")
	ap.add_argument("--ybase", type=int, required=True, metavar="YEAR", help="start year")
	ap.add_argument("--ylast", type=int, required=True, metavar="YEAR", help="final year")

	args = ap.parse_args()
	tailAnalysis(args)