#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#pathLists.py
#Defines lists which will be used on the GUI and main to synchronize
#Created: ssia@keystonestrategy.com
#Last Updated: 11/16/2016

def returnPaths():
  pathList = ["rampout", "diffout", "inputFolder", "langDef", "undpath", "strings", "depout", "profout", "vizout"]
  auxPathList = ["tools", "code", "thirdparty", "deployments"]
  return (pathList, auxPathList)