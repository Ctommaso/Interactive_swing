from PyQt4.QtGui import QDialog, QLineEdit, QFormLayout, QPushButton, QDoubleValidator, QCheckBox, QFileDialog
from functools import partial
from os import getcwd, path
import os, sys
import importlib
from load_data import load_csv


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
		print "You just closed the node-dialog window, simulation can continue!!!"



class Dialog_edge(QDialog):

	def __init__(self, edge, line_name, proc_ev):
		super(Dialog_edge, self).__init__()
		
		# Entry window name
		self.setWindowTitle("Line {}-{}".format(line_name[0],line_name[1]))
		
		# Entry forms
		self.entry_susceptance = QLineEdit()
		self.entry_susceptance.setText(str(edge["susceptance"]))
		self.entry_susceptance.setValidator(QDoubleValidator(0.01,10,2))
		
		self.entry_status = QCheckBox()
		self.entry_status.setChecked(edge["status"])
				
		self.layout = QFormLayout()
		self.layout.addRow("Susceptance", self.entry_susceptance)
		self.layout.addRow("Connected", self.entry_status)
			
		# Entry window set button
		self.button = QPushButton()
		self.button.setText("Set") 
		self.button.clicked.connect( partial( self.button_click, edge) )	
		self.layout.addWidget(self.button)
		
		# Set entry window layout
		self.setLayout(self.layout)
		
		self.proc_ev = proc_ev
		self.show()
	
	
    # Assign entries to edge properties
	def button_click(self, edge):
		edge['status'] = True if self.entry_status.checkState() == 2 else False
		edge['susceptance'] = float(self.entry_susceptance.text())
		print "New parameters set"
		print "susceptance {}, status {}".format(edge['susceptance'], edge['status'])  


	# Set the event to restart simulation after closing dialog window
	def closeEvent(self, *args, **kwargs):
		QDialog.closeEvent(self,*args, **kwargs)
		self.proc_ev.set()
		print "You just closed the edge-dialog window, simulation can continue!!!"



# Dialog window to select networks
def dialog_load_network():
	
	dir_name = 'network_data'
	
	if path.isdir(dir_name) == False:
		dir_name = getcwd()

	f_name = QFileDialog.getOpenFileName(None,'Load Electic Network', directory = dir_name, filter = "Network files *.csv")
	
	try:
		assert(os.path.exists(f_name))
	except AssertionError:
		sys.exit(' *** No file selected *** ')
	
	return load_csv(str(f_name))
