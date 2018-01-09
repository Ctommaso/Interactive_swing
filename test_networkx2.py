import networkx as nx
from scipy.sparse import diags
from graphs import *
from solver import *
import matplotlib.pyplot as plt

def main():
	
	# Intergers 0,1,2,3,4 are node ids. They can be replaced by other identifiers such as names
	buses = [(0,{'coord_x': 0.0,'coord_y': 0.0, 'sm': False, 'power':-0.5, 'damping':1}),
	         (1,{'coord_x': 0.1,'coord_y': 0.1, 'sm': True, 'power':1, 'inertia':10, 'damping':1}),
	         (2,{'coord_x': 0.2,'coord_y': 0.2, 'sm': True, 'power':-0.5, 'inertia':2, 'damping':1}),
	         (3,{'coord_x': 0.3,'coord_y': 0.3, 'sm': False, 'power':-1, 'damping':1}),
	         (4,{'coord_x': 0.4,'coord_y': 0.4, 'sm': False, 'power':1, 'damping':1})]
	         
	lines =	[(0,1,{'weight':2}),(0,2,{'weight':1}),(0,3,{'weight':7}),(1,2,{'weight':3}),
	                  (2,3,{'weight':4}),(3,4,{'weight':3})]

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
	
	phase = el_net.state.phase
	freq = el_net.state.frequency
	print "Phase", phase, el_net.state.phase
	print "Freq", freq, el_net.state.frequency
	
	s = Simulator(el_net, RK, max_iter = 2)
	print(s.max_iter)
	print(s.paused)
	
	sol_T, sol_F = s.start()	
	print sol_T[-1]
	print 3*np.sin(sol_T[-1][4]-sol_T[-1][3])
	#plt.plot(sol_T)
	fig, ax = plt.subplots(2,1,sharex=True)
	ax[0].plot(sol_T)
	ax[1].plot(sol_F)
	plt.show()

if __name__ == '__main__':
	main()
