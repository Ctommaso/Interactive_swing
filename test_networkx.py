import networkx as nx
from scipy.sparse import diags
import matplotlib.pyplot as plt


# Script to test basic networkx functions

 
def main():
	
	G = nx.Graph()
	# Intergers 0,1,2,3,4 are node ids. They can be replaced by other identifiers such as names
	G.add_nodes_from([(0,{'coord': [0.0, 0.0], 'sm': True, 'power':10, 'inertia':0.4, 'damping':0.04}),
	                  (1,{'coord': [0.1, 0.1], 'sm': True, 'power':10, 'damping':0.11}),
	                  (2,{'coord': [0.2, 0.2], 'sm': True, 'power':10, 'damping':0.33}),
	                  (3,{'coord': [0.3, 0.3], 'sm': True, 'power':10, 'inertia':0.9, 'damping':0.09}),
	                  (4,{'coord': [0.4, 0.4], 'sm': True, 'power':10, 'inertia':1.4, 'damping':0.14})])
	
	G.add_edges_from([(0,1,{'weight':2}),(0,2,{'weight':1}),(0,3,{'weight':7}),(1,2,{'weight':3}),
	                  (2,3,{'weight':4}),(3,4,{'weight':1})])
	
	print "Nodes", G.nodes()
	print "Number of nodes is {}". format(G.number_of_nodes())
	print "Edges", G.edges()

	print "Sync Machines id", filter(lambda n: G.nodes[n]['sm']==True, G.nodes)
	load_id = filter(lambda n: G.nodes[n]['sm']==False, G.nodes)
	print "Load id", load_id
	print "Load dampings", [G.nodes[n]['damping'] for n in load_id]
	
	print "Node positions", map(lambda n: G.nodes[n]['coord'], G.nodes)
	
	# Incidence in R^(|nodes| x |edges|), column ordering is produced by G.edges
	I = nx.linalg.graphmatrix.incidence_matrix(G, oriented = True)
	print(type(I))
	print(type(I.transpose()))
	print(I.todense())
	
	e_w = [G[e[0]][e[1]]['weight'] for e in G.edges()]
	print "Edge_weights", e_w
	
	print(diags(e_w))
	print(type(diags(e_w)))
	 
	print("Unweighted Laplacian")
	print((I*I.transpose()).todense())
	print("Weighted Laplacian")
	print((I*diags(e_w)*I.transpose()).todense())
	
	nx.draw_networkx(G)
	plt.show()
if __name__ == '__main__':
	main()
