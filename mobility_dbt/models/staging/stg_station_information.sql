{{ config(materialized='view') }}

with source as (
  select * from {{ source('raw', 'station_information') }}
)