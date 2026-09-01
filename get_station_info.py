import requests
from db import get_connection

URL = 'https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_bn/en/station_information.json'

response = requests.get(URL)
response.raise_for_status()

data = response.json()

stations = data['data']['stations']

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