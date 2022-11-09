#runSuite.py
#Created 08/23/2016
#ssia@keystonestrategy.com

#Takes in listOfVersions.json, and performs some diffs and stat counting
#Takes in listOfComparisons.json, calls a set of comparisons on the specified 1:1 comparisons
#calls rampDownCurve.py, analyzeDiffs.py and runDiffer.py

# Input: listOfVersions.json, listOfComparisons.json
# Output:
#  basic stats of each directory based on list of versions
#  multiple ramp-down-curve.py in excel format based on list of comparisons
#  diff'ed directories based on list of comparisons
#  analyzed diffs based on list of comparisons  

import atexit
import time
import argparse
import os
import io
import signal
import subprocess
import sys
import json
from collections import OrderedDict
from collections import defaultdict
from sys import platform as _platform
from utilScripts.util import *
from utilScripts.addMetadata import *
from summaryScripts.summary import *
from utilScripts.CKProject import CKProject
from utilScripts.staticvars import *




procs = []

#All the subprocess is terminated, when main.py is terminated.
def cleanSubProcess():
  for proc in procs:
    if proc.poll() == None:
      proc.kill()
      print("%s has been force terminated" % str(proc))

#This is called before scripts exit normally
def exit_handler():
  cleanSubProcess()

#This is called before scripts exit force
def sigint_handler(signum, frame):
  if input("\nReally quit? (y/n)> ").lower().startswith("y"):
    cleanSubProcess()
    sys.exit(1)

atexit.register(exit_handler)
signal.signal(signal.SIGINT, sigint_handler)

#Giant switch statement, given whatever tasks are currently being activated,
#runs specific functions.
def runTasks(ck_project):
  tasks = ck_project.Comparisons.tasks
  versions = ck_project.versions
  comparisons = ck_project.Comparisons.comparisons
  parameters = ck_project.Comparisons.parameters
  paths = ck_project.Comparisons.paths
  auxpaths = ck_project.Comparisons.auxpaths
  compVersions = ck_project.compVersions
  inputfolder = paths["inputFolder"]
  #Based on read of JSON, determines which task to run and with which parameters
  for task in tasks:
    if "run" not in task or task["run"] == "True" or RUNALL == True:
      print( "Running task name:", task["type"], "...", end = "" )

      #Profiling tasks, line and word counts and then metaprofiling for strings
      if (task["type"]) == "Profiler":
        profileTask( ck_project )
      elif (task["type"]) == "MetaProfiler":
        metaTask( ck_project.OutputFolders.profout, inputfolder, paths["strings"], compVersions )

      #Cloc Diffs from diagnosis to running to RampDown
      elif (task["type"]) == "DiagnoseDiffs":
        diagnoseTask( inputfolder, comparisons )
      elif (task["type"]) == "ClocDiffs":
        clocDiffsTask( ck_project.OutputFolders.diffout, inputfolder, paths["cloc"], paths["langDef"], comparisons )
      elif (task["type"]) == "RampDownCloc":
        rampClocTask( ck_project.OutputFolders.rampout, ck_project.OutputFolders.diffout, auxpaths, comparisons, parameters )

      #Udb from Generating UDB to generating dependencies to RampDown
      elif (task["type"]) == "GenUdb":
        genUDBTask( ck_project.OutputFolders.depout, inputfolder, paths["undpath"], task, compVersions)
      elif (task["type"]) == "GenDeps":
        genDepsTask( ck_project.OutputFolders.depout, inputfolder, paths["undpath"], compVersions)
      elif (task["type"]) == "RampDownDeps":
        rampDepTask( ck_project.OutputFolders.rampout, inputfolder, ck_project.OutputFolders.depout, 
          comparisons, parameters, auxpaths )

      #Visualizations and summary information
      elif (task["type"]) == "Viz":
        vizTask( ck_project.OutputFolders.vizout, ck_project.OutputFolders.diffout, comparisons )
      elif (task["type"]) == "Summary":
        getSummary(ck_project.OutputFolders.rampout, ck_project.OutputFolders.profout, versions, task)
      elif (task["type"]) == "CreateBigFile":
        createBigFile( ck_project.OutputFolders.profout, versions )

      #Git Diff from diff to analysis to rampdown. We are phasing this out.
      elif (task["type"]) == "GitDiffs":
        gitDiffsTask( ck_project.OutputFolders.diffout, inputfolder, comparisons )
      elif (task["type"]) == "AnalyzeGitDiffs":
        analyzeGitDiffsTask(paths,auxpaths,task,compVersions)      
      elif (task["type"]) == "RampDownGit":
        rampGitTask(paths,auxpaths,comparisons)

      else:
        print("Unknown task type: %s" % task["type"])

def profileTask(CKProject):
  from utilScripts.addMetadata import addMetadata
  from profScripts.profiler import PClocParams
  from profScripts.profiler import sumProfiler

  checkCreate(CKProject.OutputFolders.profout, "Profiler")
  print("Starting profiling task...")

  for version in CKProject.compVersions:
    cp = PClocParams( CKProject.OutputFolders.profout, CKProject.Comparisons.paths["inputFolder"], CKProject.Comparisons.paths["langDef"], version )
    process = subprocess.Popen([CKProject.Comparisons.paths["cloc"],
      "--skip-uniqueness",
      "--by-file",
      cp.found,
      cp.ignored,
      cp.counted,
      cp.readDef,
      cp.filesize,
      "--csv-delimiter=;",
      cp.outfile,
      cp.inFolder
    ])
    process.wait()
    procs.append(process)

    addMetadata(cp.rpFile, cp.rpaugFile, CKProject.Comparisons.auxpaths, [1], PROF_START_FLAGS)

  for comparison in CKProject.Comparisons.comparisons:
    sumProfiler(comparison, CKProject.Comparisons.parameters, CKProject.OutputFolders.profout)

def metaTask(outputpath, inputfolder, metastringspath, compVersions):
  from profScripts.metaStrings import metaStrings

  checkCreate(outputpath, "Profiler")

  try:
    with open( metastringspath ) as data_file:
      version_data = json.load(data_file)
    stringDic = OrderedDict(version_data["stringDic"])
  except FileNotFoundError:
    print("Strings File Does not yet exist. Unable to create...")
    exit()

  for version in compVersions:
    outfile = os.path.join(outputpath, version["id"]) + "_metaData.txt"
    codefolder = os.path.join(inputfolder, version["folder"])
    metaStrings(codefolder, outfile, stringDic)

  print("Metaprofiling complete")

def diagnoseTask(inputfolder, comparisons):
  from diffScripts.diffDiagnostic import diffDiagnostic
  print("Checking diff miss likelihood... ", end = "")
  error = False
  for comparison in comparisons:
    dir1path = os.path.join( inputfolder, comparison["fromFolder"] )
    dir2path = os.path.join( inputfolder, comparison["toFolder"] )
    assert(os.path.exists(dir1path))
    assert(os.path.exists(dir2path))
    if (diffDiagnostic(dir1path, dir2path)):
      error = True
  if (error == False):
    print("Ok. No significant issues.")

def clocDiffsTask(outputpath, inputfolder, clocpath, langdef, comparisons):
  from diffScripts.DClocParams import DClocParams
  checkCreate(outputpath, "Profiler")
  if (os.name == "posix"):
    clocpath = "cloc"
  else:
    assert(os.path.exists(clocpath))
  for comparison in comparisons:
    cp = DClocParams(outputpath, inputfolder, langdef, comparison)
    print(cp.dir1path, cp.dir2path)
    process = subprocess.Popen([
      clocpath,
      cp.diffAlign,
      "--max-file-size=10",
      "--skip-uniqueness",
      "--by-file-by-lang",
      cp.ignored,
      cp.readDef,
      "--csv",
      "--csv-delimiter=;",
      cp.outfile,
      cp.dir1path,
      cp.dir2path])
    process.wait()
    procs.append(process)
    print("Report written to: ", cp.outfile)

def rampClocTask(outputpath, inputfolder, auxpaths, comparisons, parameters):
  from rampDownScripts.rampDownCloc import rampDownCloc
  from utilScripts.addMetadata import addMetadata

  checkCreate(outputpath, "Ramp")

  for parameter in parameters:
    if parameter[0] not in auxpaths:
      print("Warning: ", parameter[0],
        "not in auxpaths. To have it as a parameter, define a csv file and add it to the comparisons.json auxpaths list")

  for comparison in comparisons:
    pathID = os.path.join(inputfolder, comparison["fromID"]+ "_" + comparison["toID"])
    inFile = pathID + "_report.csv"
    augFile = pathID + "_report_augmented.csv"
    try:
      assert(os.path.exists(inFile))
    except AssertionError:
      print("Fatal:", inFile, "does not exist. Make sure you have run the cloc diffs task for \
         all comparisons you are trying to make ramp down curves for.")
      exit()

    outPathID = os.path.join(outputpath, comparison["fromID"]+ "_" + comparison["toID"])
    addMetadata(inFile, augFile, auxpaths, [0])
    rampDownCloc(augFile, parameters, outPathID)


def genUDBTask(outputpath, inputfolder, undpath, task, compVersions):
  print("Generating Udb... ", end="")
  lang = task["lang"]
  depout = outputpath
  checkCreate(outputpath, "Dependency")
  for version in compVersions:
    vid = version["id"]
    logFN = vid + "_log.txt"
    udbFN = vid + ".udb"
    codefolder = os.path.join(inputfolder, version["folder"])
    udblog = os.path.join(depout, logFN)
    udbpath = os.path.join(depout, udbFN)
    cmd = [undpath, "create", "-languages", lang, "-db", udbpath]
    process = subprocess.Popen(cmd)
    process.wait()
    procs.append(process)
    cmd = [undpath, "add", "-db", udbpath, "-watch", "off", codefolder]
    process = subprocess.Popen(cmd)
    process.wait()
    procs.append(process)
    cmd = [undpath, "analyze", "-all","-db", udbpath]
    process = subprocess.Popen(cmd)
    process.wait()
    procs.append(process)

  print("ok.")

def genDepsTask(outputpath, inputfolder, undpath, compVersions):
  #checkUnderstandPath(undpath)
  from depScripts.genCPPdep import genCPPDep
  from depScripts.genCPPdep import genCPPEnt
  from depScripts.stitchCsv import stitchCsv
  from depScripts.csv2sql import csv2sql
  from depScripts.sql2json import sql2json
  from depScripts.pagerank import pagerank
  print("Generating Dependencies... ", end="")

  for version in compVersions:
    udbpath = os.path.join(outputpath, version["id"] + ".udb")
    depcsv = os.path.join( outputpath, version["id"] + "_dep.csv")
    entcsv = os.path.join( outputpath, version["id"] + "_ent.csv")
    stitchcsv = os.path.join( outputpath, version["id"] + "_stitch.csv")
    outcsv = os.path.join( outputpath,  version["id"] + "_pagerank.csv")
    dbfile = os.path.join( outputpath, version["id"])
    matrixJson = ("%s_%s.json") % (version["id"], "all")
    matrixJson = os.path.join(outputpath,  matrixJson)
    genCPPDep(udbpath, depcsv)
    genCPPEnt(udbpath, entcsv)
    stitchCsv(depcsv, entcsv, stitchcsv)
    csv2sql(stitchcsv, version["id"], dbfile)
    sql2json(matrixJson, inputfolder, version, dbfile)
    pagerank(matrixJson, outcsv)

def rampDepTask(outputpath, inputfolder, deppath, comparisons, params, auxpaths):
  from rampDownScripts.rampDownDep import rampDownDep
  checkCreate(outputpath, "Ramp")
  rampDownDep(outputpath, inputfolder, deppath, comparisons, params, auxpaths)


def gitDiffsTask(outputpath, inputfolder, comparisons):
  from diffScripts.gitDiffs import gitDiffs
  checkCreate(outputpath, "Diff")
  createDiffs(inputfolder, outputpath, "1/1", comparisons)

def analyzeGitDiffsTask(paths, auxpaths, task, comparisons):
  from diffScripts.analyzeDiffs import analyzeDiffs
  for n in task["thresholds"]:
    print("Processing diffs for %d%% threshold..." % n)

    output_file = os.path.join(paths["diffout"],("diffs-%03d.csv" % n))
    analyzeDiffs(output_file, n, comparisons,paths)

    print("File %s written.\n" % output_file)

  for comparison in comparisons:
    pathID = paths["diffout"]
    inFile = pathID + "diffs-050.csv"
    augFile = pathID + "diffs-050_augmented.csv"
    addMetadata(inFile,augFile, auxpaths,[2,3])

def rampGitTask(paths, auxpaths, comparisons):
  from rampDownScripts.rampDownCurve import report_xls
  from rampDownScripts.rampDownCurve import RampDownCurve
  checkCreate(paths["rampout"], "Ramp")
  #Spawn new curve for each comparison and param category,
  for comparison in comparisons:
    if len(comparison["params"]) == 0:
      params = {}
      report_xls(paths, auxpaths,RampDownCurve(paths, auxpaths, comparison, params))
    else:
      for params in comparison["params"]:
        report_xls(paths, auxpaths,RampDownCurve(paths, auxpaths, comparison, params))
  print("\nDone generating ramp down curve(s).")


def vizTask(outputpath, inputfolder, comparisons):
  from vizScripts.createVizCSV import createVizCSV
  import webbrowser
  import threading
  checkCreate( outputpath, "Viz" )
  for comparison in comparisons:
    inputfile = os.path.join(inputfolder, comparison["fromID"] + "_" + comparison["toID"] + "_report_augmented.csv")
    outputfile = os.path.join(outputpath, comparison["fromID"] + "_" + comparison["toID"] + "_diffViz.csv")
    createVizCSV( outputfile, inputfile, comparison )

  with open("vizScripts/currentData.js", "w") as f:
    f.write("currentData = \"" + "../../../CrimsonProject/output/Visualization/" + comparison["fromID"] + "_" + comparison["toID"] + "_diffViz.csv" + "\"")

  serverThread = threading.Thread(name="serverThread", target = start_server)
  serverThread.start()
  print("localhost server started")

  if _platform == "linux" or _platform == "linux2":
    chrome_path = '/usr/bin/google-chrome %s'
  elif _platform == "darwin":
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
  elif _platform == "win32":
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
  url = "http://localhost:8123/CrimsonCodeAnalysis/scripts/vizScripts/diffOutputViz.html"
  webbrowser.get(chrome_path).open_new_tab(url)

  serverThread.join()

def start_server():
  from http.server import HTTPServer, SimpleHTTPRequestHandler
  Handler = SimpleHTTPRequestHandler
  os.chdir("../..")
  server = HTTPServer(('localhost', 8123), Handler)
  server.serve_forever()

def parseArgs():
  parser = argparse.ArgumentParser(description = "Version and Comparison File.")
  parser.add_argument('ckprojectpath', help = "Location to Put new projects. Project location includes versions and comparisons file")
  parser.add_argument('ckprojectdir', help = "Name of project directory. Project location includes versions and comparisons file")

  args = parser.parse_args()
  return args

def main(args):
  print("Starting codeKey analysis...\n\n")

  if _platform == "linux" or _platform == "linux2":
    print("Running on Linux...\n\n")
  elif _platform == "darwin":
    print("Running on Mac OS...\n\n")
  elif _platform == "win32":
    print("Running on Windows...\n\n")

  start_time = time.time()

  DefaultCKProject = CKProject(args.ckprojectpath, args.ckprojectdir, None, SCRIPTMODE)

  DefaultCKProject.readVersionsFromJSON(None)
  DefaultCKProject.loadComparisonsFromJSON(None)
  
  runTasks(DefaultCKProject)
  print("Run time: %.3fs" % (time.time() - start_time))


if __name__ == "__main__":
  args = parseArgs()
  main(args)
