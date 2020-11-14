#!/usr/bin/python3

import json
from pathlib import Path

import requests

nodes = requests.get('https://raw.githubusercontent.com/xolentum/public-nodes-json/main/'
                     'xolentum-public-nodes.json').json()['nodes']

with open(Path(__file__).parent / '../data/nodes-history-data.json') as f:
    nodes_history = json.load(f)

for node in nodes:
    if len(nodes_history[node['url']]) > 15:
        nodes_history[node['url']].pop(0)

    try:
        requests.get(f'{"http" if not node["ssl"] else "https"}://{node["url"]}:{node["port"]}/get_info',
                     timeout=5)
        nodes_history[node['url']].append(1)

    except (requests.Timeout, requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout):
        nodes_history[node['url']].append(0)

nodes_history = json.dumps(nodes_history, indent=4)

with open(Path(__file__).parent / '../data/nodes-history-data.json', 'w') as f:
    f.write(nodes_history)

