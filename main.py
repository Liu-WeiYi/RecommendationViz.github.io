import networkx as nx
from networkx.readwrite import json_graph
import json


if __name__ == '__main__':
    abnormal_path = '../Abnormal/'
    filename = '9674.gml'
    graph = nx.read_gml(abnormal_path + filename)
    graph_dict = {}
    for node in graph.nodes():
        names = node.split('_')
        node_id = names[0]
        timestep = names[1]
        if timestep not in graph_dict:
            graph_dict[timestep] = nx.Graph()
        graph_dict[timestep].add_node(node_id)
    for edge in graph.edges(data=True):
        src_node = edge[0]
        tgt_node = edge[1]
        src_id = src_node.split('_')[0]
        tgt_id = tgt_node.split('_')[0]
        if src_id != tgt_id:
            timestep = src_node.split('_')[1]
            graph_dict[timestep].add_edge(src_id, tgt_id, weight=edge[2]['weight'])
    graph_list = [item[1] for item in sorted(graph_dict.iteritems(), key=lambda x: int(x[0]))]
    graph_list = [json_graph.node_link_data(item) for item in graph_list]
    with open(abnormal_path + '9674.json', 'w') as output_file:
        json.dump(graph_list, output_file)
