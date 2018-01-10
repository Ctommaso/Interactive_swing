import networkx as nx
import numpy as np
from scipy.sparse import diags


class State():
	
	""" State of the grid , phase, frequency """

	def __init__(self, nb_nodes):
		
		# Flat start initialization
		self.phase = np.zeros(nb_nodes)
		self.frequency = np.zeros(nb_nodes)


class Electrical_network():
	
	""" Electrical Network: graph, power injections, electrical state (phases and frequencies)
	
	inputs: list of buses (id, {dict}), list of lines (id, {dict}) """
	
	def __init__(self, buses, lines):

		# create networkx graph
		self.graph = nx.Graph()
		self.graph.add_nodes_from(buses)
		self.graph.add_edges_from(lines)
		self.state = State(self.graph.number_of_nodes()) 
		
		self.P = np.array([self.graph.nodes[n]['power'] for n in self.graph.nodes])
		
		self.sm_id = filter(lambda n: self.graph.nodes[n]['sm']==True, self.graph.nodes)
		self.load_id = filter(lambda n: self.graph.nodes[n]['sm']==False, self.graph.nodes)

		# unweighted incidence in shape (|nodes| x |edges|), column ordering is produced by graph.edges
		self.incidence = nx.linalg.graphmatrix.incidence_matrix(self.graph, oriented = True)
		# edge weights, edge ordering is produced by graph.edges
		self.edge_susc = diags([self.graph[e[0]][e[1]]['weight'] for e in self.graph.edges()])

		# inertia and damping coeffs, ordered according to sm_id and load_id
		self.inertia_sm = np.array([self.graph.nodes[n]['inertia'] for n in self.sm_id])
		self.damping_sm = np.array([self.graph.nodes[n]['damping'] for n in self.sm_id])
		self.damping_load = np.array([self.graph.nodes[n]['damping'] for n in self.load_id])


	def get_coord(self):
		
		coord = [self.graph.nodes[n]['coord'] for n in self.graph.nodes]
		return coord
