{{ config(materialized='table') }}

select
  status.station_id,
  status.retrieved_at,
  status.last_reported,
  status.num_bikes_available,
  status.num_docks_available,
  status.num_bikes_available = 0 as is_empty,
  case
    when status.weekday_num between 1 and 5
      then 'weekday'
    when status.weekday_num = 6
      then 'saturday'
    when status.weekday_num = 7
      then 'sunday'
  status.day_of_week,
  status.time_of_day
from {{ ref('int_station_snapshots') }}

