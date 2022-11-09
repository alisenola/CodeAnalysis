#!/usr/bin/python3
# -*- coding: utf-8 -*-

############################
#CodeKey GUI
# ssia@keystonestrategy.com
#Created 11/15/2016
#
# MainWindow and Docking functionality for CodeKey
############################

import json
import os
import sys
import subprocess
import guiScripts.ioHelper as ioHelper
from guiScripts.CompareForm import *
from guiScripts.CentralWidget import CentralWidget
from guiScripts.defaultParams import *
from guiScripts.NewProjectDialog import NewProjectDialog
from guiScripts.SpecifyVersionsDialog import SpecifyVersionsDialog
from guiScripts.InstallConfigDialog import InstallConfigDialog
from utilScripts.CKProject import CKProject
from utilScripts.staticvars import *
from utilScripts.util import *
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from queue import Queue
from summaryScripts.summary import getSummary
from sys import platform as _platform


class CodeKeyMain(QMainWindow):
  "Main Window for the CodeKey Application"
  comp_data = defaultComps()
  version_data = defaultVersions()
  comparisonsFile = ""
  versionsFile = ""

  if (DEBUG):
    comparisonsFile = DEFAULT_COMPARISONS_FILE
    versionsFile = DEFAULT_VERSIONS_FILE
    #print( "We are taking data from stock comparisons file: \n", comparisonsFile )
    with open(comparisonsFile) as data_file:
      comp_data = json.load(data_file)
    with open(versionsFile) as data_file:
      version_data = json.load(data_file)["versions"]

  def __init__(self):
    super().__init__()

    if _platform == "linux" or _platform == "linux2":
      print("Linux")
    elif _platform == "darwin":
      print("Mac OS")
    elif _platform == "win32":
      print("Windows")

    self.CKProject = None
    self.process = None
    self.initActions()
    self.initUI()

  def initActions(self):
    self.createNewAction()
    self.createLoadAction()
    self.createExitAction()
    self.createRunAction()
    self.createSpecifyVersions()
    self.createSaveAction()
    self.createSummarizeAction()
    self.currentFile = "/home"

  def initUI(self):
        #Create codeKeyGUI
    self.createCentralWidget()

    self.addToolBars()
    self.addMenuBar()
    self.addConsoleDock()
    #self.addLeftDock()

    self.sizeAndCenter()

    self.statusBar().showMessage('Ready')

    self.setWindowTitle('CodeKey Dev Version')
    self.setWindowIcon(QIcon(ICONPATH+'qIcon.png'))
    self.show()

    #Check if configs have been set
    currentpath = os.path.realpath(__file__)
    sourcepath = str(Path(currentpath).parent.parent)
    self.configFilePath = os.path.join(sourcepath, "configs.json");
    if os.path.exists(self.configFilePath):
      print(sourcepath)
    else:
      self.installConfigDialog = InstallConfigDialog(self.configFilePath)

  def createCentralWidget(self):
    self.tab = CentralWidget()
    self.setCentralWidget(self.tab)

  def sizeAndCenter(self):
    self.resize(1200,840)
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())

  def createLoadAction(self):
    self.loadAction = QAction(QIcon(ICONPATH+'open.jpg'), '&Load', self) #Exit   
    self.loadAction.setShortcut('Ctrl+O')
    self.loadAction.setStatusTip('Load Config File') #On The status bar
    self.loadAction.triggered.connect(self.loadCompJSON)

  def createNewAction(self):
    self.newAction = QAction(QIcon(ICONPATH+'new.png'), '&New', self) #Exit   
    self.newAction.setShortcut('Ctrl+N')
    self.newAction.setStatusTip('New Project...') #On The status bar
    self.newAction.triggered.connect(self.newProject)

  def createExitAction(self):
    self.exitAction = QAction(QIcon(ICONPATH+'exit24.png'), '&Exit', self) #Exit   
    self.exitAction.setShortcut('Ctrl+Q')
    self.exitAction.setStatusTip('Exit application') #On The status bar
    self.exitAction.triggered.connect(self.quitApplication)

  def createSpecifyVersions(self):
    self.sfversionAction = QAction(QIcon(ICONPATH+'new.png'), '&Specify Version', self) # Specify Version
    self.sfversionAction.setShortcut('Ctrl+V')
    self.sfversionAction.setStatusTip('Specify version...')
    self.sfversionAction.triggered.connect(self.openSpecifyVersionsDialog)

  def createRunAction(self):
    self.runAction = QAction(QIcon(ICONPATH+'run.png'), '&Run', self) #Run   
    self.runAction.setShortcut('Ctrl+R')
    self.runAction.setStatusTip('Run application') #On The status bar
    self.runAction.triggered.connect(self.runProg)

  def createSummarizeAction(self):
    self.sumAction = QAction(QIcon(ICONPATH+'understand_64.png'), '&Summarize', self) #Run   
    self.sumAction.setShortcut('Ctrl+M')
    self.sumAction.setStatusTip('Summarize Results') #On The status bar
    self.sumAction.triggered.connect(self.displaySummary)

  def createSaveAction(self):
    self.saveAction = QAction(QIcon(ICONPATH+'save.jpg'), '&Save', self) #Run   
    self.saveAction.setShortcut('Ctrl+S')
    self.saveAction.setStatusTip('Save Config File') #On The status bar
    #self.saveAction.triggered.connect(self.CKProject.exportComparisonsToJSON(None))

  @pyqtSlot(str)
  def append_text(self, text):
    self.console.moveCursor(QTextCursor.End)
    self.console.insertPlainText(text)

  def addToolBars(self):
    toolbar = self.addToolBar('Main')
    toolbar.addAction(self.newAction)
    toolbar.addAction(self.loadAction)
    toolbar.addAction(self.saveAction)
    toolbar.addAction(self.sfversionAction)
    toolbar.addAction(self.runAction)
    toolbar.addAction(self.sumAction)
    toolbar.addAction(self.exitAction)

  def addMenuBar(self):
    menubar = self.menuBar()
    fileMenu = menubar.addMenu('&File')
    fileMenu.addAction(self.newAction)
    fileMenu.addAction(self.loadAction)
    fileMenu.addAction(self.exitAction)
    fileMenu.addAction(self.saveAction)
    fileMenu.addAction(self.sumAction)
    runMenu = menubar.addMenu('&Run')
    runMenu.addAction(self.runAction)
    runMenu = menubar.addMenu('&Edit')
    runMenu = menubar.addMenu('&View')
    runMenu = menubar.addMenu('&Project')
    runMenu = menubar.addMenu('&Reports')
    runMenu = menubar.addMenu('&Metrics')
    runMenu = menubar.addMenu('&Graphs')
    runMenu = menubar.addMenu('&Tools')
    runMenu = menubar.addMenu('&Window')
    runMenu = menubar.addMenu('&Help')
    configMenu = menubar.addMenu('&Config')
    configMenu.addAction(self.sfversionAction)

  def addConsoleDock(self):
    self.consoleDock = QDockWidget("Console Output", self)
    self.console = QTextEdit()
    self.consoleDock.setWidget(self.console)
    self.addDockWidget(Qt.BottomDockWidgetArea, self.consoleDock)

  def closeEvent(self, event):
    if self.process.poll() == None:
      reply = QMessageBox.question(self, 'Exit CodeKey',
        "Are you sure you want to quit?", QMessageBox.Yes |
        QMessageBox.No, QMessageBox.No)

      if reply == QMessageBox.Yes:
        if self.process.poll() == None:
          self.process.kill()
        event.accept()
      else:
        event.ignore()
    else:
      event.accept()
      

  def displaySummary(self):
    self.sumTask = {
      "type": "Summary",
      "run": "True",
      "style": "diff",
      "granularity": "foobar",
      "extensions": "foobar",
      "rowOfInterest": "Percentage"
    }

    ( self.categories, self.summaryList ) = getSummary(self.comp_data["paths"], self.version_data, self.sumTask)
    #Given a List of 3 tables, choose the first one. And then start printing it

    self.tab.createSummaries(self.categories, self.summaryList)

  #Opens a new project.
  def newProject(self):
    #Creates a popup window where you type in input folder, language definitions
    #TODO: Copyright strings?
    #TODO: Cloc and Understandpath are the remaining optiosn which will be done in the future
    #TODO: Done during installation.
    self.newProjectDialog = NewProjectDialog()
    self.newProjectDialog.doneButton.clicked.connect(lambda: self.completeNewProjectDialog() )
    self.newProjectDialog.importsButton.clicked.connect(lambda: self.openSpecifyVersionsDialog() )

  def completeNewProjectDialog(self):
    try:
      print("In the future we will add an \"Directory already exists: Overwrite?\" message.")
      self.projFolder = os.path.join(self.newProjectDialog.projectLocation, self.newProjectDialog.projectName)
      print( "Creating project: ", self.projFolder )
      print( "Specified input folder: ", self.newProjectDialog.inputFolder )

      self.CKProject = CKProject( self.newProjectDialog.projectLocation,
        self.newProjectDialog.projectName,
        self.newProjectDialog.inputFolder,
        self.newProjectDialog.clocLocation,
        self.newProjectDialog.undLocation, GUIMODE )
      
      if (self.CKProject.error == 1):
        print("Project construction is none!")

      self.newProjectDialog.close()
      
      print("Creating sample comparisons and versions file based on scripted template and projects etc input.")
      self.CKProject.createNewProject()

      print("Loading comparisons and versions data.")
      self.CKProject.readVersionsFromJSON(None)
      self.CKProject.loadComparisonsFromJSON(None)
      self.addLeftDock()

      #Connect actions with CKProject after CKProject has been created
      self.saveAction.triggered.connect(self.CKProject.exportComparisonsToJSON)
      #Save input folder in comparisonsFile if possible.
    except Exception as e:
      print(str(e))

  def openSpecifyVersionsDialog(self):
    #Creates a popup window where you type in input folder, language definitions
    #TODO: Copyright strings?
    #TODO: Cloc and Understandpath are the remaining optiosn which will be done in the future
    #TODO: Done during installation.
    if self.CKProject == None:
      self.CKProject = CKProject( self.newProjectDialog.projectLocation,
                                  self.newProjectDialog.projectName,
                                  self.newProjectDialog.inputFolder,
                                  GUIMODE )
      self.specifyVersionsDialog = SpecifyVersionsDialog(self.CKProject)
    else:
      self.specifyVersionsDialog = SpecifyVersionsDialog(self.CKProject)

  def runProg(self):
    exepath = "/Volumes/Works/Works/Solomon/CrimsonCodeAnalysis/scripts/build/exe.macosx-10.6-intel-3.4/main"
    try:
      assert(os.path.exists(exepath))
      assert(os.path.exists(self.versionsFile))
      assert(os.path.exists(self.comparisonsFile))
      self.process = subprocess.Popen([exepath, "/Volumes/Works/Works/Solomon/tests", "test_diffs"])
      while True:
        output = self.process.stdout.readline()
        output = output.decode('UTF-8')
        if output == "" and self.process.poll() is not None:
          break
        if output:
          print(output.strip())
        rc = self.process.poll()
    except Exception as e:
      print("Oops, check your paths to main: Path does not exist: " + str(e))

    return

  def loadCompJSON(self):
    #Make it so its just loading JSON
    #We are going to deprecate this.
    fname = QFileDialog.getOpenFileName(self, "Load Config File", "/home/", "JSON (*.json)")

    if fname[0]:
      self.comparisonsFile = fname[0]
      with open(self.comparisonsFile) as data_file:
        self.comp_data = json.load(data_file)
        self.updateCompWidget()

  def updateCompWidget(self):
    self.tasksForm = TasksForm(self.CKProject.Comparisons)
    self.tasksDock.setWidget(self.tasksForm)

    self.compForm = CompForm(self.CKProject.Comparisons, self.CKProject.versions)
    self.compDock.setWidget(self.compForm)
    self.paramsForm = ParamsForm(self.CKProject.Comparisons)
    self.paramsDock.setWidget(self.paramsForm)

    self.tasksForm.setMinimumSize(QSize(300,0))
    self.compForm.setMinimumSize(QSize(300,0))
    self.paramsForm.setMinimumSize(QSize(300,0))

    self.tasksForm.submitButton.clicked.connect( self.CKProject.exportComparisonsToJSON(None) )
    self.compForm.submitButton.clicked.connect( self.CKProject.exportComparisonsToJSON(None) )
    self.paramsForm.submitButton.clicked.connect( self.CKProject.exportComparisonsToJSON(None) )

  def addLeftDock(self):
    self.leftDockList = []
    self.tasksDock = QDockWidget("Tasks Form", self)
    self.compDock = QDockWidget("Compare Form", self)
    self.paramsDock = QDockWidget("Params Form", self)

    self.addDockWidget(Qt.LeftDockWidgetArea, self.tasksDock)
    self.leftDockList.append(self.tasksDock)
    self.leftDockList.append(self.tasksDock)
    self.addDockWidget(Qt.LeftDockWidgetArea, self.compDock)
    self.leftDockList.append(self.compDock)
    self.addDockWidget(Qt.LeftDockWidgetArea, self.paramsDock)
    self.leftDockList.append(self.paramsDock)
    self.tabifyDockWidget(self.tasksDock,self.compDock)
    self.tabifyDockWidget(self.tasksDock,self.paramsDock)

    if self.CKProject != None:
      self.updateCompWidget()

  def quitApplication(self):
    if self.process != None:
      reply = QMessageBox.question(self, 'Exit CodeKey',
        "Are you sure you want to quit?", QMessageBox.Yes |
        QMessageBox.No, QMessageBox.No)

      if reply == QMessageBox.Yes:
        if self.process.poll() == None:
          self.process.kill()
        qApp.quit()
    else:
      qApp.quit()

if __name__ == '__main__':

  app = QApplication(sys.argv)
  ex = CodeKeyMain()
    
  queue = Queue()
  sys.stdout = ioHelper.WriteStream(queue)
  sys.stderr = ioHelper.WriteStream(queue)
  my_receiver = ioHelper.MyReceiver(queue)

  thread = QThread()
  my_receiver.mysignal.connect(ex.append_text)
  my_receiver.moveToThread(thread)
  thread.started.connect(my_receiver.run)
  thread.start()

  sys.exit(app.exec_())
