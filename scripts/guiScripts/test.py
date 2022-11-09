from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QWidget,
    QDesktopWidget, QPushButton, QMessageBox,
    QMainWindow, QAction, qApp, QTextEdit, QSlider,
    QLCDNumber, QVBoxLayout, QHBoxLayout, QGridLayout,
    QFileDialog)

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Window(QWidget):
  def __init__(self, val):
    QWidget.__init__(self)
    mygroupbox = QGroupBox("this is my groupbox")
    myform = QFormLayout()
    labellist = []
    combolist = []
    for i in range(val):
      labellist.append(QLabel("mylabel"))
      combolist.append(QComboBox())
      myform.addRow(labellist[i],combolist[i])
    mygroupbox.setLayout(myform)
    scroll = QScrollArea()
    scroll.setWidget(mygroupbox)
    scroll.setWidgetResizable(True)
    # scroll.setFixedHeight(200)

    layout = QVBoxLayout(self)
    layout.addWidget(scroll)

    # self.compareDock = QDockWidget("Compare Form", self)
    # self.tasksForm = tasksForm.tasksForm()
    # self.compareDock.setWidget(self.tasksForm)
    # self.addDockWidget(Qt.LeftDockWidgetArea, self.compareDock)

if __name__ == "__main__":
  import sys
  app = QApplication(sys.argv)
  window = Window(25)
  window.setGeometry(500, 300, 300, 400)
  window.show()
  sys.exit(app.exec_())