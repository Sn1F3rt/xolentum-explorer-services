#!/usr/bin/python3

import json
from pathlib import Path

import requests

with open('../config.json') as f:
    data = json.load(f)

    host = data['daemon_host']
    port = data['daemon_port']
    ssl = data['ssl']

blocks_data = list()

current_height = requests.get(f'{"https" if ssl else "http"}://{host}:{port}/get_info')\
    .json()['height']

for block_height in range(1, current_height + 1):
    # noinspection SpellCheckingInspection
    raw_data = requests.post(
        f'{"https" if ssl else "http"}://{host}:{port}/json_rpc',
        data={
            'jsonrpc': '2.0',
            'id': '0',
            'method': 'get_block_header_by_height',
            'params': {
                    'height': block_height
                    }
            },
        headers={
            'Content-type': 'application/json'
        }
    )\
        .json()['result']['block_header']

    # noinspection SpellCheckingInspection
    blocks_data.append(
        {
            'height': raw_data['height'],
            'already_generated_coins': raw_data['already_generated_coins'],
            'difficulty': raw_data['difficulty'],
            'num_txes': raw_data['num_txes'],
            'reward': raw_data['reward'],
            'timestamp': raw_data['timestamp']
        }
    )

blocks_data = json.dumps(blocks_data, indent=4)

with open(Path(__file__).parent / '../data/blocks-data.json', 'w') as f:
    f.write(blocks_data)
