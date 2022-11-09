#!/usr/bin/python3
# -*- coding: utf-8 -*-

############################
#CodeKey GUI
# ssia@keystonestrategy.com
#Created 11/15/2016
#
# MainWindow and Docking functionality for CodeKey
############################

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from guiScripts.CompareForm import PathOptions
from guiScripts.CompareForm import FileOptions

class NewProjectDialog(QWidget):
  def __init__(self):
    super().__init__()

    self.initUI()

  def initUI(self):
    self.sizeAndCenter()
    self.setWindowTitle("CodeKey Dev Version")
    self.setWindowIcon(QIcon("qIcon.png"))
    self.projectName = "test_diffs"
    self.projectLocation = r"/Volumes/Works/Works/Solomon/tests"
    self.inputFolder = r"/Volumes/Works/Works/Solomon/tests/test_diffs/inputs"
    self.clocLocation = r"/Volumes/Works/Works/Solomon/CrimsonCodeAnalysis/tools/cloc/lib/cloc"
    self.undLocation = r"/Volumes/Works/Works/Solomon/CrimsonCodeAnalysis/tools/scitools/bin/macosx/und"

    #Main Window is a central forms that keeps changing
    self.gridLayout = QGridLayout()
    self.gridLayout.setColumnMinimumWidth(0,250)
    self.gridLayout.setColumnMinimumWidth(1,400)
    self.setLayout(self.gridLayout)

    #In the future, we will be asking to add language definitions and copyright strings.
    self.instructions = QTextEdit("When starting a project you need to do three things:<br> \
      1. Create a project file. Browse to the folder you want to place your Project Database in.<br> \
      2. Give your Project a directory name and a location for the directory.<br> \
      3. Then give your Project a location of its input folder (Optional)<br> \
      4. Then there are understand and cloc exe paths which should be done at installation time. <br>\
      5. Warning! At the end of it the folders are created but I haven't tied comparisons and versions folders in yet.")
    self.instructions.setReadOnly(True)
    self.gridLayout.addWidget(self.instructions, 0, 0)

    self.formLayout = QFormLayout()
    self.projectNameForm = QLineEdit(self.projectName)
    self.formLayout.addRow(QLabel("Name: "), self.projectNameForm)

    self.projectLocationForm = PathOptions("Project Location:", self.projectLocation)
    self.formLayout.addRow(self.projectLocationForm.label, self.projectLocationForm.hbox)
    self.inputFolderForm = PathOptions("Input Folder:", self.inputFolder)
    self.formLayout.addRow(self.inputFolderForm.label, self.inputFolderForm.hbox)
    self.clocLocationForm = FileOptions("Cloc Location:", self.clocLocation)
    self.formLayout.addRow(self.clocLocationForm.label, self.clocLocationForm.hbox)
    self.undLocationForm = FileOptions("Path Location:", self.undLocation)
    self.formLayout.addRow(self.undLocationForm.label, self.undLocationForm.hbox)
    self.gridLayout.addLayout(self.formLayout, 0 , 1)

    self.projectNameForm.textChanged.connect(self.pathsUpdate)
    self.projectLocationForm.lineEdit.textChanged.connect(self.pathsUpdate)
    self.inputFolderForm.lineEdit.textChanged.connect(self.pathsUpdate)
    self.clocLocationForm.lineEdit.textChanged.connect(self.pathsUpdate)
    self.undLocationForm.lineEdit.textChanged.connect(self.pathsUpdate)

    #box to put the different folders
    self.imports = []

    self.importsVboxLayout = QVBoxLayout()
    self.importsButton = QPushButton("Specify Versions")
    #self.importsButton.clicked.connect(lambda: self.addNewImports())

    self.makeButtonsHboxLayout()

    #Save upon closing
    self.setMinimumSize(QSize(300, 200))
    self.show()

  def makeButtonsHboxLayout(self):
    self.hboxLayout = QHBoxLayout()

    cancelButton = QPushButton("Cancel")
    cancelButton.clicked.connect(lambda: self.close())
    self.hboxLayout.addWidget(cancelButton)
    self.hboxLayout.addStretch(1)

    self.backButton = QPushButton("<Back")
    self.backButton.setEnabled(False)
    self.hboxLayout.addWidget(self.backButton)
    self.backButton.clicked.connect(self.transitionBack)

    self.nextButton = QPushButton("Next>")
    self.hboxLayout.addWidget(self.nextButton)
    self.nextButton.clicked.connect(lambda: self.transitionNext())
    self.gridLayout.addLayout(self.hboxLayout, 1, 0, 1, 2)

    self.doneButton = QPushButton("Done")
    self.doneHBoxLayout = QHBoxLayout()
    self.doneHBoxLayout.addStretch(1)
    self.doneHBoxLayout.addWidget(self.importsButton)
    self.importsVboxLayout.addStretch(1)
    self.importsVboxLayout.addLayout(self.doneHBoxLayout)

  def transitionBack(self):
    print("We haven't implemented this function yet. LOL")

  #Currently transitioning from the input section to the other section.
  def transitionNext(self):

    #Set the text in line edit ot something different
    self.instructions.setText("The second part of a project is setting the folders to compare.<br> \
      Try adding at least one, with the identification and the folder path.<br> \
      Additionally, you should think about ading the date, and tags which will help in result presentation.<br> \
      You can always do this later by selecting 'specify versions' from the config menu")

    self.clearLayout(self.formLayout)
    self.gridLayout.addLayout(self.importsVboxLayout, 0, 1)

    #Change the buttons
    self.nextButton.deleteLater()
    self.hboxLayout.addWidget(self.doneButton)
    self.backButton.setEnabled(True)

    #Remove the form on the right and replace it with a QGrid layout
    #which we will populate with versions from the existing versions list.

  def clearLayout(self, layout):
    if layout is not None:
      while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
          widget.deleteLater()
        else:
          self.clearLayout(item.layout())

  def pathsUpdate(self):
    self.projectName = self.projectNameForm.text()
    self.projectLocation = self.projectLocationForm.lineEdit.text()
    self.inputFolder = self.inputFolderForm.lineEdit.text()
    self.clocLocation = self.clocLocationForm.lineEdit.text()
    self.undLocation = self.undLocationForm.lineEdit.text()

  def sizeAndCenter(self):
    self.resize(600,400)
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())
