import networkx

def graph(datasets):
    g = networkx.Graph()
    for dataset in datasets:
        for unique_index in dataset['unique_indices']:
            g.add_edge(datasetid, unique_index)
    return g
