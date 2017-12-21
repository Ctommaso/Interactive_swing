import networkx as nx
from scipy.sparse import diags


class State():
	
	""" State of the grid , phase, frequency """

	def __init__(self, nb_nodes):
		self.phase = np.zeros(nb_nodes)
		self.frequency = np.zeros(nb_nodes)


class Electrical_network():
	
	""" Electrical Network: graph, power injections, electrical state (phases and frequencies)
	
	inputs: list of buses (id, {dict}), list of lines (id, {dict}) """
	
	def __init__(self, buses, lines):

		# create networkx graph
		self.graph = nx.Graph()
		self.graph.add_nodes_from(buses)
		self.graph.add_lines_from(lines)
		
		self.state = State(self.graph.number_of_nodes()) 
		self.P = np.array([bus['power'] for bus in buses])
		
	def get_power(self):	

		powers =  np.array([self.graph.nodes[n]['power'] for n in self.graph.nodes])
		return powers

	def get_coord(self):	

		coord = [(self.graph.nodes[n]['coord_x'],self.graph.nodes[n]['coord_y']) for n in self.graph.nodes]
		return coord


class Simulation():
	
	""" Simulation object: 
	
	inputs: electrical network object,
	        integer max_iterations, 
	        fct for time integration time_integrator,
	        simulator state paused True/False
	"""
	
	def __init__(self, el_network, time_integrator , max_iter = 1e6, paused = False)
		self.max_iter = max_iter if max_iter is not 1e6
		self.time_integrator = time_integrator
		self.paused = paused
		self.el_network = el_network

	def start():
		
