#!/usr/bin/python3

import sys
import json
import subprocess
import atexit

from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=1)
cors = CORS(app)

# noinspection PyTypeChecker
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["2 per second"]
)


def perform_tasks():
    subprocess.call([sys.executable, '../utils/nodes_history_parser.py'])
    subprocess.call([sys.executable, '../utils/pools_history_parser.py'])

    subprocess.call([sys.executable, '../utils/nodes_parser.py'])
    subprocess.call([sys.executable, '../utils/pools_parser.py'])


subprocess.call([sys.executable, '../utils/history_data_init.py'])

scheduler = BackgroundScheduler()
scheduler.add_job(func=perform_tasks, trigger="interval", minutes=2)
scheduler.start()


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
    app.run(debug=True, use_reloader=False)

atexit.register(lambda: scheduler.shutdown())
