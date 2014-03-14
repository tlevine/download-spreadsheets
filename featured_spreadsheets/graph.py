import networx as nx

class Graph(nx.Graph):
    def add_index(self, unique_index:set, dataset_id:str):
        self.add_edge(tuple(sorted(unique_index)),dataset_id)
