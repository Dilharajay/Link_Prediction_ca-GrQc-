import gzip
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

G = nx.Graph()
with gzip.open('../data/raw/ca-GrQc.txt.gz', 'rt') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        a, b = map(int, line.split())
        if a == b:
            continue
        G.add_edge(a, b)

deg = dict(G.degree())
center = max(deg, key=deg.get)
print("center", center, "degree", deg[center])

neighbors = list(G.neighbors(center))
nodes = [center] + neighbors
H = G.subgraph(nodes).copy()
print("ego network nodes:", H.number_of_nodes(), "edges:", H.number_of_edges())

pos = nx.spring_layout(H, seed=42, k=0.55, iterations=120)

fig, ax = plt.subplots(figsize=(9, 8))
nx.draw_networkx_edges(H, pos, ax=ax, edge_color='#c9c9c9', width=0.7, alpha=0.7)
non_center = [n for n in H.nodes() if n != center]
nx.draw_networkx_nodes(H, pos, nodelist=non_center, ax=ax,
                       node_size=[80 + 6*deg[n] for n in non_center],
                       node_color=[deg[n] for n in non_center],
                       cmap=plt.cm.viridis, alpha=0.85, linewidths=0.4,
                       edgecolors='#333333')
nx.draw_networkx_nodes(H, pos, nodelist=[center], ax=ax,
                       node_size=950, node_color='#d62728',
                       edgecolors='black', linewidths=1.3)
ax.set_title('Ego-network of the highest-degree author (node %d, degree %d)' % (center, deg[center]))
ax.axis('off')
plt.tight_layout()
plt.savefig('results/figures/network_visualization.png', dpi=180, bbox_inches='tight')
print("saved results/figures/network_visualization.png")
