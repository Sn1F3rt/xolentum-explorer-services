import os

location = os.getcwd().replace('/utils', '/data')

files = [
    'nodes-data.json', 
    'pools-data.json', 
    'nodes-history-data.json', 
    'pools-history-data.json'
  ]

for file in files:
    os.remove(os.path.join(location, file))
