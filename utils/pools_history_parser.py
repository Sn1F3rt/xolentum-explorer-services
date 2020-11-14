#!/usr/bin/python3

import json
from pathlib import Path

import requests

pools = requests.get('https://raw.githubusercontent.com/xolentum/mining-pools-json/main/'
                     'xolentum-mining-pools.json').json()['pools']

with open(Path(__file__).parent / '../data/pools-history-data.json') as f:
    pools_history = json.load(f)

for pool in pools:
    if len(pools_history[pool['url']]) > 15:
        pools_history[pool['url']].pop(0)

    try:
        requests.get(pool['api'] if not isinstance(pool['api'], list) else pool['api'][0],
                     timeout=5)
        pools_history[pool['url']].append(1)

    except (requests.Timeout, requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout):
        pools_history[pool['url']].append(0)

pools_history = json.dumps(pools_history, indent=4)

with open(Path(__file__).parent / '../data/pools-history-data.json', 'w') as f:
    f.write(pools_history)

