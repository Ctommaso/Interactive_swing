from graphs import *
from solver import *
from gui import *
from multiprocessing import Process, Queue, Event


def main():
	
	# Intergers 0,1,2,3,4 are node ids. They can be replaced by other identifiers such as names
	buses = [(0,{'coord': [0.0, 0.0], 'sm': False, 'power':-0.5, 'damping':1}),
	         (1,{'coord': [0.1, 0.1], 'sm': True, 'power':1, 'inertia':10, 'damping':1}),
	         (2,{'coord': [0.1, 0.2], 'sm': True, 'power':-0.5, 'inertia':2, 'damping':1}),
	         (3,{'coord': [0.2, 0.1], 'sm': False, 'power':-1, 'damping':2}),
	         (4,{'coord': [0.4, 0.4], 'sm': False, 'power':1, 'damping':1.5}),
	         (5,{'coord': [0.5, 0.3], 'sm': False, 'power':-2, 'damping':2}),
	         (6,{'coord': [0.1, 0.4], 'sm': True, 'power':1, 'inertia':6, 'damping':1.5}),
	         (7,{'coord': [0.5, 0.8], 'sm': False, 'power':-0.5, 'damping':2}),
	         (8,{'coord': [0.2, 0.8], 'sm': False, 'power':-0.5, 'damping':1.5}),
	         (9,{'coord': [0.2, 0.45], 'sm': True, 'power':2.5, 'inertia':7, 'damping':2}),
	         (10,{'coord': [0.4, 0.5], 'sm': False, 'power':-0.5, 'damping':1.5})]
	         
	lines =	[(0,1,{'weight':2}),(0,2,{'weight':1}),(0,3,{'weight':7}),(1,2,{'weight':3}),
	         (2,3,{'weight':4}),(3,4,{'weight':3}),(1,5,{'weight':3.5}),(2,6,{'weight':4}),
	         (5,6,{'weight':2}),(0,7,{'weight':4.3}),(7,8,{'weight':3}),(1,8,{'weight':2}),
             (8,9,{'weight':4}),(9,10,{'weight':3})]

	el_net = Electrical_network(buses, lines)
	print 'Power', el_net.P
	print 'SM id', el_net.sm_id
	print 'Load id ', el_net.load_id
	print 'Coord ', el_net.get_coord()
	print 'SM inertia {}, and damping {}'.format([buses[n][1]['inertia'] for n in el_net.sm_id],
	                                             [buses[n][1]['damping'] for n in el_net.sm_id])
	print 'Load damping ', [buses[n][1]['damping'] for n in el_net.load_id]
	
	print 'Phase', el_net.state.phase
	print 'Freq', el_net.state.frequency
	
	# Event for synchrony between threads
	e = Event()
	e.set()
	
	s = Simulator(el_net, RK, max_iter = 3000)
	
	# Queue for sharing data between threads
	q = Queue()
	
	# Run simulation in a process, and display in a different process
	t = Process(target=s.start, args = (q, e))
	p = Process(target = display, args = (q, el_net, e, 500))
	
	t.start() ; p.start()
	
	t.join() ; p.join()
if __name__ == '__main__':
	main()
