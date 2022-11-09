#Version.py
#Created 02/02/2017
#hiroki.moto.pro@outlook.com

#Defines the Comparisons class
#Contains init, validity check and comparator functions
#The comparisons class is used to create a list of comparisons
#That is used in CKProject

from guiScripts.defaultParams import *

class Comparisons:
  "Comparisons Class"

  def __init__(self, paths = None, auxpaths = None, parameters = None, tasks = None, comparisons = None):
    self.paths = paths
    self.auxpaths = auxpaths
    self.parameters = parameters
    self.tasks = tasks
    self.comparisons = comparisons

  def addComparison(self, comparison):
    self.comparisons.append(comparison)

  def removeComparison(self):
    if len(self.comparisons) > 0:
      self.comparisons.pop()
    else:
      print("Bro it's already empty.")

  def addParameter(self, parameter):
    self.parameters.append(parameter)

  def removeParameter(self):
    if len(self.parameters) > 0:
      self.parameters.pop()
    else:
      print("Bro it's already empty.")

  def addTask(self):
    self.tasks.append(defaultTask())

  def removeTask(self):
    if len(self.tasks) > 0:
      self.tasks.pop()
    else:
      print("Bro it's already empty.")

  def clearComprisons(self):
    self.paths = []
    self.auxpaths = []
    self.parameters = []
    self.tasks = []
    self.comparisons = []
