import csv
import sys
from enum import Enum


class EntSchema:
    file = 0
    line = 1
    name = 2
    kind = 3
    longkind = 4
    id = 5

class CsvSchema:
    ent1file = 0
    ent1line = 1
    ent1name = 2
    ent1kind = 3
    ent1type = 4
    ent1id = 5
    reffile = 6
    refline = 7
    refkind = 8
    reftype = 9
    ent2file = 10
    ent2line = 11
    ent2name = 12
    ent2kind = 13
    ent2type = 14
    ent2id = 15
    headerList = [ "EntFile_From","EntLine_From","EntName_From","EntKind_From","EntType_From","EntID_From","RefFile",
      "RefLine","RefKind","RefType","EntFile_To","EntLine_To","EntName_To","EntKind_To","EntType_To","EntID_To" ]

class EntRecord:
  def __init__ (self, id, kind, longkind, name, deffile, defline):
    self.id = id
    self.kind = kind
    self.longkind = longkind
    self.name = name
    self.deffile = deffile
    self.defline = defline

  @classmethod
  def fromRow (cls, row, schema):
    id = row[schema.id]
    kind = row[schema.kind]
    longkind = row[schema.longkind]
    name = row[schema.name]
    deffile = row[schema.file]
    defline = row[schema.line]
    return EntRecord(id, kind, longkind, name, deffile, defline)

  def __str__ (self):
    return str([ self.id, self.kind, self.longkind, self.name, self.deffile, self.defline ])

  def __eq__ (self, other):
    if (self.id != other.id
      or self.kind != other.kind
      or self.longkind != other.longkind
      or self.name != other.name
      or self.deffile != other.deffile
      or self.defline != other.defline):
      return False
    return True

class EntMap:
  def __init__ (self, schema):
    self.schema = schema
    self.entmap = {}

  def load (self, csvInFileName):
    with open(csvInFileName, "r") as infile:
      reader = csv.reader(infile)
      next(reader) # skip header row
      for row in reader:
        record = EntRecord.fromRow(row, self.schema)
        if record.id in self.entmap:
          if record != self.entmap[record.id]:
            print("Error: inconsistent duplicate entities")
            print(str(self.entmap[record.id]))
            print(str(record))
            exit(1)
        elif record.deffile != "unknown" or record.defline != "unknown":
          self.entmap[record.id] = record

  def lookup (self, entid):
    if entid not in self.entmap:
      return None
    return self.entmap[entid]

def stitchCsv (inCsv, entDbCsv, outCsv):
  entmap = EntMap(EntSchema)
  print("Loading entity map from " + entDbCsv)
  entmap.load(entDbCsv)
  print("Stitching csv " + outCsv)
  with open(inCsv, 'r') as infile, open(outCsv, 'w') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile, delimiter=';', lineterminator='\n')
    writer.writerow(CsvSchema.headerList) # copy header row
    next(reader)
    for row in reader:
      ent2id = row[CsvSchema.ent2id]
      ent2 = entmap.lookup(ent2id)
      if ent2:
        row[CsvSchema.ent2file] = ent2.deffile
        row[CsvSchema.ent2line] = ent2.defline
      writer.writerow(row)

if __name__ == "__main__":
  if len(sys.argv) < 4:
    print("Needs 3 arguments")
    print("1. input csv file")
    print("2. entity csv file")
    print("3. output csv file")
    exit(1)

  incsv = sys.argv[1]
  entcsv = sys.argv[2]
  outcsv = sys.argv[3]
  stitchCsv(incsv, entcsv, outcsv)

