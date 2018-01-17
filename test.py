from PyQt4.QtGui import *
from multiprocessing import Queue, Event
from threading import Thread
import sys
from graphs import *
from solver import *
from gui import *


def main():

	# Intergers 0,1,2,3,4 are node ids. They can be replaced by other identifiers such as names
	buses = [(0,{'name': "Load 0", 'coord': [0.0, 0.0], 'sm': False, 'power':-0.5, 'damping':0.5}),
	         (1,{'name': "Gen 1",'coord': [0.1, 0.1], 'sm': True, 'power':1, 'inertia':1, 'damping':0.5}),
	         (2,{'name': "Gen 2",'coord': [0.15, 0.0], 'sm': True, 'power':-0.5, 'inertia':1, 'damping':0.5}),
	         (3,{'name': "Load 3",'coord': [0.1, -0.1], 'sm': False, 'power':-1, 'damping':1}),
	         (4,{'name': "Load 4",'coord': [0.2, -0.1], 'sm': False, 'power':1, 'damping':0.75}),
	         (5,{'name': "Load 5",'coord': [0.1, 0.3], 'sm': False, 'power':-2, 'damping':1}),
	         (6,{'name': "Gen 6",'coord': [0.3, 0.0], 'sm': True, 'power':1, 'inertia':0.6, 'damping':0.75}),
	         (7,{'name': "Load 7",'coord': [-0.05, 0.07], 'sm': False, 'power':-0.5, 'damping':1}),
	         (8,{'name': "Load 8",'coord': [0.0, 0.2], 'sm': False, 'power':-0.5, 'damping':0.75}),
	         (9,{'name': "Gen 9",'coord': [0.0, 0.3], 'sm': True, 'power':2.5, 'inertia':0.7, 'damping':0.5}),
	         (10,{'name': "Load 10",'coord': [0.0, 0.35], 'sm': False, 'power':-0.5, 'damping':0.6})]
	         
	lines =	[(0,1,{'susceptance':2.0, 'status':True}),(0,2,{'susceptance':1.0, 'status':True}),(0,3,{'susceptance':7.0, 'status':True}),
	         (1,2,{'susceptance':3.0, 'status':True}),(2,3,{'susceptance':4.0, 'status':True}),(3,4,{'susceptance':3.0, 'status':True}),
	         (1,5,{'susceptance':3.5, 'status':True}),(2,6,{'susceptance':4.0, 'status':True}),(5,6,{'susceptance':2.0,'status':True}),
	         (0,7,{'susceptance':4.3, 'status':True}),(7,8,{'susceptance':3.0, 'status':True}),(1,8,{'susceptance':2.0, 'status':True}),
             (8,9,{'susceptance':4.0, 'status':True}),(9,10,{'susceptance':3.0, 'status':True})]

	el_net = Electrical_network(buses, lines)
	
	# Event for synchrony between threads
	proc_ev = Event()
	proc_ev.set()
	
	# Create simulator istance
	s = Simulator(el_net, RK, max_iter = 3000)
	
	# Queue for sharing data between threads
	q = Queue()

	# Qt event loop 
	app = QApplication(sys.argv)
	
	# Simulation process
	proc = Thread(target = s.start, args = (q, proc_ev))
	proc.daemon = True
		
	# UI thread
	gui_thread = GuiThread(el_net, proc_ev)	
	
	# Start simulation and gui threads
	proc.start()
	gui_thread.display(q, proc_ev, plot_buffer = 100)
	
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()
