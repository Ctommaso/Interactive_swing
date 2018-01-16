from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyqtgraph as pg
import numpy as np
import multiprocessing, sys
from graphs import *
from functools import partial
from multiprocessing import Event

class GuiThread(QThread):
	def __init__(self, el_net, proc_ev):
		QThread.__init__(self)
		self.maindisplay = MainDisplay(el_net, proc_ev)
		
	# Real time plotting of phase and frequency time series
	def display(self, q, proc_ev, plot_buffer = 3*1e03):
		
		# number of nodes and number of synchronous machines
		self.nb_sm = len(self.maindisplay.el_net.sm_id)
		self.nb_nodes = len(self.maindisplay.el_net.graph.nodes)
		
		self.maindisplay.curves_phase = [self.maindisplay.p_phase.plot() for n in range(self.nb_nodes)]
		self.maindisplay.curves_freq = [self.maindisplay.p_freq.plot() for n in range(self.nb_sm)]
		
		self.maindisplay.data_t = np.zeros(int(plot_buffer),dtype=float)
		self.maindisplay.data_p = np.zeros((int(plot_buffer),11),dtype=float)
		self.maindisplay.data_f = np.zeros((int(plot_buffer),4),dtype=float)

		def updateInProc(self, q):
			if q.empty():
				return
					
			item = q.get()
			self.maindisplay.data_t[0:-1] = self.maindisplay.data_t[1:]
			self.maindisplay.data_p[0:-1,:] = self.maindisplay.data_p[1:,:]
			self.maindisplay.data_f[0:-1,:] = self.maindisplay.data_f[1:,:]
				
			self.maindisplay.data_t[-1] = item[0]
			self.maindisplay.data_p[-1] = item[1]
			self.maindisplay.data_f[-1] = item[2]
			
			map(lambda n: self.maindisplay.curves_phase[n].setData(self.maindisplay.data_t, self.maindisplay.data_p[:,n]), range(self.nb_nodes))
			map(lambda n: self.maindisplay.curves_freq[n].setData(self.maindisplay.data_t, self.maindisplay.data_f[:,n]), range(self.nb_sm))
			
		self.timer = QTimer()
		self.timer.timeout.connect( partial( updateInProc, self, q))
		self.timer.start(100)
		self.exec_()
		

class MainDisplay(pg.GraphicsWindow):

	def __init__(self, el_net, proc_ev):
		
		super(MainDisplay, self).__init__()
		self.init_ui(el_net, proc_ev)

	# initalize my gui window	
	def init_ui(self, el_net, proc_ev):
		self.resize(2000,1000)
		self.setWindowTitle('Interacting swing dynamics')
		self.el_net = el_net
		
		# Add items to the gui window
		self.p_phase = self.addPlot(title="Phase plot", row = 0, col=1)
		self.p_freq = self.addPlot(title="Frequency plot", row = 1, col=1)
		self.p_network = self.addViewBox(rowspan = 2, col=0)
		self.p_graph = LabeledGraph()
		self.p_network.addItem(self.p_graph)
	
		# Plotting electrical network
		pos = np.array(el_net.get_coord())
		adj = np.array([[e[0],e[1]] for e in el_net.graph.edges])
		labels = np.array([el_net.graph.nodes[n]['name'] for n in el_net.graph.nodes])
		symbols = ['s' if el_net.graph.nodes[n]['sm'] else 'o' for n in el_net.graph.nodes]
		self.p_graph.setData(pos = pos, adj = adj, size = 20, symbol = symbols, text = labels)
		
		self.p_network.scene().sigMouseClicked.connect(lambda mouse_ev: onClick(mouse_ev, el_net, proc_ev, self.p_network))
		self.show()
	
	def closeEvent(self, *args, **kwargs):
		super(pg.GraphicsWindow, self).closeEvent(*args, **kwargs)
		
	

class LabeledGraph(pg.GraphItem):
	def __init__(self):
		pg.GraphItem.__init__(self)
        
	def setData(self, **kwds):
		self.data = kwds
		if 'pos' in self.data:
			for n in range(kwds['pos'].shape[0]):
				text_item = pg.TextItem(kwds['text'][n])
				text_pos = (kwds['pos'][n][0], kwds['pos'][n][1])
				text_item.setPos(*kwds['pos'][n])
				text_item.setParentItem(self)
		self.text = kwds.pop('text', [])
		pg.GraphItem.setData(self, **self.data)
    
	
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
	
	New_UI = Entry(el_net.graph.nodes[node_id], proc_ev)	
	New_UI.show()
	print "You just opened the entry dialog window!!! you are awesome!!!"

	
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
			node['inertia'] = float(self.entry_inertia.text())
		
		print "New parameters set"
		print "P {} ".format(node['power'])  
		print "D {}, ".format(node['damping'])  
		if hasattr(self, 'entry_inertia'):
			print "I {}".format(node['inertia'])
		

	# Set the event to restart simulation after closing dialog window
	def closeEvent(self, *args, **kwargs):
		super(QDialog, self).closeEvent(*args, **kwargs)
		self.proc_ev.set()
		print "You just closed the entry dialog window!!! simulation can continue!!!"

