from PyQt4.QtGui import QApplication
from dialog_ui import dialog_load_network
from multiprocessing import Queue, Event
from threading import Thread
from sys import argv, exit, modules
from graphs import *
from solver import *
from gui import *


def main():

	# Qt event loop 
	app = QApplication(argv)

	# Load network data
	buses, lines = dialog_load_network()
	
	# Construct electrical network
	el_net = Electrical_network(buses, lines)
	
	# Event for synchrony between threads
	proc_ev = Event()
	proc_ev.set()
	
	# Create simulator istance
	s = Simulator(el_net, RK, time_step = 5e-2, max_iter = 5000)
	
	# Queue for sharing data between threads
	q = Queue()
	
	# Simulation process
	proc = Thread(target = s.start, args = (q, proc_ev))
	proc.daemon = True
		
	# UI thread
	gui_thread = GuiThread(el_net, proc_ev)	
	
	# Start simulation and gui threads
	proc.start()
	gui_thread.display(q, proc_ev, plot_buffer = 250)
	
	exit(app.exec_())

if __name__ == '__main__':
	main()
