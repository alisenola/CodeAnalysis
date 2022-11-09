#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#===================================================================================================
# This script runs through all packages in all years, and performs {git diff}s for all relevant
# year pairs, as well as {git diff}s versus an empty folder
#===================================================================================================

#Created mshakir@keystonestrategy.com
#Modified ssia@keystonestrategy.com
#Last Modified: 08/16/2016

from __future__ import print_function
from collections import defaultdict
import os
import subprocess
import time
import sys
from pprint import pprint

# Git diff command to compare 2 packages
def git_diff_cmd(pkg1, pkg2):
	return "git diff --numstat --raw --no-index --ignore-all-space --ignore-blank-lines --ignore-space-change " \
		   "--find-renames=50%% --find-copies=50%% %s %s" % (pkg1, pkg2)

# Obtain unique file name where the report on run times should be stored. This function is run
# under race condition against other processes, and therefore must perform file-locking
# operation atomically.
def get_report_file_name(outputFolder):
	for i in range(1, 100):
		try_file = "%s/runtime-report-%02d.tsv" % (outputFolder, i)
		try:
			fd = os.open(try_file, os.O_CREAT | os.O_EXCL)
			os.close(fd)
			return try_file
		except OSError:
			continue

# Filter procedure that determines which packages should be processed by the current process.
# There are 2 steps: first, all packages are randomly split into {machine_n} parts, and current
# process only works with the {machine_m}-th part. Secondly, we also try to determine whether
# the given package was already claimed by a parallel process. If not, we claim the package for
# ourselves (by creating a corresponding directory).
def is_package_available(package,outputFolder,machine_m,machine_n):
	if hash(package) % machine_m == machine_n:
		try:
			os.makedirs(os.path.join(outputFolder, package), mode=0o777) 
			return True
		except:
			pass
	return False

#Adds a version Folder to each package it has
#packages are determined by what is available in first level os.walk
def add_to_pkg(comparison, package,inputFolder):
	versionFolder = comparison["fromFolder"]
	versionID = comparison["fromID"]
	fileDir = inputFolder + "/" + str(versionFolder)
	assert os.path.isdir(fileDir)
	for pkg in next(os.walk(fileDir))[1]:
		package[pkg].add((versionFolder,versionID)) 
	versionFolder = comparison["toFolder"]
	versionID = comparison["toID"]
	fileDir = inputFolder + "/" + str(versionFolder)
	assert os.path.isdir(fileDir)
	for pkg in next(os.walk(fileDir))[1]:
		package[pkg].add((versionFolder,versionID)) 

def gitDiffs(inputFolder, outputFolder, counter, comparisons):
	# Parse script parameters
	machine_n     = int(counter.split("/")[0]) - 1
	machine_m     = int(counter.split("/")[1])
	emptyFolder  = os.path.join(outputFolder, ".empty")
	print(emptyFolder)
	
	if not os.path.exists(emptyFolder):
	    os.makedirs(emptyFolder)

	assert os.path.isdir(inputFolder)
	assert os.path.isdir(outputFolder)
	assert os.path.isdir(emptyFolder)

	# 0. Start timer
	global_start_time = time.time()

	# 1. Generate list of which packages existed in which version
	print("Generating list of packages... ", end="")
	package_versions = defaultdict(set)

	for comparison in comparisons:
		add_to_pkg(comparison,package_versions,inputFolder)	
	print("ok.")

	print("Writing diff report... ")
	# 2. Run diff analysis for all packages; one package at a time
	print(outputFolder)
	print(get_report_file_name(outputFolder))
	with open(get_report_file_name(outputFolder), "w") as rtf:
		
		#For each package
		for package, versions in package_versions.items():
			if is_package_available(package,outputFolder,machine_m,machine_n):
				#For each version in the package
				for version in versions:
					versionFolder = version[0]
					versionID = version[1]
					print("\n%s %s... " % (versionID, package), end="")
					rtf.write("%s\t%s" % (versionID, package))
					sys.stdout.flush()

						
					out_dir  = os.path.join(outputFolder, package)
					origin_version = "0000"

					target_pkg = "/".join((inputFolder, versionFolder, package))
					origin_pkg = emptyFolder

					dt_start_time = time.time()
					out_file = package + "--" + origin_version + "--" + versionID + ".txt"
					print(out_dir,out_file)
					with open(os.path.join(out_dir, out_file), "w") as out:
						subprocess.call(git_diff_cmd(origin_pkg, target_pkg), stdout = out, shell=True)
					dt_time_taken = time.time() - dt_start_time
					rtf.write("\t%.6f" % dt_time_taken)
					print("%.3fs " % dt_time_taken, end="")

					for yversion in versions:
						if (yversion != version):
						
							target_pkg = "/".join((inputFolder, versionFolder, package))
							origin_pkg = "/".join((inputFolder, yversion[0], package))

							dt_start_time = time.time()
							out_file = package + "--" + yversion[1] + "--" + versionID + ".txt"
							with open(os.path.join(out_dir, out_file), "w") as out:
								subprocess.call(git_diff_cmd(origin_pkg, target_pkg), stdout = out, shell=True)
							dt_time_taken = time.time() - dt_start_time
							rtf.write("\t%.6f" % dt_time_taken)
							print("%.3fs " % dt_time_taken, end="")
						
						sys.stdout.flush()
					rtf.write("\n")
		print("Done.")
		print("Overall time taken = %.3fs" % (time.time() - global_start_time))
		print("Report written to " + rtf.name)
