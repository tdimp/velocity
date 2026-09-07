{{ config(materialized='table') }}

select
  a.station_id,
  a.retrieved_at,
  a.last_reported,
  a.num_bikes_available,
  a.num_docks_available,
  a.is_empty,

  case
    when a.weekday_num between 1 and 5
      then 'weekday'
    when a.weekday_num = 6
      then 'saturday'
    when a.weekday_num = 7
      then 'sunday'
  end as day_type,

  a.day_of_week,
  a.time_of_day

from {{ ref('int_station_snapshots') }} as a

