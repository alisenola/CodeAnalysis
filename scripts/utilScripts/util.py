#Utility Read Scripts
#Created: mshakir@keystonestrategy.com
#Updated: ssia@keystonestrategy.com
#Last Updated: 08/15/2016

import collections
import csv
import os
import re
import shutil
import sys
import time

def copyFile(src, dest):
  try:
    shutil.copy(src, dest)
  # eg. src and dest are the same file
  except shutil.Error as e:
    print('Error: %s' % e)
  # eg. source or destination doesn't exist
  except IOError as e:
    print('Error: %s' % e.strerror)

#Prettily prints a 2D list
def prettyPrint(matrix):
  s = [[str(e) for e in row] for row in matrix]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print('\n'.join(table))

#Prints the files which are not found
def missPrint(missfiles):
  if missfiles:
    print()
    print("Files not found: ")
    for missfile in missfiles:
      print(missfile)

# Tries parsing an integer; if successful returns integer converted back to string,
# otherwise it returns empty string. This is needed so that when diff reports "-" as the
# number of lines, we write this as "" (no value) into the csv file
def check_int(s):
  try:
    return str(int(s))
  except ValueError:
    return ""

#===================================================================================================
# Helper function for reading files
#===================================================================================================

def generateSortedVersions(versions, categories, dates):
  #Map filenames to setsort sort categories.
  setsort = collections.defaultdict(lambda: collections.defaultdict(str))
  for version in versions:
    if "check" in version and version["check"] == "alternate":
      continue
    try:
      date = int(version["date"])
    except:
      if "Not Defined" not in version["date"]:
        print("The date entry of version:", version["id"], "is not convertible to an integer date format")
      continue
    if version["category"] in categories and date in dates:
      setsort[version["category"]][date] = version["id"]
  return setsort

def checkCreate(path, message):
  if not os.path.exists(path):
    print("%s outfolder not found: Creating..." % message)
    os.makedirs(path)

#Check if understand is properly configured.
def checkUnderstandPath(paths):
  try:
    user_paths = os.environ["PYTHONPATH"].split(os.pathsep)
  except KeyError:
    user_paths = []
  try:
    user_paths = os.environ["PATH"].split(os.pathsep)
  except KeyError:
    user_paths = []
  user_paths = sys.path    
  PYTHONPATH=os.environ["PYTHONPATH"].split(os.pathsep)
  ALTPYTHONPATH=r"C:\Program Files\SciTools\bin\pc-win64\python"
  sys.path.append(ALTPYTHONPATH)
  import understand
  print("understand is loaded")

def add_up(*args):
  return sum([int(a)  for a in args if a != ""])

def read_csv(filename, header_rows = 0, delimiter = None):
  with open(filename, "rt") as inp:
    # test delimiters
    if not delimiter:
      first_line = next(inp)
      inp.seek(0)
      has_commas = "," in first_line
      has_tabs = "\t" in first_line
      if has_commas and has_tabs: raise IOError("Delimiter has to be specified")
      if has_commas and not has_tabs: delimiter = ","
      if not has_commas and has_tabs: delimiter = "\t"
      if not has_commas and not has_tabs: delimiter = "\t"

    f = csv.reader(inp, delimiter=delimiter)
    for _ in range(header_rows): next(f)
    for row in f:
      yield row


# Split encoded files-pair string such as 
#  "/XXXX/{2010 => 2011}/YYY.pl"
# into 2 actual file names:
#   "/XXX/2010/CPAN_Parse_RecDescent/YYY.pl"
#   "/XXX/2011/CPAN_Parse_RecDescent/YYY.pl"

def split_files(s):
  # Find the "middle" part of the string, enclosed in braces {}
  bra = ket = -1
  lvl = 0
  for i, c in enumerate(s):
    if c == "{":
      if lvl == 0: 
        bra = i
      lvl += 1
    if c == "}":
      lvl -= 1
      if lvl == 0: 
        ket = i
        if " => " in s[bra+1:ket]: break
  if bra > -1 and ket > -1 and " => " in s[bra+1:ket]:
    parts = s[bra+1:ket].split(" => ")
    file1 = s[:bra] + parts[0] + s[ket+1:]
    file2 = s[:bra] + parts[1] + s[ket+1:]
    return (file1, file2)
  else:
    try:
      return get_paraths(s)
    except Exception:
      return tuple(s.split(" => "))

def get_paraths(s):
  # print(s)
  op = sorted([i for i in range(0, len(s)) if s[i] == "{"])
  cp = sorted([i for i in range(0, len(s)) if s[i] == "}"])

  # print(min(op), max(cp))

  base = s[:min(op)].strip()
  middle = s[min(op)+1:max(cp)].strip()
  end = s[max(cp)+1:].strip()

  lpath = base+middle.split("=>")[0].strip()+end
  rpath = base+middle.split("=>")[1].strip()+end
  lpath = lpath.replace("//", "/")
  rpath = rpath.replace("//", "/")
  return (lpath, rpath)


# Split filename such as 
#  "/media/azdata/code/BA_SNAPSHOTS/2010/CPAN_Parse_RecDescent/Parse-RecDescent-1.94/demo/demo_decomment.pl"
# into 5 parts:
#  package = "CPAN_Parse_RecDescent"
#  year    = "2010"
#  path    = "Parse-RecDescent-1.94/demo/"
#  file    = "demo_decomment"
#  extension = ".pl"
# Thus the original file can be constructed as
#   "/media/azdata/code/BA_SNAPSHOTS/" + year + "/" + package + "/" + path + file + extension
#

def parse_filename(filename, fromFolder, toFolder, line=None):
  filename_parsing_re = re.compile("^([\w\-\.]+)/(.*/)?([^\/]+)$")
  #Optional?
  if filename[0] == '"':
    filename = filename[1:-1]
  fromSplit = filename.split("/" + fromFolder + "/")
  toSplit = filename.split("/" + toFolder + "/")
  if len(fromSplit) > 1:
    codedir = fromSplit[0]
    tailString = fromSplit[1]
    version = fromFolder
  elif len(filename.split(toFolder)) > 1:
    codedir = toSplit[0]
    tailString = toSplit[1]
    version = toFolder
  else:
    print("line", line)
    print("fromFolder", fromFolder)
    print("toFolder", toFolder) 
    print("filename", filename)
    print("fromFolder, toFolder, filename")
    raise ValueError

  mm = re.match(filename_parsing_re, tailString)
  if not mm: 
    print(tailString)
    print(codedir)
    raise ValueError("Cannot parse filename: '%s'" % filename)
  pkg, path, shortfile = mm.groups()
  if "." in shortfile:
    simplefile, ext = shortfile.rsplit(".", 1)
    ext = "." + ext
  else:
    simplefile = shortfile
    ext = ""
  if (not path):
    path = ""
  assert codedir + "/" + version + "/" + pkg + "/" + path + simplefile + ext == filename
  return (pkg, version, path, simplefile, ext)
