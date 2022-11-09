#CKProject.py
#Created 08/16/2016
#ssia@keystonestrategy.com

#Takes in listOfVersions.json and listOfComparisons.json
#Loads them into comparisons and paths

#Input:
#  versions.json
#  comparisons.json 

import json
import os
import logging
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from sys import platform as _platform
from utilScripts.util import *
from utilScripts.Version import Version
from utilScripts.Comparisons import Comparisons
from utilScripts.staticvars import *

class CKProject:

  def __init__(self, projectpath = None, projectName = None, inputFolder = None, clocLocation = None, undLocation = None , runMode = None):
    self.projectpath = projectpath
    self.projectName = projectName
    self.inputFolder = inputFolder
    self.clocLocation = clocLocation
    self.undLocation  = undLocation
    self.runMode = runMode
    self.error = 0
    self.versions = None

    checkValidFolderName(projectName)
    try:
      assert(os.path.exists(projectpath))
    except AssertionError:
      print("Directory in which to put project file does not exist.")
      self.error = 1
      return

    self.projectpath = os.path.join(self.projectpath, projectName)
    #Create the various directories if they do not currently exist
    checkCreate(self.projectpath, "Project")
    self.configpath = os.path.join(self.projectpath, "configs")
    checkCreate(self.configpath, "Configs")
    self.outputpath = os.path.join(self.projectpath, "results")
    checkCreate(self.outputpath, "Output")

    self.OutputFolders = self.OutputFolders(self.outputpath)

    #Currently they will always exist, need to handle the case for a default versions and comparisons
    #form if they currently do not exist.
    self.versionspath = os.path.join(self.configpath, "versions.json")
    self.comparisonspath = os.path.join(self.configpath, "comparisons.json")
    self.langdefpath = os.path.join(self.configpath, "cloc-lang-def.txt")
    self.metastringspath = os.path.join(self.configpath, "metaStrings.json")

    currentpath = os.path.realpath(__file__)
    self.sourcepath = str(Path(currentpath).parent.parent.parent)

  #Create a initial project
  def createNewProject(self):
    if not os.path.exists(self.versionspath):
      copyFile(os.path.join(self.sourcepath, "auxiliary_datasets/versions.json"), self.versionspath)
    if not os.path.exists(self.comparisonspath):
      copyFile(os.path.join(self.sourcepath, "auxiliary_datasets/comparisons.json"), self.comparisonspath)
    if not os.path.exists(self.langdefpath):
      copyFile(os.path.join(self.sourcepath, "auxiliary_datasets/cloc-lang-def.txt"), self.langdefpath)
    if not os.path.exists(self.metastringspath):
      copyFile(os.path.join(self.sourcepath, "auxiliary_datasets/metaStrings.json"), self.metastringspath)
    self.autoComparisons()

  def autoComparisons(self):
    with open(self.comparisonspath) as versions_file:
      comp_data = json.load(versions_file)

    comp_data["paths"]["inputFolder"] = self.inputFolder
    comp_data["paths"]["undpath"] = self.undLocation
    comp_data["paths"]["cloc"] = self.clocLocation

    if _platform == "linux" or _platform == "linux2":
      pass
    elif _platform == "darwin":
      comp_data["paths"]["langDef"] = os.path.join(self.projectpath, "configs/cloc-lang-def.txt")
      comp_data["paths"]["strings"] = os.path.join(self.projectpath, "configs/metaStrings.json")

      comp_data["paths"]["diffout"] = os.path.join(self.projectpath, "outputs/01_diff_output/")
      comp_data["paths"]["depout"] = os.path.join(self.projectpath, "outputs/02_deptest/")
      comp_data["paths"]["profout"] = os.path.join(self.projectpath, "outputs/03_profiler/")
      comp_data["paths"]["rampout"] = os.path.join(self.projectpath, "outputs/04_ramp_down_output/")
      comp_data["paths"]["vizout"] = os.path.join(self.projectpath, "outputs/05_viz_output/")
      
      comp_data["auxpaths"]["tools"] = os.path.join(self.sourcepath, "auxiliary_datasets/tools.csv")
      comp_data["auxpaths"]["code"] = os.path.join(self.sourcepath, "auxiliary_datasets/code.csv")
      comp_data["auxpaths"]["nonCode"] = os.path.join(self.sourcepath, "auxiliary_datasets/nonCode.csv")
      comp_data["auxpaths"]["thirdparty"] = os.path.join(self.sourcepath, "auxiliary_datasets/thirdparty.csv")
      comp_data["auxpaths"]["deployments"] = os.path.join(self.sourcepath, "auxiliary_datasets/deployments.csv")
      comp_data["auxpaths"]["exclude"] = os.path.join(self.sourcepath, "auxiliary_datasets/exclude.csv")

    elif _platform == "win32":
      comp_data["paths"]["langDef"] = os.path.join(self.projectpath, "configs/cloc-lang-def.txt")
      comp_data["paths"]["strings"] = os.path.join(self.projectpath, "configs/metaStrings.json")

      comp_data["paths"]["diffout"] = os.path.join(self.projectpath, "outputs/01_diff_output/")
      comp_data["paths"]["depout"] = os.path.join(self.projectpath, "outputs/02_deptest/")
      comp_data["paths"]["profout"] = os.path.join(self.projectpath, "outputs/03_profiler/")
      comp_data["paths"]["rampout"] = os.path.join(self.projectpath, "outputs/04_ramp_down_output/")
      comp_data["paths"]["vizout"] = os.path.join(self.projectpath, "outputs/05_viz_output/")

      comp_data["auxpaths"]["tools"] = os.path.join(self.sourcepath, "auxiliary_datasets/tools.csv")
      comp_data["auxpaths"]["code"] = os.path.join(self.sourcepath, "auxiliary_datasets/code.csv")
      comp_data["auxpaths"]["nonCode"] = os.path.join(self.sourcepath, "auxiliary_datasets/nonCode.csv")
      comp_data["auxpaths"]["thirdparty"] = os.path.join(self.sourcepath, "auxiliary_datasets/thirdparty.csv")
      comp_data["auxpaths"]["deployments"] = os.path.join(self.sourcepath, "auxiliary_datasets/deployments.csv")
      comp_data["auxpaths"]["exclude"] = os.path.join(self.sourcepath, "auxiliary_datasets/exclude.csv")
    
    with open(self.comparisonspath, 'w') as outfile:
      json.dump(comp_data, outfile, indent = 2)

  #Arrange version for Version class
  def getParameters(self, version):
    data = {}
    tags = {}
    for key in version.keys():
      if key == "id" or key == "folder" or key == "date":
        data[key] = version[key]
      else:
        tags[key] = version[key]
    data["tags"] = tags
    return data

  def errorChecks(self):
    _versions = []
    for version in self.versions:
      _version = self.getParameters(version)
      self.Version = Version(_version["id"], _version["folder"], _version["date"], _version["tags"])
      if self.Version.error == 0:
        _versions.append(version)
    self.versions = _versions

  #Checks if id of version is unique
  def isUniqueId(self, newVersion):
    try:
      if self.versions == None:
        self.versions = []
        return True
      else:
        for version in self.versions:
          if version["id"] == newVersion["id"]:
            return False
        return True
    except TypeError:
      print("Error: version is not a valid version.")
      return False

  #Perform comparator check to ensure that the added version has a unique version ID
  def addVersion(self, version):
    try:
      if self.isUniqueId(version):
        self.versions.append(version)
        return True
      else:
        raise ValueError("Error: version %s is not a unique version" % version["id"])
        return False
    except Exception as error:
      print(str(error))

  #Clear versions list
  def clearVersionsList(self):
    self.versions = []

  #Modify specific version
  def modifyVersion(self, oldId, newVersion):
    try:
      length = len(self.versions)
      for i in range(length):
        if self.versions[i]["id"] == oldId:
          if oldId == newVersion["id"]:
            self.versions[i] = newVersion
            return True
          else:
            if self.isUniqueId(newVersion):
              self.removeVersion(oldId)
              self.versions.insert(i, newVersion)
              return True
            else:
              raise ValueError("Error: version %s is not a unique version" % newVersion["id"])
              return False
    except ValueError as error:
      print(str(error))

  #Remove specific version
  def removeVersion(self, oldId):
    try:
      for version in self.versions:
        if version["id"] == oldId:
          self.versions.remove(version)
          return True
      return False
    except TypeError:
      print("Error: versions list is not valid")
      return False

  def readVersionsFromJSON(self, filepath = None):
    if filepath != None:
      self.versionspath = filepath
    try:
      with open(self.versionspath) as versions_file:
        version_data = json.load(versions_file)
      self.versions = version_data["versions"]
      if filepath != None:
        self.errorChecks()
    except FileNotFoundError:
      print("Versions File does not exist yet. Creating...")
      self.createVersionsFile()

  #Takes in a filepath
  #Writes the current versionspath to the output json file
  #Usage: self.writeVersionsToJSON(self.versionspath)
  #Add error checks for the directory path
  def writeVersionsToJSON(self, filepath):
    if filepath == None:
      self.errorChecks()
      _versions = {"versions": []}
      _versions["versions"] = self.versions
      with open(self.versionspath, 'w') as versions_file:
        json.dump(_versions, versions_file, indent=2)
    else:
      self.errorChecks()
      _versions = {"versions": []}
      _versions["versions"] = self.versions
      with open(filepath, 'w') as versions_file:
        json.dump(_versions, versions_file, indent=2)

  def loadComparisonsFromJSON(self, filepath = None):
    #Open the comparisonspath and save it internally as list of comparisons to look at
    if filepath != None:
      self.comparisonspath = filepath
    try:
      with open(self.comparisonspath) as comparisons_file:
        comp_data = json.load(comparisons_file)
      self.Comparisons = Comparisons(comp_data["paths"], comp_data["auxpaths"], comp_data["parameters"], comp_data["tasks"], comp_data["comparisons"])
      self.exportComparisonsToJSON()
    except FileNotFoundError:
      print("Comparisons Path Does not yet exist. Creating...")
      self.createComparisonsFile()

    #Eventually there are other reasons why we would string comparisons together or mark them.
    if filepath == None:
      self.appendComparisons()
      self.noDuplicateComparisons()
      if self.runMode == SCRIPTMODE:
        self.expandListPaths()
      else:
        pass
        #self.expandListPaths()
      self.getCompVersions()

  def exportComparisonsToJSON(self, filepath = None):
    if filepath != None:
      self.comparisonspath = filepath
    try:
      self.comp_data = {}
      self.comp_data["tasks"] = self.Comparisons.tasks
      self.comp_data["paths"] = self.Comparisons.paths
      #self.comp_data["paths"]["inputFolder"] = self.inputFolder
      self.comp_data["auxpaths"] = self.Comparisons.auxpaths
      self.comp_data["comparisons"] = self.Comparisons.comparisons
      self.comp_data["parameters"] = self.Comparisons.parameters

      for comparison in self.comp_data["comparisons"]:
        if comparison["fromID"] == "Not Defined":
          self.notDefinedError()
          return
        if comparison["toID"] == "Not Defined":
          self.notDefinedError()
          return

      with open(self.comparisonspath, 'w') as outfile:
        json.dump(self.comp_data, outfile, indent = 2)
      print("Comparisons file saved.")
    except Exception as e:
      print(str(e))

  def notDefinedError(self):
    msg = QMessageBox()
    msg.setWindowTitle("Config Error")
    msg.setText("Comparison fromID/toID not defined.")
    msg.setInformativeText("File not saved:")
    msg.setDetailedText("""Try defining the comparisons, or deleting unwanted comparisons.
      Go to the comparisons tab and set the fromID and toID options correctly""")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    retval = msg.exec_()

  class OutputFolders:
    def __init__(self, outputpath):
      self.rampout = os.path.join(outputpath, "Reports")
      self.diffout = os.path.join(outputpath, "Diffs")
      self.profout = os.path.join(outputpath, "Profiling") 
      self.vizout = os.path.join(outputpath, "Visualization") 
      self.depout = os.path.join(outputpath, "Dependencies") 

  def createVersionsFile(self):
    print("This is currently fatal but will be created in the future. \
      \n Program exiting")
    exit()

  def createComparisonsFile(self):
    print("This is currently fatal but will be created in the future. \
      \n Program exiting")
    exit()

  #Get list of all versions involved from comparisons
  def getCompVersions(self):
    self.compVersions = []
    for comparison in self.Comparisons.comparisons:
      if comparison["fromVersion"] not in self.compVersions:
        self.compVersions.append(comparison["fromVersion"])
      if comparison["toVersion"] not in self.compVersions:
        self.compVersions.append(comparison["toVersion"])

  def appendComparisons(self):
    #For each conditions in list
    for comparison in self.Comparisons.comparisons:
      for version in self.versions:
        if comparison["fromID"] == version["id"]:
          comparison["fromFolder"] = version["folder"]
          comparison["fromVersion"] = version
        if comparison["toID"] == version["id"]:
          comparison["toFolder"] = version["folder"]
          comparison["toVersion"] = version
      #if not "fromFolder" in comparison:
        #raise ValueError("Error: folder of fromID not found in versions list", comparison["fromID"])
      #if not "toFolder" in comparison:
        #raise ValueError("Error: folder of toID not found in versions list", comparison["toID"])

  #Error check make sure there's no duplicate comparison.
  def noDuplicateComparisons(self):
    compList = []
    for comparison in self.Comparisons.comparisons:
      addToList = (comparison["fromID"], comparison["toID"])
      if addToList in compList:
        raise Exception( """Duplicate comparisons detected: %s and %s in comparisons file. 
      There should not be duplicates.""" % (comparison["fromID"], comparison["toID"]) )
      compList.append(addToList)

  #given a list of listpath CSV filess, read in the CSVs 
  #outputs a list of listpaths.
  def expandListPaths(self):
    for key in self.Comparisons.auxpaths:
      listPaths = []
      filename = self.Comparisons.auxpaths[key]
      for row in read_csv(filename):
        if (len(row) == 1):
          listPaths.extend(row)
        elif (len(row) > 1):
          print("Row ignored: ")
          print(row)
      self.Comparisons.auxpaths[key] = listPaths

def checkValidFolderName(projectName):
  pass
