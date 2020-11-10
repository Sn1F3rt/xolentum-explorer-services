# Xolentum Block Explorer Utils

## About

A high-availabilty Flask API for [Xolentum Block Explorer](https://explorer.xolentum.org)

this API serves the data for `Nodes` and `Pools`, along with uptime history. The list of available Xolentum public nodes and mining pools can be found [here](https://github.com/xolentum/public-nodes-json) and [here](https://github.com/xolentum/mining-pools-json) respectively.

## Installation

Clone the repository either using `git` or by downloading a ZIP file using the *Download* button above. 

```sh
git clone https://github.com/sohamb03/xolentum-explorer-utils.git
```

Install `pipenv` and then install the dependencies, and enter the shell. 

```sh
python3 -m pip pipenv

pipenv install
pipenv shell
```

## Usage

For development,

```sh
cd api && python3 main.py
```

For production, start the application using gunicorn. 

```sh
gunicorn -w 5 -b 127.0.0.1:5000 wsgi
```

## License 

[BSD-3-Clause License](LiCENSE)

Copyright © 2020 Sayan Bhattacharyya, The Xolentum Project
