#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#addMetadata.py
#Takes a CSV file and a set of lists
#From each list, adds an additional column to the cloc diff csv output
#Marking them with a 1 or 0 as appropriate.
#Created: ssia@keystonestrategy.com
#Last Updated: 10/25/2016

from utilScripts.util import *
import csv
import collections

#Takes a cloc diff CSV out file and a set of lists
#From each list, adds an additional column to the cloc diff csv output
#Marks each file with a 1 or 0, spits augmented into outfile
#fileCols tells us how many files (usually 1 or 2), and which col
#The data is in.
def addMetadata(inFile,outFile,listOfListPaths,fileCols,start=0):
  with open(outFile, 'w') as out:
    writer = csv.writer(out, delimiter = ";", quotechar = '|', lineterminator='\n')
    for i,row in enumerate(read_csv(inFile, header_rows=0, delimiter=";")):
      if i == 0:
        for f in fileCols:
          for key in listOfListPaths:
            row.append(key)
        writer.writerow(row)
      else:
        for f in fileCols:
          while len(row) < start:
            row.append("")
          for key in listOfListPaths:
            filePath = row[f]
            listPaths = listOfListPaths[key]
            tag = toTag(filePath,listPaths)
            row.append(tag)
        writer.writerow(row)

#Given a filepathname, and a list of paths
#Returns 1 if filepathname contains one
#Or more of the listed paths.
def toTag(filePath,listPaths):
  for path in listPaths:
    if path in filePath:
      return 1
  return 0

#Given an index for when the flags begin
#And the headerRow of the csv file
#Outputs an index corresponding to each flag.
def createFlagToCol( flagStartCol, headerRow ):
  flagToCol = collections.defaultdict(set)
  for j in range(flagStartCol,len(headerRow)):
    flagToCol[headerRow[j]].add(j)
  return flagToCol

#Given a list of flags, and where the flags are and a row,
#Determines if the file should be included in the analysis.
def flagFilter( flags, flagToCol, row ):
  if len(flags) == 0:
    return True
  else:
    for flag in flags:
      include = flag[1]
      listColNum = flagToCol[flag[0]]
      for colNum in listColNum:
        if(int(row[colNum]) != int(include) ):
          return False
    return True

#given a list of listpath CSV filess, read in the CSVs 
#outputs a list of listpaths.
#Marked for removal and pushing into the readJson chart.
def expandListPaths(listOfListPaths):
  for key in listOfListPaths:
    listPaths = []
    filename = listOfListPaths[key]
    for row in read_csv(filename):
      if (len(row) == 1):
        listPaths.extend(row)
      elif (len(row) > 1):
        print("Row ignored: ")
        print(row)
    listOfListPaths[key] = listPaths
  return listOfListPaths

if __name__ == "__main__":
  listOfListPaths = {}
  listOfListPaths["tools"] = "../auxiliary_datasets/test.csv"
  listOfListPaths["libraries"] = "../auxiliary_datasets/libraries.csv"
  addMetadata("../output_datasets/03_profiler/Testv5_Testv6_report.csv",
    "../output_datasets/03_profiler/Testv5_Testv6_report_augmented.csv",listOfListPaths)
