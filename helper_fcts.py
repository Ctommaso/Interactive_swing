import numpy as np


def shortest_distance(X,Y,x,y):
	
	euclidean_distance = (X-x)**2+(Y-y)**2
	idx = np.nanargmin(euclidean_distance)
	min_dist = euclidean_distance[idx]
	return idx, min_dist


def relative_line_load(el_net):
	
	I = el_net.incidence
	
	line_load = el_net.get_active_susceptance().dot(np.sin(I.transpose().dot(el_net.state.phase)))
	rel_load = 100. * line_load / el_net.get_susceptance().diagonal()
		
	# Map rel_load line loads to their sign
	sgn = [1 if rel_load[n] > 0 else -1 for n in range(len(rel_load))]
	rel_load = abs(rel_load)

	node_coord = el_net.node_coord
	edge_coord = el_net.edge_coord
	
	line_flows = []

	# id of node emitting te power
	# unweighted incidence in shape (|nodes| x |edges|), column ordering is produced by graph.edges
	for n, v in enumerate(sgn):
		col = np.squeeze(I[:,n].toarray())
		from_id = np.where(col == v)[0]
		to_id = np.where(col == -v)[0]
		x, y = (node_coord[to_id] - node_coord[from_id])[0]
		angle = - np.arctan2(y, x)*180./np.pi + 180.
		line_flows.append({"from" : from_id, "to": to_id, "pos": edge_coord[n], 
		                   "angle": angle, "rel_load" : rel_load[n]})
	return line_flows


def steady_state_PF(theta, *args):
	
	el_net = args[0]
	P = args[1]
	
	susc = el_net.get_active_susceptance()
	I = el_net.incidence
	return P - (I.dot(susc)).dot(np.sin((I.transpose()).dot(theta)))
