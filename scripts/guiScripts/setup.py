# -*- coding: utf-8 -*-

# A simple setup script to create an executable using PyQt4. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# PyQt4app.py is a very simple type of PyQt4 application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
  base = "Win32GUI"

includefiles = [".", "guiScripts/README.txt", "guiScripts/CHANGELOG.txt", "guiScripts/exit24.png", "guiScripts/keystone.png",
  "guiScripts/open.jpg", "guiScripts/qIcon.png", "guiScripts/run.png", "guiScripts/save.jpg", "guiScripts/understand_64.png"]
excludes = ["Tkinter"]
includes = ["atexit"]

options = {
  "build_exe": {
    "includes": includes,
    "include_files": includefiles,
    "excludes": excludes
   }
}

executables = [
  Executable("guiScripts/CodeKeyApp.py", base = base)
]

setup(name = "simple_CodeKey",
      version = "0.1",
      description = "Sample CodeKey script",
      options = options,
      executables = executables
      )
