from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

def display(name, q, el_net, plot_buffer = 3*1e03):
	app2 = QtGui.QApplication([])

	win = pg.GraphicsWindow()
	win.resize(2000,1000)
	win.setWindowTitle('Interacting swing dynamics')
	p_phase = win.addPlot(title="Phase plot", row = 0, col=1)
	p_freq = win.addPlot(title="Frequency plot", row = 1, col=1)
	p_network = win.addViewBox(rowspan = 2, col=0)
	
	print(type(p_network))
	
	p_graph = pg.GraphItem()
	p_network.addItem(p_graph)
	
	pos = np.array(el_net.get_coord())
	adj = np.array([[e[0],e[1]] for e in el_net.graph.edges])
	symbols = ['s' if el_net.graph.nodes[n]['sm'] else 'o' for n in el_net.graph.nodes]
	p_graph.setData(pos = pos, adj = adj, size = 20, symbol = symbols, pxMode = True)
	#p_graph.sigClicked.connect(clicked)
	
	curves_phase = [p_phase.plot() for n in range(0,11)]
	curves_freq = [p_freq.plot() for n in range(0,4)]
	
	data_t = np.zeros(int(plot_buffer),dtype=float)
	data_p = np.zeros((int(plot_buffer),11),dtype=float)
	data_f = np.zeros((int(plot_buffer),4),dtype=float)
	
	def updateInProc(curves_phase, q, data_t, data_p):
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




#lastClicked = []
def clicked(plot, points):
	print(points)
	"""
	global lastClicked
	for p in lastClicked:
		p.resetPen()
	print("clicked points", points)
	for p in points:
		p.setPen('b', width=2)
	lastClicked = points
	"""
