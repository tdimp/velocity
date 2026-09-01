import requests
from db import get_connection

URL = 'https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_bn/en/station_information.json'


def get_station_info():
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    return data['data']['stations']


def load_station_info(stations):
    with get_connection() as conn:
     with conn.cursor() as cur:
         for station in stations:
             cur.execute(
                 """
                 INSERT INTO station_information (
                     station_id,
                     name,
                     short_name,
                     lat,
                     lon,
                     region_id,
                     is_virtual_station,
                     capacity
                     )
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                 ON CONFLICT (station_id) DO UPDATE SET
                     name = EXCLUDED.name,
                     short_name = EXCLUDED.short_name,
                     lat = EXCLUDED.lat,
                     lon = EXCLUDED.lon,
                     region_id = EXCLUDED.region_id,
                     is_virtual_station = EXCLUDED.is_virtual_station,
                     capacity = EXCLUDED.capacity
                 """,
                 (
                     station['station_id'],
                     station['name'],
                     station['short_name'],
                     station['lat'],
                     station['lon'],
                     station['region_id'],
                     station['is_virtual_station'],
                     station.get('capacity')
                 )
             )


def validate_station_info(stations):
    if not stations:
        raise ValueError('No station info retrieved from API.')
    
    required_fields = {
        'station_id',
        'name',
        'lat',
        'lon',
        'region_id',
    }
    
    for station in stations:
        missing_fields = required_fields - station.keys()
        
        if missing_fields:
            raise ValueError(f'Station {station["station_id"]} is missing fields: {missing_fields}')
    
    return True


if __name__ == '__main__':
    stations = get_station_info()
    validate_station_info(stations)
    load_station_info(stations)