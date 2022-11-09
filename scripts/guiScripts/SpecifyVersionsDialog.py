#!/usr/bin/python3
# -*- coding: utf-8 -*-

############################
#CodeKey GUI
# hiroki.moto.pro@outlook.com
#Created 02/04/2017
#
# Popup window for Versions
############################

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from guiScripts.CompareForm import PathOptions

class SpecifyVersionsDialog(QWidget):
  def __init__(self, ckProject = None):
    super().__init__()

    self.ckProject = ckProject
    self.initUI()

  def initUI(self):
    self.setWindowTitle("Specify Versions")
    self.setWindowIcon(QIcon("qIcon.png"))
    #
    self.gridLayout = QGridLayout()
    self.gridLayout.setRowMinimumHeight(0, 30)
    self.gridLayout.setRowMinimumHeight(1, 100)
    self.gridLayout.setRowMinimumHeight(2, 30)
    self.gridLayout.setRowMinimumHeight(3, 30)
    self.setLayout(self.gridLayout)
    #
    self.versionsComboLayout = QFormLayout()
    self.versionNamesCombobox = QComboBox()
    if self.ckProject.versions == None:
      self.versionNamesCombobox.setEnabled(False)
    else:
      for version in self.ckProject.versions:
        self.versionNamesCombobox.addItem(version["id"])
    self.versionsComboLayout.addRow("Versions: ", self.versionNamesCombobox)
    self.versionNamesCombobox.currentIndexChanged.connect(self.onVersionsSelectionChanged)
    self.gridLayout.addLayout(self.versionsComboLayout, 0, 0)
    #
    self.versionInfoLayout = QFormLayout()
    self.idLineEdit = QLineEdit("id")
    self.dateLineEdit = QLineEdit("date")
    self.folderLineEdit = QLineEdit("folder")
    self.studioLineEdit = QLineEdit("studio")
    self.checkLineEdit = QLineEdit("check")
    self.categoryLineEdit = QLineEdit("category")
    self.clearTexts()
    #
    self.versionInfoLayout.addRow("id:       ", self.idLineEdit)
    self.versionInfoLayout.addRow("date:     ", self.dateLineEdit)
    self.versionInfoLayout.addRow("folder:   ", self.folderLineEdit)
    self.versionInfoLayout.addRow("studio:   ", self.studioLineEdit)
    self.versionInfoLayout.addRow("check:    ", self.checkLineEdit)
    self.versionInfoLayout.addRow("category: ", self.categoryLineEdit)
    self.gridLayout.addLayout(self.versionInfoLayout, 1, 0)
    #
    self.controlVersionLayout = QHBoxLayout()
    self.controlVersionLayout.addStretch(1)
    self.addButton = QPushButton("Add")
    self.modifyButton = QPushButton("Modify")
    self.removeButton = QPushButton("Remove")
    self.controlVersionLayout.addWidget(self.addButton)
    self.controlVersionLayout.addWidget(self.modifyButton)
    self.controlVersionLayout.addWidget(self.removeButton)
    self.addButton.clicked.connect(lambda: self.addVersion())
    self.modifyButton.clicked.connect(lambda: self.modifyVersion())
    self.removeButton.clicked.connect(lambda: self.removeVersion())
    self.gridLayout.addLayout(self.controlVersionLayout, 2, 0)

    if self.ckProject.versions == None:
      self.modifyButton.setEnabled(False)
    #
    self.boardLayout = QHBoxLayout()
    self.importButton = QPushButton("Import")
    self.saveButton = QPushButton("Save")
    self.boardLayout.addStretch(1)
    self.boardLayout.addWidget(self.importButton)
    self.boardLayout.addWidget(self.saveButton)
    self.importButton.clicked.connect(lambda: self.importVersions())
    self.saveButton.clicked.connect(lambda: self.saveVersions())
    self.gridLayout.addLayout(self.boardLayout, 3, 0)
    #
    self.setMinimumSize(QSize(300, 200))
    self.show()

  def onVersionsSelectionChanged(self, index):
    self.currentIndex = index
    if "id" in self.ckProject.versions[index].keys():
      self.idLineEdit.setText(self.ckProject.versions[index]["id"])
    else:
      self.idLineEdit.setText("Not Defined")
    if "date" in self.ckProject.versions[index].keys():
      self.dateLineEdit.setText(self.ckProject.versions[index]["date"])
    else:
      self.dateLineEdit.setText("Not Defined")
    if "folder" in self.ckProject.versions[index].keys():
      self.folderLineEdit.setText(self.ckProject.versions[index]["folder"])
    else:
      self.folderLineEdit.setText("Not Defined")
    if "check" in self.ckProject.versions[index].keys():
      self.checkLineEdit.setText(self.ckProject.versions[index]["check"])
    else:
      self.checkLineEdit.setText("Not Defined")
    if "studio" in self.ckProject.versions[index].keys():
      self.studioLineEdit.setText(self.ckProject.versions[index]["studio"])
    else:
      self.studioLineEdit.setText("Not Defined")
    if "category" in self.ckProject.versions[index].keys():
      self.categoryLineEdit.setText(self.ckProject.versions[index]["category"])
    else:
      self.categoryLineEdit.setText("Not Defined")

  def addVersion(self):
    self.updateVersion()
    if self.ckProject.addVersion(self.version):
      self.updateUI()
      print("Notice: A version %s has been added." % self.version["id"])

  def modifyVersion(self):
    self.updateVersion()
    oldId = self.versionNamesCombobox.currentText()
    if self.ckProject.modifyVersion(oldId, self.version):
      self.updateUI(self.currentIndex)
      print("Notice: A version %s has been modified." % oldId)

  def removeVersion(self):
    oldId = str(self.versionNamesCombobox.currentText())
    if self.ckProject.removeVersion(oldId):
      self.updateUI(self.currentIndex)
      print("Notice: A version %s has been removed." % oldId)

  def importVersions(self):
    fname = QFileDialog.getOpenFileName(self, "Load Versions File", "/home/", "JSON (*.json)")
    if fname[0]:
      self.ckProject.readVersionsFromJSON(fname[0])
      self.updateUI()

  def saveVersions(self):
    self.ckProject.writeVersionsToJSON(None)
    self.close()
    print("Notice: versions has been saved at '%s'" % self.ckProject.versionspath)

  def clearTexts(self):
    self.idLineEdit.setText("")
    self.dateLineEdit.setText("")
    self.folderLineEdit.setText("")
    self.checkLineEdit.setText("")
    self.studioLineEdit.setText("")
    self.categoryLineEdit.setText("")

  def updateVersion(self):
    if self.ckProject == None:
      raise ValueError("Error: version %s is not a unique version" % version["id"])
    else:
      self.version = {}
      self.version["id"] = self.idLineEdit.text()
      self.version["date"] = self.dateLineEdit.text()
      self.version["folder"] = self.folderLineEdit.text()
      self.version["check"] = self.checkLineEdit.text()
      self.version["studio"] = self.studioLineEdit.text()
      self.version["category"] = self.categoryLineEdit.text()

  def updateUI(self, index = None):
    self.versionNamesCombobox.clear()
    self.versionNamesCombobox.clearEditText()
    self.versionNamesCombobox.removeItem(0)
    self.clearTexts()

    if self.ckProject.versions != None:
      self.versionNamesCombobox.setEnabled(True)
      self.modifyButton.setEnabled(True)

    for version in self.ckProject.versions:
      self.versionNamesCombobox.addItem(version["id"])
    if index == None:
      lastIndex = len(self.ckProject.versions) - 1
      self.versionNamesCombobox.setCurrentIndex(lastIndex)
    else:
      lastIndex = len(self.ckProject.versions) - 1
      if index > lastIndex:
        index = lastIndex
      self.versionNamesCombobox.setCurrentIndex(index)
