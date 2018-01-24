from PyQt4.QtCore import QThread, QTimer
from pyqtgraph import GraphicsWindow, GraphItem, TextItem, ArrowItem
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
			
			self.maindisplay.p_lineflows.setData(self.maindisplay.el_net)
						
		self.timer = QTimer()
		self.timer.timeout.connect( partial( updateInProc, self, q))
		self.timer.start(1)
		self.start()


class MainDisplay(GraphicsWindow):

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
	
		self.p_lineflows = LineFlows(self.p_network, el_net)
		self.p_network.scene().sigMouseClicked.connect(lambda mouse_ev: onClick(mouse_ev, el_net, proc_ev, self.p_network))
	
		self.show()
	
	def closeEvent(self, *args, **kwargs):
		super(GraphicsWindow, self).closeEvent(*args, **kwargs)
		
	

class LabeledGraph(GraphItem):
	def __init__(self):
		GraphItem.__init__(self)
        
	def setData(self, **kwds):
		self.data = kwds
		if 'pos' in self.data:
			for n in range(kwds['pos'].shape[0]):
				text_item = TextItem(kwds['text'][n])
				text_pos = (kwds['pos'][n][0], kwds['pos'][n][1])
				text_item.setPos(*kwds['pos'][n])
				text_item.setParentItem(self)
		self.text = kwds.pop('text', [])
		GraphItem.setData(self, **self.data)
    
	
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
	x = p_network.mapToView(mouse_ev.scenePos()).x(),
	y = p_network.mapToView(mouse_ev.scenePos()).y(),
	
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
class LineFlows():
	
	
	def __init__(self, viewBox, el_net):
		
		self.arrows = []
		self.arrow_labels = []
		self.line_flows = relative_line_load(el_net)
		
		for l in self.line_flows:
			arrow = ArrowItem(angle = l['angle'], tipAngle = 40, headLen= 10, tailLen=0, pen={'color': 'w', 'width': 1}, brush = 'y', pxMode = True)
			arrow.setPos(*l['pos'])
			arrow_label = TextItem("{0:.0f}%".format(l['rel_load']))
			arrow_label.setPos(*l['pos'])
			viewBox.addItem(arrow)
			viewBox.addItem(arrow_label)
			self.arrows.append(arrow)
			self.arrow_labels.append(arrow_label)
	
	
	def setData(self, el_net):
		
		self.line_flows = relative_line_load(el_net)
		
		for n, l in enumerate(self.line_flows):
			angle_rot = -self.arrows[n].opts['angle'] + l['angle']
			self.arrows[n].rotate(angle_rot)
			self.arrows[n].opts.update(angle = l['angle'])
			self.arrow_labels[n].setText("{0:.0f}%".format(l['rel_load']))
