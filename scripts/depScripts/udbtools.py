import understand
import csv

class Ent:
  def __init__ (self, udb, ent):
    self.udb = udb
    self.ent = ent
    self.kindobj = ent.kind()
    self.kind = self.kindobj.longname()
    self.category = udb.lookUpEntCategory(self.kind)
    self.name = self.ent.longname()
    self.defref = None
    self.deffileobj = None
    self.deffile = None
    self.defline = None

  def setDefRef (self, defref):
    self.defref = defref
    self.deffileobj = defref.file()
    self.deffile = self.deffileobj.longname()
    self.defline = self.defref.line()

  @staticmethod
  def rowHeaders ():
    return [ "EntFile", "EntLine", "EntName", "EntKind", "EntType" ]

  def row (self):
    if self.category == "File":
      return [ self.name, "n/a", "n/a", self.category, self.kind ]
    row = []
    if self.defref:
      row += [ self.deffile, str(self.defline) ]
    else:
      row += [ "unknown", "unknown" ]
    row += [ self.name, self.category, self.kind ]
    return row

  @staticmethod
  def idrowHeaders ():
    return [ "EntFile", "EntLine", "EntName", "EntKind", "EntType", "EntID" ]

  def idrow (self):
    return self.row() + [ self.ent.id() ]

class Ref:
  def __init__ (self, udb, ref):
    self.udb = udb
    self.ref = ref
    kindobj = self.ref.kind()
    self.kind = kindobj.longname()
    self.category = udb.lookUpRefCategory(self.kind)
    fileobj = self.ref.file()
    self.file = fileobj.longname()
    self.line = self.ref.line()

  @staticmethod
  def rowHeaders ():
    return [ "RefFile", "RefLine", "RefKind", "RefType" ]

  def row (self):
    row = []
    row += [ self.file, self.line, self.category, self.kind ]
    return row

class UDB:
  def __init__ (self, udbpath):
    self.udbpath = udbpath
    print("Opening " + self.udbpath)
    self.db = understand.open(self.udbpath)
    print("Done opening " + self.udbpath)

  def setSpecs (self, language, typemap, refmap, deprules, nofile=set()):
    self.language = language
    self.typemap = typemap
    self.refmap = refmap
    self.deprules = deprules
    self.buildDepmap()
    self.nofile = nofile
    self.defineinKind = self.language + " Definein"

  def buildDepmap (self):
    self.depmap = {}
    for rule in self.deprules:
      if rule[0] not in self.depmap:
        self.depmap[rule[0]] = {}
      if rule[1] not in self.depmap[rule[0]]:
        self.depmap[rule[0]][rule[1]] = []
      if rule[2] not in self.depmap[rule[0]][rule[1]]:
        self.depmap[rule[0]][rule[1]].append(rule[2])

  def lookUpEntCategory (self, enttype):
    for key in self.typemap:
      if enttype in self.typemap[key]:
        return key
    return None

  def lookUpRefCategory (self, reftype):
    for key in self.refmap:
      if reftype in self.refmap[key]:
        return key
    return None

  def generateEntString (self):
    ents = []
    for rule in self.deprules:
      if rule[0] not in ents:
        ents.append(rule[0])
    return ", ".join(ents)

  def generateCompleteEntString (self):
    ents = []
    for rule in self.deprules:
      if rule[0] not in ents:
        ents.append(rule[0])
      if rule[2] not in ents:
        ents.append(rule[2])
    return ", ".join(ents)

  def generateRefString (self, enttype):
    refs = []
    entcategory = self.lookUpEntCategory(enttype)
    for rule in self.deprules:
      if rule[0] == entcategory and rule[1] not in refs:
        refs.append(rule[1])
    if "Definein" not in refs:
      refs.append("Definein")
    return ", ".join(refs)

  def dumpDeps (self, csvOutPath):
    with open(csvOutPath, 'w') as csvfile:
      writer = csv.writer(csvfile, lineterminator='\n')
      writer.writerow(Ent.idrowHeaders() + Ref.rowHeaders() + Ent.idrowHeaders())

      # find and process ents
      entstring = self.generateEntString()
      for rawent in self.db.ents(entstring):
        ent = Ent(self, rawent)
        if ent.category == None:
          print("no category for ent: ", ent.kind)
        if ent.category not in self.depmap:
          print(ent.category + " ent not in a dep rule")
          continue
        deps = []

        # find and process each dep for this ent
        refString = self.generateRefString(ent.kind)
        for rawref in rawent.refs(refString, unique=True):
          ref = Ref(self, rawref)

          # record the ent definition if applicable
          if ref.kind == self.defineinKind:
            if not ent.defref:
              ent.setDefRef(ref.ref)

          # otherwise process the reference
          else:
            if ref.category == None:
              print("no category for ref: ", ref.kind)
              continue
            if ref.category not in self.depmap[ent.category]:
              print(ref.category + " ref is not in a dep rule")
              continue

            # process the referenced ent
            ent2 = Ent(self, ref.ref.ent())
            if ent2.category == None:
              print("no category for ent: ", ent2.kind)
            if ent2.category in self.depmap[ent.category][ref.category]:
              deps.append([ref, ent2])

        # save all dependencies for this ent
        for dep in deps:
          writer.writerow(ent.idrow() + dep[0].row() + dep[1].idrow())

  def dumpEnts (self, csvOutPath):
    with open(csvOutPath, 'w') as csvfile:
      writer = csv.writer(csvfile, lineterminator='\n')
      writer.writerow(Ent.idrowHeaders())

      # find and process ents
      entstring = self.generateCompleteEntString()
      for rawent in self.db.ents(entstring):
        ent = Ent(self, rawent)
        if ent.category == None:
          print("no category for ent: ", ent.kind)
        if ent.category not in self.depmap:
          print(ent.category + " ent not in a dep rule")
          continue

        defref = rawent.ref("definein")
        if defref:
          ent.setDefRef(defref)

        writer.writerow(ent.idrow())

