import json
import requests

r = requests.post(url='http://localhost:5000/node_web/get_transactions',
                  json=json.dumps({"txs_hashes":["b387a534420880f5fc9ee8e033ea4e2a496efa86faefea70e2e6ce6bae7751b4"],"decode_as_json":True}))

print(r.json())
