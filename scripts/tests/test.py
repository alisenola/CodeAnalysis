#versions.py
#Created 02/04/2017
#hiroki.moto.pro@outlook.com

#Unit test for readVersionsFromJSON and writeVersionsToJSON functions

#Input:
# versions.json
# vversions2.json 

import unittest
import sys
import os
import json
from utilScripts.Version import Version
from utilScripts.CKProject import CKProject
from guiScripts.defaultParams import *

class VersionsTest(unittest.TestCase):
  def setUp(self):
    self.versions = [{
      "category": "engine",
      "studio": "Infinity Ward",
      "id": "MW2src_sp",
      "date": "2/1/2007",
      "check": "alternate",
      "folder": "/Volumes/Works/Works/Solomon/CrimsonCodeAnalysis/auxiliary_datasets"
    }]
    self.readVersionPath = "/Volumes/Works/Works/Solomon/CrimsonCodeAnalysis/scripts/tests/vversions.json"
    self.writeVersionPath = "/Volumes/Works/Works/Solomon/CrimsonCodeAnalysis/scripts/tests/vversions2.json"
    self.readComparisonPath = "/Volumes/Works/Works/Solomon/CrimsonCodeAnalysis/scripts/tests/ccomparisons.json"
    self.writeComparisonPath = "/Volumes/Works/Works/Solomon/CrimsonCodeAnalysis/scripts/tests/ccomparisons2.json"
    self.CKProject = CKProject("", "", "")
    
  def test_readandwriteVersions(self):
    self.CKProject.readVersionsFromJSON(self.readVersionPath)
    self.CKProject.writeVersionsToJSON(self.writeVersionPath)
    with open(self.readVersionPath) as read_file:
      version_read = json.load(read_file)
    with open(self.writeVersionPath) as write_file:
      version_write = json.load(write_file)
    self.assertEqual(version_read, version_write)

  def test_cearVersionsList(self):
    self.CKProject.readVersionsFromJSON(self.readVersionPath)
    self.CKProject.clearVersionsList()
    self.assertEqual(self.CKProject.versions, [])

  def test_addVersion(self):
    self.CKProject.clearVersionsList()
    self.CKProject.addVersion(self.versions[0])
    self.assertEqual(self.CKProject.versions, self.versions)

  def test_removeVersion(self):
    self.CKProject.clearVersionsList()
    self.CKProject.addVersion(self.versions[0])
    self.CKProject.removeVersion(self.versions[0]["id"])
    self.assertEqual(self.CKProject.versions, [])

  def test_readandwriteComparisons(self):
    self.CKProject.loadComparisonsFromJSON(self.readComparisonPath)
    self.CKProject.exportComparisonsToJSON(self.writeComparisonPath)
    with open(self.readComparisonPath) as read_file:
      comparisons_read = json.load(read_file)
    with open(self.writeComparisonPath) as write_file:
      comparisons_write = json.load(write_file)
    self.assertEqual(comparisons_read, comparisons_write)

  def test_addremoveComparison(self):
    self.CKProject.loadComparisonsFromJSON(self.readComparisonPath)
    comparisons = self.CKProject.Comparisons.comparisons
    self.CKProject.Comparisons.addComparison(defaultComp())
    self.CKProject.Comparisons.removeComparison()
    self.assertEqual(comparisons, self.CKProject.Comparisons.comparisons)

  def test_addremoveParameter(self):
    self.CKProject.loadComparisonsFromJSON(self.readComparisonPath)
    parameters = self.CKProject.Comparisons.parameters
    parameter = ("Not Defined", False)
    self.CKProject.Comparisons.addParameter(parameter)
    self.CKProject.Comparisons.removeParameter()
    self.assertEqual(parameters, self.CKProject.Comparisons.parameters)

if __name__ == '__main__':
  unittest.main()
