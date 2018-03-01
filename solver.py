import numpy as np
import time


class Simulator():
	
	""" Simulation object: 
	
	inputs: electrical network object,
	        integer max_iterations, 
	        fct for time integration time_integrator
	        time integrator time step
	"""
	
	def __init__(self, el_network, time_integrator , max_iter = 1e6, time_step = 1e-2):
		self.max_iter = max_iter
		self.time_integrator = time_integrator
		self.el_network = el_network
		self.time_step = time_step
		
	def start(self, queue, ev):
		print('started sim')
		return self.time_integrator(self.el_network, self.max_iter, self.time_step, queue, ev)


def RK(el_network, max_iter, time_step, queue, ev):
	
	print('welcome to RK')
	
	sm_id = getattr(el_network, 'sm_id')	
	nb_nodes = el_network.graph.number_of_nodes()
	state = el_network.state
	rk_state = np.concatenate((state.phase, state.frequency[sm_id]))
	
	step = 0
	
	while(step < max_iter):
		
		queue.put([step * time_step, rk_state[0:nb_nodes], rk_state[nb_nodes:]])
		time.sleep(0.05)
		el_network.state.phase = rk_state[0:nb_nodes]
		el_network.state.frequency[sm_id] = rk_state[nb_nodes:]
		
		# wait() method blocks until the flag is true
		ev.wait()
		
		
		# 4th order Runge Kutta (1st order DE)
		k1 = time_step * swing_eq(rk_state, el_network)
		k2 = time_step * swing_eq(rk_state + k1/2., el_network)
		k3 = time_step * swing_eq(rk_state + k2/2., el_network)
		k4 = time_step * swing_eq(rk_state + k3, el_network)

		rk_state = rk_state + (k1 + 2 * k2 + 2* k3 + k4) / 6.
		step += 1

	print 'Finished time integration'
		
		
def swing_eq(rk_state, el_network):
		
	# sync_machines and load ids
	sm_id = getattr(el_network, 'sm_id')
	load_id = getattr(el_network, 'load_id')
	
	nb_nodes = el_network.graph.number_of_nodes()
	
	# Swing equation coefficients
	# Coefficients are ordered according to sm_id and load_id
	M_sm = el_network.get_I_sm() # Inertia sync machines
	D_sm = el_network.get_D_sm() # Damping sync machines
	D_load = el_network.get_D_load() # Damping loads
	
	# Vector of injections, ordered according to the node labelling
	P = el_network.get_P()
	
	# incidence matrix, and edge susceptances constructed from the node ordering 
	I = getattr(el_network, 'incidence')
	susc = el_network.get_active_susceptance()
	#print "in swing eq"
	#print np.diag(susc.todense())
	#print el_network.graph.edges
	
	# Power imbalance, rk_state = [theta, frequency_sm], with:
	# theta ordered according to node ordering
	# frequency_sm ordered according to sm_id
	phase_diff = (I.transpose()).dot(rk_state[0:nb_nodes])
	sin_phase_diff = np.sin(phase_diff)
	delta_P = P - (I.dot(susc)).dot(sin_phase_diff)
	
	# rk_state = [theta, frequency_sm]
	delta_phase = np.zeros(nb_nodes)
	delta_phase[sm_id] = rk_state[nb_nodes:] 
	delta_phase[load_id] = delta_P[load_id] / D_load
	delta_freq_sm = ( - D_sm * rk_state[nb_nodes:] + delta_P[sm_id]) / M_sm

	delta_rk_state = np.concatenate((delta_phase, delta_freq_sm))
	
	return delta_rk_state


