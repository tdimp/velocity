{{ config(materialized='view') }}

with empty_station_observations as (

  select 
    station_id,
    num_bikes_available,
    num_docks_available,
    last_reported,
    retrieved_at
  from {{ ref('stg_station_status') }} 
  where num_bikes_available = 0

)

select
  e.station_id,
  info.name,
  info.lat,
  info.lon,
  info.capacity,
  info.is_virtual_station,
  e.num_bikes_available,
  e.num_docks_available,
  e.last_reported,
  e.retrieved_at

from empty_station_observations e

left join {{ ref('stg_station_information') }} info on e.station_id = info.station_id