class VersionName:
	"""class to parse data"""

	def __init__(self,string,srcIndex,fileName):
		self.dic = {}
		self.extDic = {}
		self.string = string
		self.wantedFolder = srcIndex
		self.fileName = fileName

	def printDirs(self):
		print(self.string)
		for key in self.dic:
			print (key, self.dic[key][0], self.dic[key][1])
		print()
		for key in self.extDic:
			print(key, self.extDic[key][0],self.extDic[key][1])
		print()