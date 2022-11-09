#!/usr/bin/python3
# -*- coding: utf-8 -*-

############################
#CodeKey GUI
# hiroki.moto.pro@outlook.com
#Created 02/04/2017
#
# Popup window for Versions
############################

import json
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from guiScripts.CompareForm import FileOptions

class InstallConfigDialog(QWidget):
  def __init__(self, configPath):
    super().__init__()

    self.configPath = configPath
    self.initUI()

  def initUI(self):


    self.setWindowTitle("Specify Versions")
    self.setWindowIcon(QIcon("qIcon.png"))
    #
    self.gridLayout = QGridLayout()
    self.gridLayout.setRowMinimumHeight(0, 30)
    self.gridLayout.setRowMinimumHeight(1, 30)
    self.setLayout(self.gridLayout)
    #
    self.configsInfoLayout = QFormLayout()
    self.clocFileOptions = FileOptions("Cloc Location:", "")
    self.undsFileOptions = FileOptions("Unds Location:", "")
    #
    self.configsInfoLayout.addRow(self.clocFileOptions.label, self.clocFileOptions.hbox)
    self.configsInfoLayout.addRow(self.undsFileOptions.label, self.undsFileOptions.hbox)
    self.gridLayout.addLayout(self.configsInfoLayout, 0, 0)
    self.clocFileOptions.lineEdit.textChanged.connect(self.pathsUpdate)
    self.undsFileOptions.lineEdit.textChanged.connect(self.pathsUpdate)
    #
    self.boardLayout = QHBoxLayout()
    self.cancelButton = QPushButton("Cancel")
    self.saveButton = QPushButton("Save")
    self.boardLayout.addStretch(1)
    self.boardLayout.addWidget(self.cancelButton)
    self.boardLayout.addWidget(self.saveButton)
    self.cancelButton.clicked.connect(lambda: self.cancelConfigs())
    self.saveButton.clicked.connect(lambda: self.saveConfigs())
    self.gridLayout.addLayout(self.boardLayout, 1, 0)
    #
    self.setMinimumSize(QSize(300, 200))
    self.show()

  def pathsUpdate(self):
    self.clocPath = self.clocFileOptions.lineEdit.text()
    self.undsPath = self.undsFileOptions.lineEdit.text()

  def cancelConfigs(self):
    self.close()

  def saveConfigs(self):
    try:
        paths = {"cloc": self.clocPath, "unds": self.undsPath}
        process = subprocess.Popen([self.clocPath, self.clocPath])
        if process.returncode != False:
            with open(self.configPath, 'w') as outfile:
              json.dump(paths, outfile, indent = 2)
            self.close()
        process.wait()
    except Exception:
        print("Please make sure if the cloc and understand works right.")
