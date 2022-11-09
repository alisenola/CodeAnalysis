# TODO: Make this run on many files at once
# TODO: Error-check JSON input dep file

#core_s.py
#takes in a json list of all nodes and all links
#For each dependency, creates a list of nodes and edges,
#Runs networkX centrality upon the nodes and edges,
#Outputs the data which is the centrality scores into a CSV file

#Created: mshakir@keystonestrategy.com
#Updated: ssia@keystonestrategy.com
#Last Updated: 10/25/2016

import json
import networkx as nx
import csv

ADDITIONAL_METRICS = False

def pagerank(matrixJson, outcsv):
	deps = json.loads(open(matrixJson,"r").read())

	nodes = deps['nodes']
	links = deps['links']
	packages = deps['packages']

	node_package_map = {}

	# Load DSM into a graph
	G = nx.DiGraph()

	# Add nodes
	for node in nodes:
		n_name = node["name"]
#		node_package_map[n_name] = packages[node["group"]]
		G.add_node(n_name)

	# Add edges
	for link in links:
		row = link['source']
		column = link['target']
		value = link['value']

		r_n_name = nodes[row]["name"]
		c_n_name = nodes[column]["name"]

		G.add_edge(r_n_name, c_n_name)


	metrics = {}

	# NOTE: DEFAULT ALPHA FROM LITERATURE IS 0.85
	metrics["page_rank"] = nx.pagerank(G, alpha = 0.85)

	# 	Compute the in-degree centrality for nodes.
	# 	Compute the out-degree centrality for nodes.
	# closeness_centrality(G[, v, distance, ...]) # 	Compute closeness centrality for nodes.
	# betweenness_centrality(G[, k, normalized, ...]) # 	Compute the shortest-path betweenness centrality for nodes.
	# load_centrality(G[, v, cutoff, normalized, ...]) # 	Compute load centrality for nodes.
	if (ADDITIONAL_METRICS):
		metrics["degree_centrality"] = nx.degree_centrality(G)
		metrics["in_degree_centrality"] = nx.in_degree_centrality(G) 
		metrics["out_degree_centrality"] = nx.out_degree_centrality(G) 
		metrics["closeness_centrality"] = nx.closeness_centrality(G) 
		metrics["betweenness_centrality"] = nx.betweenness_centrality(G) 
		metrics["load_centrality"] = nx.load_centrality(G) 

	with open(outcsv, 'w', newline = '') as outfile:
		logFile = csv.writer(outfile, delimiter = ',', quotechar = '|')
		for metricName in metrics:
			metric = metrics[metricName]
			for node_name in sorted(metric, key=metric.get, reverse=True):
				logFile.writerow([ node_name, str(metric[node_name]), metricName ])

	print("Pagerank written to: ", outcsv)
