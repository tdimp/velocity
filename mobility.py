import requests
import json

data = requests.get('https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_bn/gbfs.json')

for name in data.json()['data']['en']['feeds']:
    print(name['name'])