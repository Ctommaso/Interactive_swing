from sys import exit, argv
from gui import MainDisplay
from graphs import Electrical_network
from multiprocessing import Event
from PyQt4.QtGui import QApplication
from sample_networks import buses1, lines1
from scipy import optimize
from helper_fcts import steady_state_PF
import numpy as np

# Script to test the layout of the main window (i.e. MainDisplay object)
# It also allows to test the response of the network to clicks
# Clicking opens Dialog windows to edit node and line parameters
# It also allows to test power flow direction arrows

def main():
	
	el_net = Electrical_network(buses1, lines1)
	node_nb = el_net.graph.number_of_nodes()
	# Use scipy to solve the steady state power flow
	sol = optimize.root(steady_state_PF, np.zeros(node_nb), args = (el_net, el_net.get_P()), jac=None, method='hybr')
	print "SIMULATION SUCCESSFUL", sol.success
	el_net.state.phase = sol.x

	proc_ev = Event()
	proc_ev.set()
	app = QApplication(argv)
	
	# Create Main Display instance
	test = MainDisplay(el_net, proc_ev)
	exit(app.exec_())
	
	
if __name__ == "__main__":
	main()
