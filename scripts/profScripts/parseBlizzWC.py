#parseBlizzWC.py
#Created 10/25/2016
#ssia@keystonestrategy.com


#Takes in the wc output for Blizzard directories
#Extracts file extension and line counts from the source directory

from versionName import VersionName

def parseBlizzWC(versionList)
	for v in versionList:
		#Read file.
		with open(v.fileName) as f:
			#This reads the line without newlines
			lines = f.read().splitlines()
		for line in lines:
			#If has colon, ":", it's a directory header
			if v.wantedFolder in line:
				#Split on whitespace
				line = line.split()
				files = 1
				num = int(line[0])
				if num > 0:
					fname = line[1]
					fname = fname.split("/")[-1]
					ext = fname.split(".")[-1]
					if ext in v.extDic:
						v.extDic[ext] = (v.extDic[ext][0] + files, v.extDic[ext][1] + num)
					else:
						v.extDic[ext] = (files,num)
		v.printDirs()

if __name__ == "__main__":
	fname = "../../input_datasets/patch_filelineCount.txt"
	v406 = VersionName("Cataclysm","./wow-patch-4_0_6-branch/WoW/Source",fname)
	fname = "../../input_datasets/source_filelineCount.txt"
	v701 = VersionName("Legion","./Source",fname)
	versionList = [v406,v701]
	parseBlizzWC(versionList)
