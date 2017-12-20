
import numpy as np

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

df=pd.read_csv('author_list.txt',names=['lastname','firstname'])

df['community']=0
adj = np.load('network.npy')



G = nx.from_numpy_matrix(adj)




labels={}

for ind,author in df.iterrows():
    if np.sum(adj[:,ind]):
        labels[ind]=author.lastname

G.remove_nodes_from(nx.isolates(G))
pos=nx.spring_layout(G,k=0.05,iterations=200) # positions for all nodes

#plt.show()
#nx.draw(G)
#plt.draw()
#plt.axis('equal')

#from scipy.cluster import hierarchy
#from scipy.spatial import distance
#
#
#path_length=nx.all_pairs_shortest_path_length(G)
#n = len(G.nodes())
#distances=np.zeros((n,n))
#for u,p in path_length.items():
#	 for v,d in p.items():
#	 	 distances[int(u)-1][int(v)-1] = d
#sd = distance.squareform(distances)
#
#hier = hierarchy.average(sd)	
#
#hierarchy.dendrogram(hier)
#plt.savefig("tree.png",format="png")

import community

parts = community.best_partition(G)
values = [parts.get(node) for node in G.nodes()]



#values = [val_map.get(node, 0.25) for node in G.nodes()]

#nx.draw(G, cmap=plt.get_cmap('jet'), node_color=values)
nx.draw_networkx_nodes(G,pos, cmap=plt.get_cmap('viridis'), node_color=values)
nx.draw_networkx_edges(G,pos)
nx.draw_networkx_labels(G,pos,labels,font_size=8)
plt.show()

i=0
for key, value in labels.items():
    print( value, ',',values[i])
    i+=1


