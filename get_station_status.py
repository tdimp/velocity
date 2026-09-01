import requests
import json

URL = 'https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_bn/en/station_status.json'

response = requests.get(URL)
response.raise_for_status()

data = response.json()

print(data['data']['stations'])