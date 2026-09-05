{{ config(materialized='view') }}

select
  status.station_id,
  status.retrieved_at,
  status.last_reported,
  status.num_bikes_available,
  status.num_docks_available,
  status.num_bikes_available = 0 as is_empty,
  info.name,
  info.lat,
  info.lon,
  info.capacity,
  info.is_virtual_station,

  extract(hour from status.last_reported) as hour,
  extract(isodow from status.last_reported) as weekday_num,
  trim(to_char(status.last_reported, 'Day')) as weekday,
  case
    when extract(hour from status.last_reported) between 6 and 9
      then 'morning'
    when extract(hour from status.last_reported) between 10 and 15
      then 'midday'
    when extract(hour from status.last_reported) between 16 and 19
      then 'evening'
    else
      'night'
  end as time_of_day

from {{ ref('stg_station_status') }} as status

left join {{ ref('stg_station_information' )}} as info
on status.station_id = info.station_id