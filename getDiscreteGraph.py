import glob
import networkx as nx
from networkx.readwrite import json_graph
#  import Abnormal_Scenario_Generation as ASG
import json

def get_data_list(url, tag):
    abnormal_files = glob.glob(url)
    data_list = []
    for index, filename in enumerate(abnormal_files):
        graph = nx.read_gml(filename)
        graph_dict = {}
        for node in graph.nodes():
            names = node.split('_')
            node_id = names[0]
            timestep = names[1]
            if timestep not in graph_dict:
                graph_dict[timestep] = nx.Graph()
            graph_dict[timestep].add_node(node_id)
            graph_dict[timestep].nodes[node_id]['name'] = node_id
            graph_dict[timestep].nodes[node_id]['originalID'] = node
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
        data_item = {'id': tag + '_' + str(index), 'graph': graph_list}
        data_list.append(data_item)
    return data_list


if __name__ == '__main__':
    abnormal_url = './Abnormal/*.gml'
    normal_url = './Normal/*.gml'
    data_list = get_data_list(abnormal_url, 'Abnormal') + get_data_list(normal_url, 'Normal')
    with open('single-data.json', 'w') as output_file:
        json.dump(data_list, output_file)
