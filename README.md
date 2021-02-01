# Xolentum Block Explorer Utils

## About

A high-availability Flask API for [Xolentum Block Explorer](https://explorer.xolentum.org)

this API serves the data for `Nodes` and `Pools`, along with uptime history. The list of available Xolentum public nodes and mining pools can be found [here](https://github.com/xolentum/public-nodes-json) and [here](https://github.com/xolentum/mining-pools-json) respectively.

## Installation

Clone the repository either using `git` or by downloading a ZIP file using the *Download* button above. 

```sh
git clone https://github.com/sohamb03/xolentum-explorer-utils.git
```

Install `pipenv` and then install the dependencies, and enter the shell. 

```sh
python3 -m pip install pipenv

pipenv install
pipenv shell
```

## Usage

For development:

```sh
cd api && python3 main.py
```

For production, it is recommended to use gunicorn:

```sh
gunicorn -w 5 -b 127.0.0.1:5000 wsgi
```

An example system unit file `xolentum-explorer-utils.service` has been provided. Replace the necessary information in the file, copy it into the system unit files directory and start the API. 

```sh
sudo cp xolentum-explorer-utils.service /etc/systemd/system

sudo systemctl daemon-reload
sudo systemctl enable --now xolentum-explorer-utils
``` 

You can check that the service started successfully by using `sudo systemctl status xolentum-explorer-utils`.

Install the required cron jobs:

```sh
crontab -l | { cat; echo "*/2 * * * * python3 ~/xolentum-explorer-utils/utils/nodes_history_parser.py >/dev/null 2>&1"; } | crontab -
crontab -l | { cat; echo "*/2 * * * * python3 ~/xolentum-explorer-utils/utils/pools_history_parser.py >/dev/null 2>&1"; } | crontab -

crontab -l | { cat; echo "*/2 * * * * python3 ~/xolentum-explorer-utils/utils/nodes_parser.py >/dev/null 2>&1"; } | crontab -
crontab -l | { cat; echo "*/2 * * * * python3 ~/xolentum-explorer-utils/utils/pools_parser.py >/dev/null 2>&1"; } | crontab -
crontab -l | { cat; echo "*/2 * * * * python3 ~/xolentum-explorer-utils/utils/blocks_parser.py >/dev/null 2>&1"; } | crontab -
```

## License 

[BSD-3-Clause License](LICENSE)

Copyright &copy; 2020 Sayan Bhattacharyya, The Xolentum Project
