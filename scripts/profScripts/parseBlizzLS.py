#parseBlizzLS.py
#Created 10/25/2016
#ssia@keystonestrategy.com

#Takes in the ls output for Blizzard directories
# For each 1st level directory, prints the file extension and file information

from versionName import VersionName

def parseBlizzLS(versionList):
	for v in versionList:
		#Read file.
		with open(v.fileName) as f:
			#This reads the line without newlines
			lines = f.read().splitlines()
		use = 0
		for line in lines:
			#If has colon, ":", it's a directory header
			if ":" in line and "Administrators" not in line:
				if v.wantedFolder in line:
					use = 1
					#Exclude the wantedFolder, split by "/", take first reading
					curDir = line.replace(":","")
					curDir = curDir.replace(v.wantedFolder,"",1)
					if curDir:
						curDir = curDir.split("/")[1]
					else: curDir = "base"
				else:
					use = 0
			#If administrators in line, it's a file and filecount
			elif "Administrators" in line:
				if use == 1:
					#Split on whitespace
					line = line.split()
					if len(line) == 9:
						files = 1
						num = int(line[4])
						if num > 0:
							if curDir in v.dic:
								v.dic[curDir] = (v.dic[curDir][0] + files, v.dic[curDir][1] + num)
							else:
								v.dic[curDir] = (files,num)
							fname = line[8]
							ext = fname.split(".")[-1]
							if ext in v.extDic:
								v.extDic[ext] = (v.extDic[ext][0] + files, v.extDic[ext][1] + num)
							else:
								v.extDic[ext] = (files,num)
		v.printDirs()

if __name__ == "__main__":
	fname = "../../input_datasets/patch406_files.txt"
	v406 = VersionName("Cataclysm","./WoW/Source",fname)
	fname = "../../input_datasets/source701_files.txt"
	v701 = VersionName("Legion",".",fname)
	versionList = [v1,v2]
	parseBlizzLS(versionList)