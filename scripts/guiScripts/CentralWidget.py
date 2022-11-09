#!/usr/bin/python3
# -*- coding: utf-8 -*-

############################
#CodeKey GUI Central Widget
# ssia@keystonestrategy.com
#Created 11/15/2016
#
# Central Widget experimentation
############################

import guiScripts.CentralWidget
import guiScripts.ioHelper
from guiScripts.CompareForm import *
from guiScripts.defaultParams import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from summaryScripts.summary import getSummary
from utilScripts.util import *


class Communicate(QObject):
  clickedApp = pyqtSignal()


class CentralWidget(QTabWidget):
    
  def __init__(self):
    super().__init__()

    self.initUI()

  def initUI(self):
    self.createStartTable()
    self.createFromTabList()

  def createStartTable(self):
    self.tabList = []
    table = QTableWidget()
    table.setRowCount(2)
    table.setColumnCount(4)
    table.setItem(0,0, QTableWidgetItem("This"))
    table.setItem(0,1, QTableWidgetItem("is"))
    table.setItem(0,2, QTableWidgetItem("a"))
    table.setItem(0,3, QTableWidgetItem("Placeholder"))
    table.setItem(1,0, QTableWidgetItem("until"))
    table.setItem(1,1, QTableWidgetItem("we"))
    table.setItem(1,2, QTableWidgetItem("get"))
    table.setItem(1,3, QTableWidgetItem("data"))
    self.tabList.append(["Default Table", table])

  def createFromTabList(self):
    self.clear()
    for tab in self.tabList:
      self.addTab(tab[1], tab[0])

  def createSummaries(self, categories, summaryList):
    self.tabList = []
    for (i, slist) in enumerate(summaryList):
      table = QTableWidget()
      tableRow = len(slist) - 1
      tableCol = len(slist[0]) 
      table.setRowCount(tableRow)
      table.setColumnCount(tableCol)
      table.setHorizontalHeaderLabels(slist[0])

      for row in range(tableRow):
        for col in range(tableCol):
          table.setItem(row,col, QTableWidgetItem(str(slist[row + 1][col])))

      self.tabList.append([categories[i] , table])

    self.createFromTabList()
