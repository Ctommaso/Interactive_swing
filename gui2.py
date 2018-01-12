from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyqtgraph as pg
import numpy as np
import multiprocessing, sys
from graphs import *
from functools import partial

class Thread(QThread):
	def __init__(self, el_net, proc_ev):
		QThread.__init__(self)
		self.maindisplay = MainDisplay(el_net, proc_ev)
		
	def display(self, q, el_net, proc_ev, plot_buffer = 3*1e03):
		
		# Real time plotting of phase and frequency time series
		self.maindisplay.curves_phase = [self.maindisplay.p_phase.plot() for n in range(0,11)]
		self.maindisplay.curves_freq = [self.maindisplay.p_freq.plot() for n in range(0,4)]
		
		self.maindisplay.data_t = np.zeros(int(plot_buffer),dtype=float)
		self.maindisplay.data_p = np.zeros((int(plot_buffer),11),dtype=float)
		self.maindisplay.data_f = np.zeros((int(plot_buffer),4),dtype=float)
		print("Hello 1")

		def updateInProc(self, q):
			#print("updating plot")
			if q.empty():
				return
					
			item = q.get()
			self.maindisplay.data_t[0:-1] = self.maindisplay.data_t[1:]
			self.maindisplay.data_p[0:-1,:] = self.maindisplay.data_p[1:,:]
			self.maindisplay.data_f[0:-1,:] = self.maindisplay.data_f[1:,:]
				
			self.maindisplay.data_t[-1] = item[0]
			self.maindisplay.data_p[-1] = item[1]
			self.maindisplay.data_f[-1] = item[2]
				
			map(lambda n: self.maindisplay.curves_phase[n].setData(self.maindisplay.data_t, self.maindisplay.data_p[:,n]), range(0,11))
			map(lambda n: self.maindisplay.curves_freq[n].setData(self.maindisplay.data_t, self.maindisplay.data_f[:,n]), range(0,4))

		timer = QTimer()
		timer.timeout.connect( partial( updateInProc, self, q))
		timer.start(1)
		self.maindisplay.show()
		print(timer.isActive())
		print("Hello 2")
		self.exec_()


class MainDisplay(pg.GraphicsWindow):

	def __init__(self, el_net, proc_ev):
		
		super(MainDisplay, self).__init__()
		self.init_ui(el_net, proc_ev)

	# initalize my gui window	
	def init_ui(self, el_net, proc_ev):
		self.resize(2000,1000)
		self.setWindowTitle('Interacting swing dynamics')
	
		# Add items to the gui window
		self.p_phase = self.addPlot(title="Phase plot", row = 0, col=1)
		self.p_freq = self.addPlot(title="Frequency plot", row = 1, col=1)
		self.p_network = self.addViewBox(rowspan = 2, col=0)
		self.p_graph = pg.GraphItem()
		self.p_network.addItem(self.p_graph)
	
		# Plotting electrical network
		pos = np.array(el_net.get_coord())
		adj = np.array([[e[0],e[1]] for e in el_net.graph.edges])
		symbols = ['s' if el_net.graph.nodes[n]['sm'] else 'o' for n in el_net.graph.nodes]
		self.p_graph.setData(pos = pos, adj = adj, size = 20, symbol = symbols)
		
		self.p_network.scene().sigMouseClicked.connect(lambda mouse_ev: onClick(mouse_ev, el_net, proc_ev, self.p_network))
		self.show()
			
	
	
def onClick(mouse_ev, el_net, proc_ev, p_network):
	
	# Clear proc_event to stop simulation
	proc_ev.clear()
	
	# Node positions
	pos = np.array(el_net.get_coord())
	X, Y = pos[:,0], pos[:,1]
	
	# Retrieve mouse click position
	x = p_network.mapSceneToView(mouse_ev.pos()).x(),
	y = p_network.mapSceneToView(mouse_ev.pos()).y(),
	
	# Find node id
	node_id = np.nanargmin((X-x)**2+(Y-y)**2)
	print x,y, node_id
	
	New_UI = Entry(el_net.graph.nodes[node_id], proc_ev)	
	New_UI.show()

class Entry(QDialog):

	def __init__(self, node, proc_ev):
		
		super(Entry, self).__init__()
		
		# Entry window name
		self.setWindowTitle(node["name"])
		
		# Entry forms
		self.entry_power = QLineEdit()
		self.entry_power.setText(str(node["power"]))
		self.entry_power.setValidator(QDoubleValidator())
		
		self.entry_damping = QLineEdit()
		self.entry_damping.setText(str(node["damping"]))
		self.entry_damping.setValidator(QDoubleValidator(0.01,10,2))

		self.layout = QFormLayout()
		self.layout.addRow("Power", self.entry_power)
		self.layout.addRow("Damping", self.entry_damping)
	
		if node['sm'] == True:
			self.entry_inertia = QLineEdit()
			self.entry_inertia.setText(str(node["inertia"]))
			self.entry_inertia.setValidator(QDoubleValidator(0.01,10,2))
			self.layout.addRow("Inertia", self.entry_inertia)
		
		# Entry window set button
		self.button = QPushButton()
		self.button.setText("Set") 
		self.button.clicked.connect( partial( self.button_click, node) )	
		self.layout.addWidget(self.button)
		
		# Set entry window layout
		self.setLayout(self.layout)
		self.proc_ev = proc_ev
		
    # Assign entries to node properties
	def button_click(self, node):
		node['power'] = float(self.entry_power.text())
		node['damping'] = float(self.entry_damping.text())
		if hasattr(self, 'entry_inertia'):
			node['inertia'] = self.entry_inertia.text()
	
	# Set the event to restart simulation after closing dialog window
	def closeEvent(self, *args, **kwargs):
		super(QDialog, self).closeEvent(*args, **kwargs)
		print "you just closed the pyqt window!!! you are awesome!!!"
		self.proc_ev.set()
	
def main():
	
	# Intergers 0,1,2,3,4 are node ids. They can be replaced by other identifiers such as names
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
	
	app = QApplication(sys.argv)
	test = MainDisplay(el_net)
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()





