#!/usr/bin/python3
# -*- coding: utf-8 -*-

############################
#Default Params py
# ssia@keystonestrategy.com
#Created 11/15/2016
#
# Contains Default comp_data and default params_data
############################

def defaultComps():
  comp_data = {
    "paths": {
      "rampout": "../output_datasets/06_ramp_down_output/",
      "diffout": "/Volumes/Works/Works/Solomon/CrimsonCodeAnalysis/output_datasets/01_diff_output/",
      "inputFolder": "",
      "langDef": "../auxiliary_datasets/cloc-lang-def.txt",
      "undpath": "../../../../../../Program Files/SciTools/bin/pc-win64/und.exe",
      "strings": "../auxiliary_datasets/metaStrings.json",
      "depout": "../output_datasets/02_deptest",
      "profout": "../output_datasets/03_profiler/",
      "vizout": "../output_datasets/08_viz_output"
    },
    "parameters": [
      ("Placeholder" , 0),
      ("Foobar" , 1)
    ],
    "auxpaths": {
      "tools":  "../auxiliary_datasets/tools.csv",
      "code":  "../auxiliary_datasets/code.csv",
      "nonCode":  "../auxiliary_datasets/nonCode.csv",
      "thirdparty":  "../auxiliary_datasets/thirdparty.csv",
      "deployments": "../auxiliary_datasets/deployments.csv",
      "exclude": "../auxiliary_datasets/exclude.csv"  
    },
    "tasks": [
      {
        "type": "Profiler",
        "run": "False"
      },
      {
        "type": "MetaProfiler",
        "run": "False"
      },
      {
        "type": "DiagnoseDiffs",
        "run": "False"
      },
      {
        "type": "ClocDiffs",
        "run": "False"
      },
      {
        "type": "Diffs",
        "counter": "1/1",
        "run": "False"
      },
      {
        "type": "GenUdb",
        "lang": "C++",
        "run": "False"
      },
      {
        "type": "GenDeps",
        "run": "False"
      },
      {
        "type": "AnalyzeDiffs",
        "thresholds": [100,50],
        "run": "False"
      },
      {
        "type": "RampDownCloc",
        "run": "False"
      },
      {
        "type": "RampDownCurve",
        "run": "False"
      },
      {
        "type": "RampDownDeps",
        "run": "False"
      },
      {
        "type": "Viz",
        "run": "False"
      },
      {
        "type": "Summary",
        "run": "False",
        "style": "diff",
        "rowOfInterest": "Percentage"
      }
    ],
    "comparisons": [
      {
        "fromID" : "MWtools",
        "toID" : "WaWtools"
      },
      {
        "fromID" : "MWtools",
        "toID" : "BOtools"
      },
      {
        "fromID" : "MWtools",
        "toID" : "BO2tools"
      },
      {
        "fromID" : "MWtools",
        "toID" : "BO3tools"
      }
    ]
  }

  return comp_data

def defaultComp():
  comp =  {
    "fromID" : "Not Defined",
    "toID" : "Not Defined",
    "params" : [
      {}
    ]
  }
  return comp

def defaultTask():
  task = {
    "type": "Profiler",
    "run": "False"
  }
  return task

def defaultVersions():
  versions =  [
    {
      "id" : "Not Defined",
      "studio" : "Not Defined",
      "date" : "Not Defined",
      "check": "Not Defined",
      "category": "Not Defined",
      "folder" : "Not Defined"
    },  
    {
      "id" : "MW2src_sp",
      "studio" : "Infinity Ward",
      "date" : "2007",
      "check": "alternate",
      "category": "engine",
      "folder" : "/media/ks-magenta/data/iw4-depot/iw4/code_source_sp-gold"
    },
    {
      "id" : "Testv5",
      "studio" : "Oculus",
      "date" : "2012",
      "check": "Not Defined",
      "category": "Not Defined",
      "folder" : "v5"
    },
    {
      "id" : "Testv6",
      "studio" : "Oculus",
      "date" : "2013",
      "check": "Not Defined",
      "category": "Not Defined",
      "folder" : "v6"
    },
    {
      "id" : "MW2src_ps3",
      "studio" : "Infinity Ward",
      "date" : "2007",
      "check": "alternate",
      "category": "engine",
      "folder" : "/media/ks-magenta/data/iw4-depot/iw4/code_source_ps3"
    },
    {
      "id" : "MW2src_dw",
      "studio" : "Infinity Ward",
      "date" : "2007",
      "check": "alternate",
      "category": "engine",
      "folder" : "/media/ks-magenta/data/iw4-depot/iw4/code_source_dw"
    },
    {
      "id" : "MW",
      "studio" : "Infinity Ward",
      "date" : "2007",
      "category": "game",
      "folder" : "/media/ks-magenta/data/cod3-depot/cod3/cod3"
    },
    {
      "id" : "MWsrc",
      "studio" : "Infinity Ward",
      "date" : "2007",
      "category": "engine",
      "folder" : "/media/ks-magenta/data/cod3-depot/cod3/cod3src"
    },
    {
      "id" : "MWmap",
      "studio" : "Infinity Ward",
      "date" : "2007",
      "check": "alternate",
      "folder" : "/media/ks-magenta/data/cod3-depot/cod3/cod3/map_source"
    },
    {
      "id" : "MWsrc-console",
      "studio" : "Infinity Ward",
      "date" : "2007",
      "check": "alternate",
      "category": "engine",
      "folder" : "/media/ks-magenta/data/cod3-depot/cod3-console/cod3src"
    },
    {
      "id" : "MWsrc-linux",
      "studio" : "Infinity Ward",
      "date" : "2007",
      "check": "alternate",
      "category": "engine",
      "folder" : "/media/ks-magenta/data/cod3-depot/cod3-linux/cod3src"
    },
    {
      "id" : "MWtools",
      "studio" : "Infinity Ward",
      "date" : "2007",
      "category": "tools",
      "folder" : "/media/ks-magenta/data/cod3-depot/cod3-outgoing/iw-core/tools_source"
    },
    {
      "id" : "WaW",
      "studio" : "Treyarch",
      "date" : "2008",
      "category": "game",
      "folder" : "/media/ks-maroon/data/Treyarch/depot/cod5/cod/cod5"
    },
    {
      "id" : "WaWsrc",
      "studio" : "Treyarch",
      "date" : "2008",
      "category": "engine",
      "folder" : "/media/ks-maroon/data/Treyarch/depot/cod5/cod/codsrc"
    },
    {
      "id" : "WaWtools",
      "studio" : "Treyarch",
      "date" : "2008",
      "category": "tools",
      "folder" : "/media/ks-maroon/data/Treyarch/depot/cod5/iw-core/tools_source"
    },
    {
      "id" : "BO",
      "studio" : "Treyarch",
      "date" : "2010",
      "category": "game",
      "folder" : "/media/ks-maroon/data/Treyarch/keystone-t5/depot/wii/t5/cod/t5"
    },
    {
      "id" : "BOsrc",
      "studio" : "Treyarch",
      "date" : "2010",
      "category": "engine",
      "folder" : "/media/ks-maroon/data/Treyarch/keystone-t5/depot/wii/t5/cod/codsrc"
    },
    {
      "id" : "BOtools",
      "studio" : "Treyarch",
      "date" : "2010",
      "category": "tools",
      "folder" : "/media/ks-maroon/data/Treyarch/keystone-t5/depot/wii/t5/iw-core/tools_source"
    },
    {
      "id" : "BO2",
      "studio" : "Treyarch",
      "date" : "2012",
      "category": "game",
      "folder" : "/media/ks-maroon/data/Treyarch/t6/main/game"
    },
    {
      "id" : "BO2src",
      "studio" : "Treyarch",
      "date" : "2012",
      "category": "engine",
      "folder" : "/media/ks-maroon/data/Treyarch/t6/main/code"
    },
    {
      "id" : "BO2tools",
      "studio" : "Treyarch",
      "date" : "2012",
      "category": "tools",
      "folder" : "/media/ks-maroon/data/Treyarch/t6/main/iw-core/tools_source"
    },
    {
      "id" : "BO3",
      "studio" : "Treyarch",
      "date" : "2015",
      "category": "game",
      "folder" : "/media/ks-maroon/data/Treyarch/t7/main/game"
    },
    {
      "id" : "BO3src",
      "studio" : "Treyarch",
      "date" : "2015",
      "category": "engine",
      "folder" : "/media/ks-maroon/data/Treyarch/t7/main/code"
    },
    {
      "id" : "BO3tools",
      "studio" : "Treyarch",
      "date" : "2015",
      "category": "tools",
      "folder" : "/media/ks-maroon/data/Treyarch/t7/main/code/tools"
    },
    {
      "id" : "MW2",
      "studio" : "Infinity Ward",
      "date" : "2009",
      "category": "game",
      "folder" : "/media/ks-magenta/data/iw4-depot/iw4/game"
    },
    {
      "id" : "MW2map",
      "studio" : "Infinity Ward",
      "date" : "2009",
      "category": "map",
      "folder" : "/media/ks-magenta/data/iw4-depot/iw4/map_source"
    },
    {
      "id" : "MW2src",
      "studio" : "Infinity Ward",
      "date" : "2009",
      "category": "engine",
      "folder" : "/media/ks-magenta/data/iw4-depot/iw4/code_source"
    },
    {
      "id" : "MW2tools",
      "studio" : "Infinity Ward",
      "date" : "2009",
      "category": "tools",
      "folder" : "UNKNOWN"
    },
    {
      "id" : "MW3",
      "studio" : "Infinity Ward",
      "date" : "2011",
      "category": "game",
      "folder" : "/media/ks-magenta/data/iw5-depot/iw5/game"
    },
    {
      "id" : "MW3-release",
      "studio" : "Infinity Ward",
      "date" : "2011",
      "check": "alternate",
      "category": "game",
      "folder" : "/media/ks-magenta/data/iw5-depot/iw5-release/game"
    },
    {
      "id" : "MW3src",
      "studio" : "Infinity Ward",
      "date" : "2011",
      "category": "engine",
      "folder" : "/media/ks-magenta/data/iw5-depot/iw5/code_source"
    },
    {
      "id" : "MW3src-release",
      "studio" : "Infinity Ward",
      "date" : "2011",
      "check": "alternate",
      "category": "engine",
      "folder" : "/media/ks-magenta/data/iw5-depot/iw5-release/code_source"
    },
    {
      "id" : "MW3tools",
      "studio" : "Infinity Ward",
      "date" : "2011",
      "category": "tools",
      "folder" : "UNKNOWN"
    },
    {
      "id" : "Ghosts",
      "studio" : "Infinity Ward",
      "date" : "2013",
      "category": "game",
      "folder" : "/media/ks-magenta/analysis/iw6-depot/iw6/game"
    },
    {
      "id" : "Ghostssmap",
      "studio" : "Infinity Ward",
      "date" : "2013",
      "category": "map",
      "folder" : "/media/ks-magenta/analysis/iw6-depot/iw6/map_source"
    },
    {
      "id" : "Ghostssrc",
      "studio" : "Infinity Ward",
      "date" : "2013",
      "category": "engine",
      "folder" : "/media/ks-magenta/analysis/iw6-depot/iw6/code_source"
    },
    {
      "id" : "Ghoststools",
      "studio" : "Infinity Ward",
      "date" : "2013",
      "category": "tools",
      "folder" : "UNKNOWN"
    },
    {
      "id" : "AW",
      "studio" : "Infinity Ward",
      "date" : "2014",
      "category": "game",
      "folder" : "UNKNOWN"
    }
  ]
  return versions
