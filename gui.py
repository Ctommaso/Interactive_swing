from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import multiprocessing

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

def display(q, el_net, proc_ev, plot_buffer = 3*1e03):

	# gui window
	win = pg.GraphicsWindow()
	win.resize(2000,1000)
	win.setWindowTitle('Interacting swing dynamics')
	
	# Add items to the gui window
	p_phase = win.addPlot(title="Phase plot", row = 0, col=1)
	p_freq = win.addPlot(title="Frequency plot", row = 1, col=1)
	p_network = win.addViewBox(rowspan = 2, col=0)
	p_graph = pg.GraphItem()
	p_network.addItem(p_graph)
	#win.addItem(p_graph)
	
	# Plotting electrical network
	pos = np.array(el_net.get_coord())
	adj = np.array([[e[0],e[1]] for e in el_net.graph.edges])
	symbols = ['s' if el_net.graph.nodes[n]['sm'] else 'o' for n in el_net.graph.nodes]
	p_graph.setData(pos = pos, adj = adj, size = 20, symbol = symbols, pxMode = True)
	
	# Response to click events
	p_network.scene().sigMouseClicked.connect(lambda mouse_ev: onClick(mouse_ev, proc_ev, el_net, p_network))
	
	# Real time plotting of phase and frequency time series
	curves_phase = [p_phase.plot() for n in range(0,11)]
	curves_freq = [p_freq.plot() for n in range(0,4)]
	
	data_t = np.zeros(int(plot_buffer),dtype=float)
	data_p = np.zeros((int(plot_buffer),11),dtype=float)
	data_f = np.zeros((int(plot_buffer),4),dtype=float)
	
	def updateInProc(curves_phase, q, data_t, data_p):
		if q.empty():
			return
			
		item = q.get()
		data_t[0:-1] = data_t[1:]
		data_p[0:-1,:] = data_p[1:,:]
		data_f[0:-1,:] = data_f[1:,:]
		
		data_t[-1] = item[0]
		data_p[-1] = item[1]
		data_f[-1] = item[2]
		
		map(lambda n: curves_phase[n].setData(data_t, data_p[:,n]), range(0,11))
		map(lambda n: curves_freq[n].setData(data_t, data_f[:,n]), range(0,4))
				
	timer = QtCore.QTimer()
	timer.timeout.connect(lambda: updateInProc(curves_phase, q, data_t, data_p))
	timer.start(0)

	QtGui.QApplication.instance().exec_()


def onClick(mouse_ev, proc_ev, el_net, p_network):
	
	
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
	
