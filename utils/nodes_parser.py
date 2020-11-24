#!/usr/bin/python3

import json
from pathlib import Path
import urllib3

import requests


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_info(node_host, node_port, ssl=False):
    info = requests.get(f'{"http" if not ssl else "https"}'
                        f'://{node_host}:{node_port}/get_info', verify=False).json()

    return info['version'], info['height'], info['incoming_connections_count'], \
        info['outgoing_connections_count']


nodes = requests.get('https://raw.githubusercontent.com/xolentum/public-nodes-json/main/'
                     'xolentum-public-nodes.json').json()['nodes']

active_nodes = list()

for node in nodes:
    # noinspection PyBroadException
    try:
        requests.get(f'{"http" if not node["ssl"] else "https"}://{node["url"]}:{node["port"]}/get_info',
                     verify=False, timeout=5)

    except:
        continue

    version, height, _in, out = get_info(node['url'], node['port'],
                                         True if node['ssl'] else False)

    with open(Path(__file__).parent / '../data/nodes-history-data.json') as f:
        history = json.load(f)

    try:
        active_nodes.append(
            {
                'name': node['name'],
                'host': node['url'],
                'port': node['port'],
                'ssl': node['ssl'],
                'version': version,
                'height': height,
                'in_conn': _in,
                'out_conn': out,
                'history': history[node['url']]
            }
        )

    except IndexError:
        pass

active_nodes = json.dumps(active_nodes, indent=4)

with open(Path(__file__).parent / '../data/nodes-data.json', 'w') as f:
    f.write(active_nodes)
