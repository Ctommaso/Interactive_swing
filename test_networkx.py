import networkx as nx
from scipy.sparse import diags

def main():
	
	G = nx.Graph()
	# Intergers 0,1,2,3,4 are node ids. They can be replaced by other identifiers such as names
	G.add_nodes_from([(0,{'coord_x': 0.0}),(1,{'coord_x': 0.1}),(2,{'coord_x': 0.2}),
	                  (3,{'coord_x': 0.3}),(4,{'coord_x': 0.4})])
	G.add_edges_from([(0,1,{'weight':2}),(0,2,{'weight':1}),(0,3,{'weight':7}),(1,2,{'weight':3}),
	                  (2,3,{'weight':4}),(3,4,{'weight':1})])
	
	print "Nodes", G.nodes()
	print "Number of nodes is {}". format(G.number_of_nodes())
	print "Nodes", type(G.nodes())
	print "Edges", G.edges()


	print "Node positions", [G.nodes[n]['coord_x'] for n in G.nodes]
	print "Node positions", map(lambda n: G.nodes[n]['coord_x'], G.nodes)
	
	
	
	# Incidence in R^(|nodes| x |edges|), column ordering is produced by G.edges
	"""
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
	"""
if __name__ == '__main__':
	main()
