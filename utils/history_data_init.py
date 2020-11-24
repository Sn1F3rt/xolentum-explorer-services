#!/usr/bin/python3

import json
from pathlib import Path

import requests

nodes = requests.get('https://raw.githubusercontent.com/xolentum/public-nodes-json/main/'
                     'xolentum-public-nodes.json').json()['nodes']

nodes_history = dict()

for node in nodes:
    nodes_history[node['url']] = list()

nodes_history = json.dumps(nodes_history, indent=4)


with open(Path(__file__).parent / '../data/nodes-history-data.json', 'w') as f:
    f.write(nodes_history)

pools = requests.get('https://raw.githubusercontent.com/xolentum/mining-pools-json/main/'
                     'xolentum-mining-pools.json').json()['pools']

pools_history = dict()

for pool in pools:
    pools_history[pool['url']] = list()

pools_history = json.dumps(pools_history, indent=4)

with open(Path(__file__).parent / '../data/pools-history-data.json', 'w') as f:
    f.write(pools_history)
