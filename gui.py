from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyqtgraph as pg
import numpy as np
from graphs import *
from functools import partial
from dialog_ui import Dialog_edge, Dialog_node
from helper_fcts import *


class GuiThread(QThread):
	def __init__(self, el_net, proc_ev):
		QThread.__init__(self)
		self.maindisplay = MainDisplay(el_net, proc_ev)
		
	# Real time plotting of phase and frequency time series
	def display(self, q, proc_ev, plot_buffer = 1*1e03):
		
		# number of nodes and number of synchronous machines
		self.nb_sm = len(self.maindisplay.el_net.sm_id)
		self.nb_nodes = len(self.maindisplay.el_net.graph.nodes)
		
		self.maindisplay.curves_phase = [self.maindisplay.p_phase.plot() for n in range(self.nb_nodes)]
		self.maindisplay.curves_freq = [self.maindisplay.p_freq.plot() for n in range(self.nb_sm)]
		
		self.maindisplay.data_t = np.zeros(int(plot_buffer),dtype=float)
		self.maindisplay.data_p = np.zeros((int(plot_buffer), self.nb_nodes),dtype=float)
		self.maindisplay.data_f = np.zeros((int(plot_buffer), self.nb_sm),dtype=float)

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
			
			[self.maindisplay.curves_phase[n].setData(self.maindisplay.data_t, self.maindisplay.data_p[:,n]) for n in range(self.nb_nodes)]
			[self.maindisplay.curves_freq[n].setData(self.maindisplay.data_t, self.maindisplay.data_f[:,n]) for n in range(self.nb_sm)]
						
		self.timer = QTimer()
		self.timer.timeout.connect( partial( updateInProc, self, q))
		self.timer.start(1)
		self.start()


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
	
		# Uncomment to activate autorange plots
		#self.p_phase.disableAutoRange(axis= 'y')
		#self.p_phase.setYRange(-1, 1)
		self.p_freq.disableAutoRange(axis= 'y')
		self.p_freq.setYRange(-0.5,0.5)
		
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
	node_id, min_node_dist = shortest_distance(node_X,node_Y,x,y)
	edge_id, min_edge_dist = shortest_distance(edge_X,edge_Y,x,y)

	if min_node_dist < min_edge_dist:
		Dialog_node(el_net.graph.nodes[node_id], proc_ev)
	else:
		e = list(el_net.graph.edges())[edge_id]
		line_name = (el_net.graph.nodes[e[0]]['name'], el_net.graph.nodes[e[1]]['name'])
		Dialog_edge(el_net.graph[e[0]][e[1]], line_name, proc_ev)
	print "You just opened the entry dialog window!!! you are awesome!!!"

		
## Plotting line flows
def plot_line_flows(viewBox, el_net):
	
	line_flows = relative_line_load(el_net)
		
	for l in line_flows:
		arrow = pg.ArrowItem(angle = l['angle'], tipAngle = 40, headLen= 10, tailLen=0, pen={'color': 'w', 'width': 1}, brush = 'y')
		arrow.setPos(*l['pos'])
		arrow_label = pg.TextItem("{0:.0f}%".format(l['rel_load']))
		arrow_label.setPos(*l['pos'])
		viewBox.addItem(arrow)
		viewBox.addItem(arrow_label)
