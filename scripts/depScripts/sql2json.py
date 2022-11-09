#sql2json.py
#Created: mshakir@keystonestrategy.com
#Updated: ssia@keystonestrategy.com
#Last Updated: 12/14/2016

#From a db file, creates a json file which is used for centrality
#Currently also contains additional functions for future dsm work if necessary.

# Input: listOfVersions.json, listOfComparisons.json
# Output:
#	basic stats of each directory based on list of versions
#	multiple ramp-down-curve.py in excel format based on list of comparisons
#	diff'ed directories based on list of comparisons
#	analyzed diffs based on list of comparisons	

import json
import sqlite3
import os

class DSM:

	def __init__(self, database=False, table=False, jsonFile=False, zoom="files", data_root=False):
		
		if jsonFile:
			structure = json.loads(open(jsonFile, 'r').read())
			self.packages = structure['packages']
			self.nodes = structure['nodes']
			self.links = structure['links']
			self.zoom = structure['zoom']
		else:
			self.database = database
			self.table = table
			self.zoom = zoom
			self.data_root = data_root
			self.packages = []
			self.nodes = []
			self.links = []
			self.initialize_structure(zoom)

	def getNormEntName(self, EntName, zoom, ent_kind):
		package = ""
		EntName = EntName.replace("\\", "/")
		EntName = EntName.replace(self.data_root, "")

		return EntName

		
	def getPackageID(self, EntName):
		package = self.getNormEntName(EntName, self.zoom, "package")

	# 	# If EntName does not have package info return -1
		if package == "" or package == "error-parsing":
			return -1

		if package not in self.packages:
			self.packages.append(package)

		return self.packages.index(package)

	def getNodeID(self, EntName):
		# group_id = self.getPackageID(EntName)
		# # If not package was found then return -1
		# if group_id < 0:
		# 	return -1

		node_name = self.getNormEntName(EntName, self.zoom, "class")

		#node = {"name":node_name,"group":group_id}
		node = {"name": node_name, "group": 1}

		if node not in self.nodes:
			self.nodes.append(node)

		return self.nodes.index(node)

	def initialize_structure(self, query_type):
		results, total 	= self.queryDatabase(query_type)
		self.errors = []
		count = 0

		for row in results:
			From_File, To_File, Dep_Count = row
			src_index = self.getNodeID(From_File)
			target_index = self.getNodeID(To_File)


			if src_index < 0 or target_index < 0:
				self.errors.append(row)
				continue

			link = {}
			link['source'] 	= src_index
			link['target'] 	= target_index
			link['value']	= Dep_Count

			self.links.append(link)
			if count%10000 == 0:
				print(count, total)

			count += 1
		print("There were %s errors while parsing dependencies." % len(self.errors))

	def queryDatabase(self, query_type):
		conn = sqlite3.connect(self.database)
		c = conn.cursor()
		c1 = conn.cursor()

		query = 'select EntFile_From, EntFile_To, COUNT(*) '
		query += 'from %s ' % self.table
		query += 'group by EntFile_From, EntFile_To '
		query += 'order by EntFile_From, EntFile_To, COUNT(*) desc '


		return c.execute(query), c1.execute('select count(*) from ( '+query+" )").fetchone()[0]

	def saveDependencyMatrixJson(self, output_filename):
		json.dump({"nodes":self.nodes,"links":self.links, "packages":self.packages, "zoom":self.zoom}, \
    		open(output_filename,'w'), \
    		sort_keys=True, indent=4, separators=(',', ': '))

	def getDependencyMatrixNumpy(self):
		import numpy as np
		size = len(self.nodes)	
		print("Matrix has %s nodes"%size)
		# Create a (size x size x 3) array of 8 bit unsigned integers
		color_data = np.zeros( (size,size,3), dtype=np.uint8 )
		color_data.fill(255)

		freq_data = np.zeros( (size,size), dtype=np.uint8 )
		freq_data.fill(0)


		for link in self.links:
			row = link['source'] 
			column = link['target'] 
			value = link['value'] 
			source_copied = link['source_copied']
			target_copied = link['target_copied']

			color = [255,255,255]
			color_name = "white"
			try:
				if source_copied == 1 and target_copied == 1:
					color = [255,140,0] # Orange
					color_name = "orange"
				elif source_copied == 1 and target_copied == 0:
					color = [0,255,0] # Green
					color_name = "green"
				elif source_copied == 0 and target_copied == 1:
					color = [0,0,255] # Blue
					color_name = "blue"
				else:
					color = [255,0,0] # Red
					color_name = "red"
				color_data[row,column] = color
				freq_data[row,column] = value

				print(self.nodes[row]['name'], self.nodes[column]['name'], color_name)

			except:
				print('error')

		return [color_data, freq_data]

	def sortDependencyMatrixJson(self, sort_by):
		#TODO: Test
		if sort_by == "name":
			print("sorting by name")
			# sort nodes by name
			new_nodes = sorted(self.nodes, key=lambda k: k['name'])
			new_links = []
			for link in self.links:
				new_link = link
				new_link['source'] = new_nodes.index(self.nodes[link['source']])
				new_link['target'] = new_nodes.index(self.nodes[link['target']])
				new_links.append(new_link)

			self.nodes = new_nodes
			self.links = new_links



# Code for scaling and rendering of the DSM image
	def scaleMatrixColumns(self, color_data, freq_data, scale):
		import numpy as np
		size = freq_data.shape[1]
		new_freq_columns = []
		new_color_columns = []
		for column_number in range(0, size):
			freq_column = freq_data[:,column_number]
			color_column = color_data[:,column_number]

			freq_column_sum = np.sum(freq_column)
			

			# Get the log of freq unless sum is 0
			log_column_sum = freq_column_sum
			if freq_column_sum > 0:
				log_column_sum = int(np.log10(log_column_sum))
			
			if log_column_sum > 1:
				# If column_sum >= 10 ( log10(sum)>=1 )
				log_column_sum = log_column_sum * scale
				for i in range(0, log_column_sum):
					new_freq_columns.append(freq_column)
					new_color_columns.append(color_column)
			else:
				# If column_sum < 10 (log10(sum)<1)
				new_freq_columns.append(freq_column)
				new_color_columns.append(color_column)
			
		cols_size = len(new_freq_columns)
		print("Freq, Color rows: ", len(new_freq_columns[0]), len(new_color_columns[0]))
		print("Freq, Color columns: ", len(new_freq_columns), len(new_color_columns))

		new_freq_data = np.zeros( (size,cols_size), dtype=np.uint8 )
		new_freq_data.fill(0)

		new_color_data = np.zeros( (size,cols_size, 3), dtype=np.uint8 )
		new_color_data.fill(255)

		for column_number in range(0, cols_size):
			new_freq_data[:,column_number] = new_freq_columns[column_number]
			new_color_data[:,column_number] = new_color_columns[column_number]
		

		return [new_color_data, new_freq_data] 

	def scaleMatrixRows(self, color_data, freq_data, scale):
		import numpy as np
		row_size = freq_data.shape[0]
		cols_size = freq_data.shape[1]
		new_freq_rows = []
		new_color_rows = []
		for row_number in range(0, row_size):
			freq_row = freq_data[:][row_number]
			color_row = color_data[:][row_number]

			freq_row_sum = np.sum(freq_row)
			

			# Get the log of freq unless sum is 0
			log_row_sum = freq_row_sum
			if freq_row_sum > 0:
				log_row_sum = int(np.log10(log_row_sum))
			
			if log_row_sum > 1:
				# If column_sum >= 10 ( log10(sum)>=1 )
				log_row_sum = log_row_sum * scale
				for i in range(0, log_row_sum):
					new_freq_rows.append(freq_row)
					new_color_rows.append(color_row)
			else:
				# If column_sum < 10 (log10(sum)<1)
				new_freq_rows.append(freq_row)
				new_color_rows.append(color_row)
			
		row_size = len(new_freq_rows)
		print("Freq, Color rows: ", len(new_freq_rows[0]), len(new_color_rows[0]))
		print("Freq, Color columns: ", len(new_freq_rows), len(new_color_rows))

		new_freq_data = np.zeros( (row_size,cols_size), dtype=np.uint8 )
		new_freq_data.fill(0)

		new_color_data = np.zeros( (row_size,cols_size, 3), dtype=np.uint8 )
		new_color_data.fill(255)

		for row_number in range(0, cols_size):
			new_freq_data[:][row_number] = new_freq_rows[row_number]
			new_color_data[:][row_number] = new_color_rows[row_number]
		savede

		return [new_color_data, new_freq_data]

	def printPNG(self, matrixPng, scale):
		print("printing png")
		color_data, freq_data = self.getDependencyMatrixNumpy()

		import scipy.misc
		from skimage import transform as tf

		scaled_color_data = color_data

		# scaled_freq_data = freq_data
		# scaled_color_data, scaled_freq_data = self.scaleMatrixColumns(color_data, freq_data, scale)
		# scaled_color_data, scaled_freq_data = self.scaleMatrixRows(scaled_color_data, scaled_freq_data, scale)

		print("Matrix has %s nodes"%scaled_color_data.shape[1])

		img = scipy.misc.toimage(scaled_color_data)       # Create a PIL image
		img.save(matrixPng)

def sql2json(matrixJson,inputFolder,version, dbFile):
	zoom = "all"

	rootFolder = os.path.join(inputFolder, version["folder"])
	try:
		dsm = DSM(False, False, matrixJson, zoom, rootFolder )
	except:
		print("No matrixJson found!: Creating a new file")
		dsm = DSM(dbFile, version["id"], False, "files", rootFolder)
		dsm.sortDependencyMatrixJson("name")   # for name of the package.class i.e. same as ordering by package and node name
		dsm.saveDependencyMatrixJson(matrixJson)
		