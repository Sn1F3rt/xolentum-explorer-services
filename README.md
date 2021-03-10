# Xolentum Block Explorer Services (XES)

## About

A high-availability Flask API for [Xolentum Block Explorer](https://explorer.xolentum.org)

this API serves the data for `Nodes` and `Pools`, along with uptime history. The list of available Xolentum public nodes and mining pools can be found [here](https://github.com/xolentum/public-nodes-json) and [here](https://github.com/xolentum/mining-pools-json) respectively.

## Requirements

* `python3` (tested on **v3.8.5**)
* `git`

## Installation

Clone the repository either using `git` or by downloading a ZIP file using the *Download* button above. 

```
git clone https://github.com/sohamb03/xolentum-explorer-services.git
```

Install `pipenv` and then install the dependencies, and enter the shell. 

```
python3 -m venv .venv

source .venv/bin/activate
pip3 install -r requirements.txt
```

## Usage

For development:

```
python3 -m api.main 
```

For production, it is recommended to use gunicorn and run the application as a system service, proxied by Nginx.

An example system unit file `xes.service` has been provided. Replace the necessary information in the file, copy it into the system unit files directory and start the API. 

```
sudo cp xes.service /etc/systemd/system

sudo systemctl daemon-reload
sudo systemctl enable --now xes
``` 

You can check that the service started successfully by using `sudo systemctl status xes`.

Setup Nginx permissions:

```
sudo usermod -aG sohamb03 nginx
chmod 710 /home/sohamb03

sudo nginx -t
sudo systemctl enable --now nginx
```

Install the required cron jobs:

```
crontab -l | { cat; echo "*/2 * * * * . $HOME/.bash_profile; ~/xolentum-explorer-services/.venv/bin/python3 ~/xolentum-explorer-services/utils/nodes_history_parser.py >/dev/null 2>&1"; } | crontab -
crontab -l | { cat; echo "*/2 * * * * . $HOME/.bash_profile; ~/xolentum-explorer-services/.venv/bin/python3 ~/xolentum-explorer-services/utils/pools_history_parser.py >/dev/null 2>&1"; } | crontab -

crontab -l | { cat; echo "*/3 * * * * . $HOME/.bash_profile; ~/xolentum-explorer-services/.venv/bin/python3 ~/xolentum-explorer-services/utils/nodes_parser.py >/dev/null 2>&1"; } | crontab -
crontab -l | { cat; echo "*/3 * * * * . $HOME/.bash_profile; ~/xolentum-explorer-services/.venv/bin/python3 ~/xolentum-explorer-services/utils/pools_parser.py >/dev/null 2>&1"; } | crontab -
crontab -l | { cat; echo "*/10 * * * * . $HOME/.bash_profile; ~/xolentum-explorer-services/.venv/bin/python3 ~/xolentum-explorer-services/utils/blocks_parser.py >/dev/null 2>&1"; } | crontab -
```

## License 

[BSD-3-Clause License](LICENSE)

Copyright &copy; 2020 Sayan Bhattacharyya, The Xolentum Project
