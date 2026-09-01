import requests
from datetime import datetime, timezone
from db import get_connection
from psycopg.types.json import Jsonb

URL = 'https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_bn/en/station_status.json'


def get_station_status():
    response = requests.get(URL)
    response.raise_for_status()
    
    data = response.json()
    return data['data']['stations']


def load_station_status(stations):
    retrieved_at = datetime.now(timezone.utc)
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            for station in stations:
                last_reported = datetime.fromtimestamp(
                    station['last_reported'],
                    tz=timezone.utc
                )
                cur.execute(
                    """
                    INSERT INTO station_status (
                        station_id,
                        num_bikes_available,
                        vehicle_types_available,
                        num_docks_available,
                        is_installed,
                        is_renting,
                        is_returning,
                        last_reported,
                        retrieved_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        station['station_id'],
                        station['num_bikes_available'],
                        Jsonb(station['vehicle_types_available']),
                        station['num_docks_available'],
                        station['is_installed'],
                        station['is_renting'],
                        station['is_returning'],
                        last_reported,
                        retrieved_at
                    )
                )


def validate_station_status(stations):
    if not stations:
        raise ValueError('No station data retrieved from API.')
    
    required_fields = {
        'station_id',
        'num_bikes_available',
        'vehicle_types_available',
        'num_docks_available',
        'is_installed',
        'is_renting',
        'is_returning',
        'last_reported',
    }
    
    for i, station in enumerate(stations):
        missing_fields = required_fields - station.keys()
        
        if missing_fields:
            raise ValueError(f'Station {i} is missing fields: {missing_fields}')
    
    return True


if __name__ == '__main__':
    stations = get_station_status()
    validate_station_status(stations)
    load_station_status(stations)
    
    print(f'Loaded {len(stations)} station records.')