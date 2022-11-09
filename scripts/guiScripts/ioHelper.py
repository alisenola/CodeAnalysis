#!/usr/bin/python3
# -*- coding: utf-8 -*-

########################################
#CodeKey GUI Misc Helpers
# ssia@keystonestrategy.com
#Created 11/15/2016
#
# Additional Methods for dealing with IO
#########################################

from PyQt5.QtCore import *

class WriteStream(object):
  def __init__(self, queue):
    self.queue = queue

  def write(self, text):
    self.queue.put(text)

  def flush(self):
    return

class MyReceiver(QObject):
  mysignal = pyqtSignal(str)

  def __init__(self, queue, *args, **kwargs):
    QObject.__init__(self, *args, **kwargs)
    self.queue = queue

  @pyqtSlot()
  def run(self):
    while True:
      text = self.queue.get()
      self.mysignal.emit(text)
