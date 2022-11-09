#!/usr/bin/python3
# -*- coding: utf-8 -*-

############################
#CodeKey GUI Comparison Form
# ssia@keystonestrategy.com
#Created 11/15/2016
#
# Dock for filling out CodeKey GUI Comparisons Form
# Includes the tasks form list
# And also the Paths Form List
############################

from collections import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from guiScripts.defaultParams import *

#Extend a form class
class TasksForm(QScrollArea):

  def __init__(self, Comparisons = None):
    super().__init__()     
    self.initUI(Comparisons)
         
  def initUI(self, Comparisons):
    self.Comparisons = Comparisons
    self.createFbox()
    self.setWidgetResizable(True)

  def createFbox(self):
    fbox = QFormLayout()
    self.groupBox = QGroupBox('Select Analysis to Run')

    self.checkBoxList = []

    for task in self.Comparisons.tasks:
      checkBox = QCheckBox(task["type"])
      self.checkBoxList.append(checkBox)
      checkBox.stateChanged.connect(self.tasksUpdate)
      if task["run"] == "True":
        checkBox.setChecked(True)

    for checkBox in self.checkBoxList:
      fbox.addRow(checkBox)

    self.groupBox.setLayout(fbox)
    scroll = QScrollArea()
    scroll.setWidget(self.groupBox)
    scroll.setWidgetResizable(True)

    layout = QVBoxLayout(self)
    layout.addWidget(scroll)
    self.submitButton = QPushButton("Save Configs")
    layout.addWidget(self.submitButton)

  def tasksUpdate(self):
    for (i,checkBox) in enumerate(self.checkBoxList):
      if checkBox.isChecked():
        self.Comparisons.tasks[i]["run"] = "True"
      else:
        self.Comparisons.tasks[i]["run"] = "False"

class PathOptions(QObject):
  def __init__(self, labelName, labelPath):
    self.label = QLabel(labelName)
    self.lineEdit = QLineEdit(labelPath)
    self.button = QPushButton()
    self.hbox = QHBoxLayout()

    self.hbox.addWidget(self.lineEdit)
    self.hbox.addWidget(self.button)

    self.button.setIcon(QIcon("open.jpg"))
    self.button.dirName = ""
    self.button.clicked.connect(lambda: self.chooseDir() )

  def chooseDir(self):
    file = str(QFileDialog.getExistingDirectory(self.button, "Select Directory"))
    self.lineEdit.setText(file)

class FileOptions(QObject):
  def __init__(self, labelName, labelPath):
    self.label = QLabel(labelName)
    self.lineEdit = QLineEdit(labelPath)
    self.button = QPushButton()
    self.hbox = QHBoxLayout()

    self.hbox.addWidget(self.lineEdit)
    self.hbox.addWidget(self.button)

    self.button.setIcon(QIcon("open.jpg"))
    self.button.dirName = ""
    self.button.clicked.connect(lambda: self.chooseFile() )

  def chooseFile(self):
    file = QFileDialog.getOpenFileName(self.button, "Select Directory")
    self.lineEdit.setText(str(file[0]))

class CompSelector(QObject):
  def __init__(self, labelName, versionName, items):
    super().__init__()
    self.initUI(labelName, versionName, items)

  def initUI(self, labelName, versionName, items):
    self.label = QLabel(labelName)
    self.cb = QComboBox()
    self.cb.addItems(items)
    try:
      self.cb.setCurrentIndex(items.index(versionName))
    except:
      print("Warning, no comboBox item: ", versionName)
      print("Change versions file to get combobox. Currently setting it to Not Defined.")
      self.cb.setCurrentIndex(items.index("Not Defined") )

class ParamSelector(QObject):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.le = QLineEdit()
    self.hbox = QHBoxLayout()
    self.group = QButtonGroup()
    self.but1 = QRadioButton("Include")
    self.but2 = QRadioButton("Exclude")

    self.group.addButton(self.but1)
    self.group.addButton(self.but2)
    self.but1.setChecked(True)
    self.hbox.addWidget(self.but1)
    self.hbox.addWidget(self.but2)

class ParamsForm(QScrollArea):

  def __init__(self, Comparisons = None):
    super().__init__()     
    self.initUI(Comparisons)

  def initUI(self, Comparisons):
    self.group = QGroupBox()
    self.Comparisons = Comparisons
    self.scroll = QScrollArea()

    self.createFormBox()
    self.setWidgetResizable(True)

    layout = QVBoxLayout(self)
    layout.addWidget(self.scroll)
    self.submitButton = QPushButton("Save Configs")
    layout.addWidget(self.submitButton)

  def createFormBox(self):
    self.fbox = QFormLayout()
    self.groupBox = QGroupBox("Select Filter Parameters")

    self.paramList = []

    for param in self.Comparisons.parameters:
      self.addParams(param)

    self.groupBox.setLayout(self.fbox)

    self.scroll.setWidget(self.groupBox)
    self.scroll.setWidgetResizable(True)

    self.addButton = QPushButton("Add param")
    self.addButton.clicked.connect(self.addParamDatas)
    self.removeButton = QPushButton("Remove param")
    self.removeButton.clicked.connect(self.removeParamDatas)
    self.fbox.addRow(self.addButton, self.removeButton)

  def addParams(self, param):
    paramName = param[0]
    includeBool = param[1]
    number_group = QButtonGroup(self) # Number group

    r0 = QRadioButton("Exclude")
    number_group.addButton(r0)
    r1 = QRadioButton("Include")
    number_group.addButton(r1)

    if includeBool:
      r1.setChecked(True)
    else:
      r0.setChecked(True)

    hbox2 = QHBoxLayout()
    hbox2.addWidget(r0)
    hbox2.addWidget(r1)

    lineEdit = QLineEdit(paramName)
    r0.toggled.connect(self.paramsUpdate)
    lineEdit.textChanged.connect(self.paramsUpdate)
    self.fbox.addRow(lineEdit, hbox2)
    self.paramList.append((lineEdit, r1))

  def paramsUpdate(self):
    print("Woo updating params")
    for i, param in enumerate(self.paramList):
      self.Comparisons.parameters[i] = (param[0].text() , param[1].isChecked())

  def addParamDatas(self):
    parameter = ("Not Defined", False)
    self.Comparisons.addParameter(parameter)
    self.createFormBox()

  def removeParamDatas(self):
    self.Comparisons.removeParameter()
    if len(self.Comparisons.parameters) > 0:
      self.createFormBox()

class CompForm(QScrollArea):
    #Comparisons take on a instance of Comparisons class

  def __init__(self, Comparisons = None, version_data = None):
    super().__init__()     
    self.initUI(Comparisons, version_data)

  def initUI(self, Comparisons, version_data):
    self.group = QGroupBox()
    self.Comparisons = Comparisons
    self.version_data = version_data
    self.scroll = QScrollArea()

    self.createFormBox()
    self.setWidgetResizable(True)

    layout = QVBoxLayout(self)
    layout.addWidget(self.scroll)
    self.submitButton = QPushButton("Save Configs")
    layout.addWidget(self.submitButton)

  def createFormBox(self):
    self.fbox = QFormLayout()
    self.groupBox = QGroupBox("Select Comparison Versions")

    versions = []
    for version in self.version_data:
      versions.append(version["id"])

    self.compList = []

    for comparison in self.Comparisons.comparisons:
      fromID = CompSelector("fromID", comparison["fromID"], versions)
      toID = CompSelector("toID", comparison["toID"], versions)
      self.fbox.addRow(fromID.label, fromID.cb)
      self.fbox.addRow(toID.label, toID.cb)
      fromID.cb.currentIndexChanged.connect(self.compsUpdate)
      toID.cb.currentIndexChanged.connect(self.compsUpdate)
      self.compList.append( (fromID,toID) )

    self.addButton = QPushButton('Add comparison')
    self.addButton.clicked.connect(self.addComparison)
    self.removeButton = QPushButton('Remove comparison')
    self.removeButton.clicked.connect(self.removeComparison)
    self.fbox.addRow(self.addButton, self.removeButton)

    self.groupBox.setLayout(self.fbox)

    self.scroll.setWidget(self.groupBox)
    self.scroll.setWidgetResizable(True)

  def compsUpdate(self):
    print("wooo updating comps")
    for i, comp in enumerate(self.compList):
      self.Comparisons.comparisons[i]["fromID"] = comp[0].cb.currentText()
      self.Comparisons.comparisons[i]["toID"] = comp[1].cb.currentText()

  def addComparison(self):
    self.Comparisons.addComparison(defaultComp())
    #Update formBox UI
    self.createFormBox()

  def removeComparison(self):
    self.Comparisons.removeComparison()
    self.createFormBox()
