#!/usr/bin/python3

import sys
import json
import logging
import subprocess
from pathlib import Path

import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

# noinspection SpellCheckingInspection
logging.basicConfig(format='%(asctime)s - [%(levelname)s] %(message)s', level=logging.INFO)

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=1)
cors = CORS(app)

# noinspection PyTypeChecker
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["2 per second"],
    default_limits_exempt_when=lambda:
    request.environ.get('HTTP_ORIGIN', None) == 'https://explorer.xolentum.org'
)

logging.info('Clearing stale data')
subprocess.call([sys.executable, Path(__file__).parent / '../utils/data_init.py'])
logging.info('Stale data cleared')

logging.info('Initializing history')
subprocess.call([sys.executable, Path(__file__).parent / '../utils/history_data_init.py'])
logging.info('History initialized')

"""
if Path(Path(__file__).parent / '../data/blocks-data.json').exists():
    logging.info('Updating existing cached blocks data')
    subprocess.call([sys.executable, Path(__file__).parent / '../utils/blocks_parser.py'])
    logging.info('Existing blocks data updated')

else:
    logging.info('Caching blocks data')
    subprocess.call([sys.executable, Path(__file__).parent / '../utils/blocks_data_init.py'])
    logging.info('Blocks data initialized')

logging.info('Application successfully initialized')
"""


@app.route('/nodes', methods=['GET'])
def nodes():
    with open(Path(__file__).parent / '../data/nodes-data.json') as f:
        data = json.load(f)

    return jsonify(data)


@app.route('/pools', methods=['GET'])
def pools():
    with open(Path(__file__).parent / '../data/pools-data.json') as f:
        data = json.load(f)

    return jsonify(data)


@app.route('/blocks', methods=['GET'])
def blocks():
    with open(Path(__file__).parent / '../data/blocks-data.json') as f:
        data = json.load(f)

    return jsonify(data)


@app.route('/node_web', methods=['GET', 'POST'])
@app.route('/node_web/<end_point>', methods=['GET', 'POST'])
def node_web(end_point=None):
    with open(Path(__file__).parent / '../config.json') as f:
        data = json.load(f)
        daemon_host = data['daemon_host']
        daemon_port = data['daemon_port']
        ssl = data['ssl']

    if request.method == 'GET':
        r = requests.get(
            url=f'{"http" if not ssl else "https"}://{daemon_host}:{daemon_port}/'
            f'{end_point if end_point else "json_rpc"}'
        )

        if r.status_code != 404:
            return jsonify(r.json()), r.status_code

        else:
            return jsonify({'message': 'Method not found.'}), 404

    else:
        params = request.get_json(force=True)

        r = requests.post(
            url=f'{"http" if not ssl else "https"}://{daemon_host}:{daemon_port}/'
            f'{end_point if end_point else "json_rpc"}',
            data=json.dumps(params),
            headers={
                'Content-Type': 'application/json'
            }
        )

        if r.status_code != 404:
            return jsonify(r.json()), r.status_code

        else:
            return jsonify({'message': 'Method not found.'}), 404


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
