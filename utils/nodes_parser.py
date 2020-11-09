#!/usr/bin/python3

import json
import requests


def get_info(node_host, node_port, ssl=False):
    info = requests.get(f'{"http" if not ssl else "https"}://{node_host}:{node_port}/get_info').json()

    return info['version'], info['height'], info['incoming_connections_count'], \
        info['outgoing_connections_count']


nodes = requests.get('https://raw.githubusercontent.com/xolentum/public-nodes-json/main/'
                     'xolentum-public-nodes.json').json()['nodes']

active_nodes = list()

for node in nodes:
    try:
        requests.get(f'{"http" if not node["ssl"] else "https"}://{node["url"]}:{node["port"]}/get_info',
                     timeout=5)
    except requests.Timeout:
        continue

    version, height, _in, out = get_info(node['url'], node['port'],
                                         True if node['ssl'] else False)

    active_nodes.append(
        {
            'name': node['name'],
            'host': node['url'],
            'port': node['port'],
            'ssl': node['ssl'],
            'version': version,
            'height': height,
            'in_conn': _in,
            'out_conn': out
        }
    )

active_nodes = json.dumps(active_nodes, indent=4)

with open('../data/nodes-data.json', 'w') as f:
    f.write(active_nodes)
