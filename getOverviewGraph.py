import json
import glob
import networkx as nx
from networkx.readwrite import json_graph
import Abnormal_Scenario_Generation as ASG

def get_data_list(url, tag):
    abnormal_files = glob.glob(url)
    data_list = []
    for index, filename in enumerate(abnormal_files):
        graph = nx.read_gml(filename)
        for node in graph.nodes():
            names = node.split('_')
            node_id = names[0]
            timestep = names[1]
            graph.node[node]['name'] = node_id
            graph.node[node]['originalID'] = node
            graph.node[node]['timestep'] = timestep
        data_item = {'id': tag + '_' + str(index), 'graph': json_graph.node_link_data(graph)}
        if tag == 'Abnormal':
            score_set, score_com = ASG.Detection_Outliers(graph)
            data_item['scores'] = []
            index = 0
            for score_i, s in enumerate(score_set):
                if score_i == 0:
                    data_item['abnormalScore'] = len(score_com[s])
                for com in score_com[s]:
                    data_item['scores'].append({'id': 'Group_' + str(index), 'score': s, 'nodes': com})
                    index += 1
        data_list.append(data_item)
    return data_list


if __name__ == '__main__':
    abnormal_url = './Abnormal/*.gml'
    normal_url = './Normal/*.gml'
    data_list = get_data_list(abnormal_url, 'Abnormal') + get_data_list(normal_url, 'Normal')
    with open('group-data.json', 'w') as output_file:
        json.dump(data_list, output_file)
