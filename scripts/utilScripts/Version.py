#Version.py
#Created 01/31/2017
#hiroki.moto.pro@outlook.com

#Defines the Version class
#Contains init, validity check and comparator functions
#The version class is used to create a list of versions
#That is used in CKProject

import datetime
import os

class Version:
  "Version Class"
  def __init__(self, id, folder, date, tags):
    #Write code here to check that date, id, folder, tags are valid.
    self.id = id
    self.folder = folder
    self.date = date
    self.tags = tags
    self.error = 0
    if self.id == "Not Defined" or self.id == "":
      self.error += 1
    if not os.path.exists(folder):
      self.error += 1
    self.isDateValid(date)
    self.isTagsValid(tags)

  #Comparator check. Returns true if self and Version have the same versionID  
  def sameID(self, Version):
    pass

  def isDateValid(self, date):
    minyear = 1900
    maxyear = datetime.date.today().year
    dateparts = date.split("/")
    try:
      if len(dateparts) == 1:
        if int(dateparts[0]) > maxyear or int(dateparts[0]) < minyear:
          self.error += 1
          return
      elif len(dateparts) == 3:
        if int(dateparts[2]) > maxyear or int(dateparts[2]) < minyear:
          self.error += 1
          return
      else:
        self.error += 1
        return
    except Exception:
      self.error += 1

  def isTagsValid(self, tags):
    for tag in tags:
      if tags[tag] == "Not Defined" or tags[tag] == "":
        self.error += 1
        return
