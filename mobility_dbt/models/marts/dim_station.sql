{{ config(materialized='table') }}

select
  info.station_id,
  info.name,
  info.lat,
  info.lon,
  info.capacity,
  info.is_virtual_station,
from {{ ref('int_empty_stations') }} info;
