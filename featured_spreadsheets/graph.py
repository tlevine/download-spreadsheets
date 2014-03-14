import networx as nx

def new_graph():
    '''
    >>> new_graph().is_directed()
    False
    '''
    return nx.Graph()

def add_edge(graph:nx.Graph, unique_index:set, dataset_id:str):
    graph.add_edge(tuple(sorted(unique_index)),dataset_id)
    return graph
