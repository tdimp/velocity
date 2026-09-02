{{ config(materialized='view') }}

select * from {{ source('raw', 'station_information') }}