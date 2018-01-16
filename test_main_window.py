import sys
from gui import MainDisplay
from graphs import Electrical_network
from multiprocessing import Event
from PyQt4.QtGui import *


# Script to test the layout of the main window (i.e. MainDisplay object)
# It also allows to test the response of the network to clicks
# Clicking opens Dialog windows to edit node and line parameters

def main():
	
	# Intergers 0,1,2,3,4 are node ids. They can be replaced by other identifiers such as names
	buses = [(0,{'name': "Load 0", 'coord': [0.0, 0.0], 'sm': False, 'power':-0.5, 'damping':1}),
	         (1,{'name': "Gen 1",'coord': [0.1, 0.1], 'sm': True, 'power':1, 'inertia':10, 'damping':1}),
	         (2,{'name': "Gen 2",'coord': [0.15, 0.0], 'sm': True, 'power':-0.5, 'inertia':2, 'damping':1}),
	         (3,{'name': "Load 3",'coord': [0.1, -0.1], 'sm': False, 'power':-1, 'damping':2}),
	         (4,{'name': "Load 4",'coord': [0.2, -0.1], 'sm': False, 'power':1, 'damping':1.5}),
	         (5,{'name': "Load 5",'coord': [0.1, 0.3], 'sm': False, 'power':-2, 'damping':2}),
	         (6,{'name': "Gen 6",'coord': [0.3, 0.0], 'sm': True, 'power':1, 'inertia':6, 'damping':1.5}),
	         (7,{'name': "Load 7",'coord': [-0.05, 0.07], 'sm': False, 'power':-0.5, 'damping':2}),
	         (8,{'name': "Load 8",'coord': [0.0, 0.2], 'sm': False, 'power':-0.5, 'damping':1.5}),
	         (9,{'name': "Gen 9",'coord': [0.0, 0.3], 'sm': True, 'power':2.5, 'inertia':7, 'damping':2}),
	         (10,{'name': "Load 10",'coord': [0.0, 0.35], 'sm': False, 'power':-0.5, 'damping':1.5})]
	         
	lines =	[(0,1,{'weight':2}),(0,2,{'weight':1}),(0,3,{'weight':7}),(1,2,{'weight':3}),
	         (2,3,{'weight':4}),(3,4,{'weight':3}),(1,5,{'weight':3.5}),(2,6,{'weight':4}),
	         (5,6,{'weight':2}),(0,7,{'weight':4.3}),(7,8,{'weight':3}),(1,8,{'weight':2}),
             (8,9,{'weight':4}),(9,10,{'weight':3})]

	el_net = Electrical_network(buses, lines)
	
	proc_ev = Event()
	proc_ev.set()
	app = QApplication(sys.argv)
	test = MainDisplay(el_net, proc_ev)
	sys.exit(app.exec_())
	
	
if __name__ == "__main__":
	main()
