from graphs import *
from solver import *
from gui2 import *
from PyQt4.QtGui import *
from multiprocessing import Process, Queue, Event
import time

def main():

	buses = [(0,{'name': "Load 0", 'coord': [0.0, 0.0], 'sm': False, 'power':-0.5, 'damping':1}),
	         (1,{'name': "Gen 1",'coord': [0.1, 0.1], 'sm': True, 'power':1, 'inertia':10, 'damping':1}),
	         (2,{'name': "Gen 2",'coord': [0.1, 0.2], 'sm': True, 'power':-0.5, 'inertia':2, 'damping':1}),
	         (3,{'name': "Load 3",'coord': [0.2, 0.1], 'sm': False, 'power':-1, 'damping':2}),
	         (4,{'name': "Load 4",'coord': [0.4, 0.4], 'sm': False, 'power':1, 'damping':1.5}),
	         (5,{'name': "Load 5",'coord': [0.5, 0.3], 'sm': False, 'power':-2, 'damping':2}),
	         (6,{'name': "Gen 6",'coord': [0.1, 0.4], 'sm': True, 'power':1, 'inertia':6, 'damping':1.5}),
	         (7,{'name': "Load 7",'coord': [0.5, 0.8], 'sm': False, 'power':-0.5, 'damping':2}),
	         (8,{'name': "Load 8",'coord': [0.2, 0.8], 'sm': False, 'power':-0.5, 'damping':1.5}),
	         (9,{'name': "Gen 9",'coord': [0.2, 0.45], 'sm': True, 'power':2.5, 'inertia':7, 'damping':2}),
	         (10,{'name': "Load 10",'coord': [0.4, 0.5], 'sm': False, 'power':-0.5, 'damping':1.5})]
	         
	lines =	[(0,1,{'weight':2}),(0,2,{'weight':1}),(0,3,{'weight':7}),(1,2,{'weight':3}),
	         (2,3,{'weight':4}),(3,4,{'weight':3}),(1,5,{'weight':3.5}),(2,6,{'weight':4}),
	         (5,6,{'weight':2}),(0,7,{'weight':4.3}),(7,8,{'weight':3}),(1,8,{'weight':2}),
             (8,9,{'weight':4}),(9,10,{'weight':3})]

	el_net = Electrical_network(buses, lines)
	
	# Event for synchrony between threads
	proc_ev = Event()
	proc_ev.set()
	
	s = Simulator(el_net, RK, max_iter = 3000)
	
	app = QApplication(sys.argv)
	
	# Queue for sharing data between threads
	q = Queue()
	print("uno")
	
	# Simulation process
	t = Process(target=s.start, args = (q, proc_ev))

	# UI thread
	thread_instance = Thread(el_net, proc_ev)
	
	#p = Process(target = test_UI.display, args = (q, el_net, proc_ev, 500))
	print("due")
	t.start()
	thread_instance.display(q, el_net, proc_ev, 500)
	
	
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()
