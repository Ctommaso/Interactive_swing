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
		self.timer.start(1)
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
		#self.p_phase.disableAutoRange(axis= 'y')
		#self.p_phase.setYRange(-0.5,0.5)
		
		self.p_freq = self.addPlot(title="Frequency plot", row = 1, col=1)
		#self.p_freq.disableAutoRange(axis= 'y')
		#self.p_freq.setYRange(-0.4,0.4)
		
		self.p_network = self.addViewBox(rowspan = 2, col=0)
		self.p_graph = LabeledGraph()
		self.p_network.addItem(self.p_graph)
	
		# Plotting electrical network
		pos = el_net.node_coord
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
		#self.text = kwds.pop('text', [])
		self.text = kwds.pop('text', [])
		pg.GraphItem.setData(self, **self.data)
    
	
def onClick(mouse_ev, el_net, proc_ev, p_network):
	
	# Clear proc_event to stop simulation
	proc_ev.clear()
	
	# Node positions
	node_pos = el_net.node_coord
	node_X, node_Y = node_pos[:,0], node_pos[:,1]
	
	# Edge positions
	edge_pos = el_net.edge_coord
	edge_X, edge_Y = edge_pos[:,0], edge_pos[:,1]

	# Retrieve mouse click position
	x = p_network.mapSceneToView(mouse_ev.pos()).x(),
	y = p_network.mapSceneToView(mouse_ev.pos()).y(),
	
	# Find id and min distance
	node_id, min_node_dist = closest_distance(node_X,node_Y,x,y)
	edge_id, min_edge_dist = closest_distance(edge_X,edge_Y,x,y)
	"""
	if min_node_dist < min_edge_dist:
		Dialog_node(el_net.graph.nodes[node_id], proc_ev)
	else:
		e = list(el_net.graph.edges())[edge_id]
		line_name = (el_net.graph.nodes[e[0]]['name'], el_net.graph.nodes[e[1]]['name'])
		Dialog_edge(el_net.graph[e[0]][e[1]], line_name, proc_ev)
	"""
	if min_node_dist > min_edge_dist:
		e = list(el_net.graph.edges())[edge_id]
		line_name = (el_net.graph.nodes[e[0]]['name'], el_net.graph.nodes[e[1]]['name'])
		Dialog_edge(el_net.graph[e[0]][e[1]], line_name, proc_ev)	
	else:
		Dialog_node(el_net.graph.nodes[node_id], proc_ev)

	print "You just opened the entry dialog window!!! you are awesome!!!"


def closest_distance(X,Y,x,y):
	euclidean_distance = (X-x)**2+(Y-y)**2
	idx = np.nanargmin(euclidean_distance)
	min_dist = euclidean_distance[idx]
	return idx, min_dist

	
class Dialog_node(QDialog):

	def __init__(self, node, proc_ev):
		super(Dialog_node, self).__init__()
		
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
		self.show()
		
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
		QDialog.closeEvent(self,*args, **kwargs)
		self.proc_ev.set()
		print "You just closed the entry dialog window!!! simulation can continue!!!"


class Dialog_edge(QDialog):

	def __init__(self, edge, line_name, proc_ev):
		super(Dialog_edge, self).__init__()
		
		print "CAZZO", "Line {}-{}".format(line_name[0],line_name[1])
		# Entry window name
		self.setWindowTitle("Line {}-{}".format(line_name[0],line_name[1]))
		
		# Entry forms
		self.entry_susceptance = QLineEdit()
		self.entry_susceptance.setText(str(edge["susceptance"]))
		self.entry_susceptance.setValidator(QDoubleValidator())
		
		
		self.entry_status = QLineEdit()
		self.entry_status.setText(str(edge["status"]))
		self.entry_status.setValidator(QDoubleValidator(0.01,10,2))
		"""
		self.entry_status = QCheckBox()
		self.entry_status.setChecked(True)
		"""
		self.layout = QFormLayout()
		self.layout.addRow("Susceptance", self.entry_susceptance)
		self.layout.addRow("Connected", self.entry_status)
			
		# Entry window set button
		self.button = QPushButton()
		self.button.setText("Set") 
		#self.button.clicked.connect( partial( self.button_click, edge) )	
		self.layout.addWidget(self.button)
		
		# Set entry window layout
		self.setLayout(self.layout)
		
		self.proc_ev = proc_ev
		self.show()
		
	"""
    # Assign entries to node properties
	def button_click(self, edge):
		
		edge['susceptance'] = self.entry_power.text())
		edge['damping'] = float(self.entry_damping.text())
		if hasattr(self, 'entry_inertia'):
			node['inertia'] = float(self.entry_inertia.text())
		
		print "New parameters set"
		print "P {} ".format(node['power'])  
		print "D {}, ".format(node['damping'])  
		if hasattr(self, 'entry_inertia'):
			print "I {}".format(node['inertia'])
		

	# Set the event to restart simulation after closing dialog window
	def closeEvent(self, *args, **kwargs):
		QDialog.closeEvent(self,*args, **kwargs)
		self.proc_ev.set()
		print "You just closed the entry dialog window!!! simulation can continue!!!"
	"""

