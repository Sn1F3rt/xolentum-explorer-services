import os

location = os.getcwd().replace('/utils', '/data')

files = [
    'nodes-data.json', 
    'pools-data.json', 
    'nodes-history-data.json', 
    'pools-history-data.json'
  ]

for file in files:
    try:
        os.remove(os.path.join(location, file))
    except FileNotFoundError:
        continue
