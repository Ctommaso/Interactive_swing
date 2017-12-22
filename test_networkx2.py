import networkx as nx
from scipy.sparse import diags
from Graphs import *
from solver import *

def main():
	
	# Intergers 0,1,2,3,4 are node ids. They can be replaced by other identifiers such as names
	buses = [(0,{'coord_x': 0.0,'coord_y': 0.0, 'sm': True, 'power':0.10, 'inertia':0.4, 'damping':0.4}),
	         (1,{'coord_x': 0.1,'coord_y': 0.1, 'sm': False, 'power':0.05, 'damping':0.11}),
	         (2,{'coord_x': 0.2,'coord_y': 0.2, 'sm': False, 'power':-0.2, 'damping':0.33}),
	         (3,{'coord_x': 0.3,'coord_y': 0.3, 'sm': True, 'power':0.15, 'inertia':0.9, 'damping':0.9}),
	         (4,{'coord_x': 0.4,'coord_y': 0.4, 'sm': True, 'power':-0.1, 'inertia':1.4, 'damping':1.4})]
	lines =	[(0,1,{'weight':20}),
	         (0,2,{'weight':10}),
	         (0,3,{'weight':70}),
	         (1,2,{'weight':30}),
	         (2,3,{'weight':40}),
	         (3,4,{'weight':30})]

	el_net = Electrical_network(buses, lines)

	print 'Phase', el_net.state.phase
	print 'Freq', el_net.state.frequency
	print 'Power', el_net.P
	print 'SM id', el_net.sm_id
	print 'Load id ', el_net.load_id
	print 'Coord ', el_net.get_coord()
	print [buses[n][1]['inertia'] for n in el_net.sm_id]
	print [buses[n][1]['damping'] for n in el_net.sm_id]
	print [buses[n][1]['damping'] for n in el_net.load_id]
	
	s = Simulator(el_net, RK, max_iter = 1000)
	print(s.max_iter)
	print(s.paused)
	
	s.start()	

if __name__ == '__main__':
	main()
