#!/usr/bin/python3

import sys
import json
import subprocess
from pathlib import Path

from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=1)
cors = CORS(app)

# noinspection PyTypeChecker
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["2 per second"]
)

subprocess.call([sys.executable, Path(__file__).parent / '../utils/data_init.py'])
subprocess.call([sys.executable, Path(__file__).parent / '../utils/history_data_init.py'])

subprocess.call([sys.executable, Path(__file__).parent / '../utils/blocks_data_init.py'])


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


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
