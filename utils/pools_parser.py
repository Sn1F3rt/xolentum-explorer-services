#!/usr/bin/python3

import math
import json
import requests


def cn_js_info(api_url):
    info = requests.get(api_url).json()

    _height = info['network']['height']
    _hash_rate = info['pool']['hashrate']
    _miners = info['pool']['miners']
    _fee = info['config']['fee']
    _min_payout = info['config']['minPaymentThreshold'] / math.pow(10, 12)
    _last_block = info['lastblock']['timestamp']

    return _height, _hash_rate, _miners, _fee, _min_payout, _last_block


def rplant_info(api_url):
    info = requests.get(api_url).json()['pools']['xolentum']

    _height = info['poolStats']['networkBlocks']
    _hash_rate = info['hashrate']
    _miners = info['poolStats']['minerCount']
    _fee = info['fee']
    _min_payout = info['minimumPayment']
    # _last_block = info['lastblock']['timestamp']
    _last_block = 123456890

    return _height, _hash_rate, _miners, _fee, _min_payout, _last_block


def gntl_info(api_urls):
    info = requests.get(api_urls[0]).json()['pool_statistics']

    _hash_rate = info['hashRate']
    _miners = info['miners']
    _last_block = info['lastBlockFoundTime']

    info = requests.get(api_urls[1]).json()

    _height = info['height']

    info = requests.get(api_urls[2]).json()

    _fee = f'{info["pplns_fee"]}% PPLNS'
    _min_payout = info['min_wallet_payout'] / math.pow(10, 12)

    return _height, _hash_rate, _miners, _fee, _min_payout, _last_block


pools = requests.get('https://raw.githubusercontent.com/xolentum/mining-pools-json/main/'
                     'xolentum-mining-pools.json').json()['pools']

active_pools = list()

for pool in pools:
    try:
        requests.get(pool['api'] if not isinstance(pool['api'], list) else pool['api'][0])
    except requests.Timeout:
        continue

    if pool['type'] == 'cn-js':
        height, hash_rate, miners, fee, min_payout, last_block = cn_js_info(pool['api'])

    elif pool['type'] == 'other':
        if 'gntl' in pool['name'].lower():
            height, hash_rate, miners, fee, min_payout, last_block = gntl_info(pool['api'])

        elif 'rplant' in pool['name'].lower():
            height, hash_rate, miners, fee, min_payout, last_block = rplant_info(pool['api'])

        else:
            continue

    else:
        continue

    # noinspection PyUnboundLocalVariable
    active_pools.append(
        {
            'name': pool['name'],
            'url': pool['url'],
            'height': height,
            'hashrate': hash_rate,
            'miners': miners,
            'fee': str(fee) + '%' if '%' not in str(fee) else fee,
            'min_payout': min_payout,
            'last_block_timestamp': last_block
        }
    )

active_pools = json.dumps(active_pools, indent=4)

with open('../data/pools-data.json', 'w') as f:
    f.write(active_pools)
