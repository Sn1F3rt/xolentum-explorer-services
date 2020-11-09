#!/usr/bin/python3

import sys
import time
import subprocess
import json

from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.contrib.fixers import ProxyFix
import schedule

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=1)
cors = CORS(app)

# noinspection PyTypeChecker
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["2 per second"]
)


@app.route('/nodes', methods=['GET'])
def nodes():
    with open('../data/nodes-data.json') as f:
        data = json.load(f)

    return jsonify(data)


@app.route('/pools', methods=['GET'])
def pools():
    with open('../data/pools-data.json') as f:
        data = json.load(f)

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)

    schedule.every(5).minutes.do(subprocess.call([sys.executable, '../utils/nodes_parser.py']))
    schedule.every(5).minutes.do(subprocess.call([sys.executable, '../utils/pools_parser.py']))

    while True:
        schedule.run_pending()
        time.sleep(1)
