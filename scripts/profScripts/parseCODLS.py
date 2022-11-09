#parseCODLS.py
#Created 10/25/2016
#ssia@keystonestrategy.com

#Takes in the ls output for codSrc directory output
#Provided by Activision BLizzard
# For each 1st level directory, prints the file extension and file information

from versionName import VersionName

def parseCODLS(versionList):
	for v in versionList:
		#Read file.
		with open(v.fileName) as f:
			lines = f.read().splitlines()

		for line in lines:
			if v.string in line:
				line = line.split("/")
				m = v.srcIndex
				if len(line) >= m+2 and line[m] == "src":
					curDir = line[m+1]
					numstr = line[0].split()[0]
					num = int(numstr.replace(",",""))
					files = 1
					if curDir in v.dic:
						v.dic[curDir] = (v.dic[curDir][0] + files, v.dic[curDir][1] + num)
					else:
						v.dic[curDir] = (files,num)
		v.printDirs()

if __name__ == "__main__":
	fname = "../../output_datasets/03_sloc_output/sloccount_ba_clean_08_Call_of_Duty_Modern_Warfare_2.txt"
	o8 = VersionName("08_Call_of_Duty_Modern_Warfare_2",8,fname)
	fname = "../../output_datasets/03_sloc_output/sloccount_ba_clean_06_Call_of_Duty_Modern_Warfare.txt"
	o6 = VersionName("06_Call_of_Duty_Modern_Warfare",8,fname)
	fname = "../../output_datasets/03_sloc_output/sloccount_ba_clean_10_Call_of_Duty_Modern_Warfare_3.txt"
	o10 = VersionName("10_Call_of_Duty_Modern_Warfare_3",8,fname)
	fname = "../../output_datasets/03_sloc_output/sloccount_ba_clean_11_Call_of_Duty_Black_Ops_2.txt"
	o11 = VersionName("11_Call_of_Duty_Black_Ops_2",9,fname)
	fname = "../../output_datasets/03_sloc_output/sloccount_ba_clean_11_Call_of_Duty_Black_Ops_2.txt"
	o12 = VersionName("11_Call_of_Duty_Black_Ops_2",9,fname)
	versionList = [o8, o6,o10, o11, o12]
	parseCODLS(versionList)