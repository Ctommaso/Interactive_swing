from networkx import Graph
from networkx.linalg.graphmatrix import incidence_matrix
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
		self.graph = Graph()
		self.graph.add_nodes_from(buses)
		self.graph.add_edges_from(lines)
		self.state = State(self.graph.number_of_nodes()) 
				
		self.sm_id = filter(lambda n: self.graph.nodes[n]['sm']==True, self.graph.nodes)
		self.load_id = filter(lambda n: self.graph.nodes[n]['sm']==False, self.graph.nodes)

		# unweighted incidence in shape (|nodes| x |edges|), column ordering is produced by graph.edges
		self.incidence = incidence_matrix(self.graph, oriented = True)

		self.node_coord = np.array([self.graph.nodes[n]['coord'] for n in self.graph.nodes])
		self.edge_coord = np.array([(self.node_coord[e[0]] + self.node_coord[e[1]])/2. for e in self.graph.edges()])
	
		
	def get_P(self):
		return np.array([self.graph.nodes[n]['power'] for n in self.graph.nodes])
	
	
	# inertia and damping coeffs, ordered according to sm_id and load_id
	def get_I_sm(self):
		return np.array([self.graph.nodes[n]['inertia'] for n in self.sm_id])
	
		
	def get_D_sm(self):
		return np.array([self.graph.nodes[n]['damping'] for n in self.sm_id])
	
		
	def get_D_load(self):
		return np.array([self.graph.nodes[n]['damping'] for n in self.load_id])

	
	# edge susceptance, edge ordering is produced by graph.edges
	def get_active_susceptance(self):
		return diags([self.graph[e[0]][e[1]]['susceptance'] * int(self.graph[e[0]][e[1]]['status']) for e in self.graph.edges()])


	# edge susceptance, edge ordering is produced by graph.edges
	def get_susceptance(self):
		return diags([self.graph[e[0]][e[1]]['susceptance'] for e in self.graph.edges()])
