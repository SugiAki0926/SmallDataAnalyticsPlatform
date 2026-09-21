{{
    config(
        materialized='incremental',
        unique_key='current_weather_id',
        incremental_strategy='merge',
    )
}}
select
    scw.current_weather_id,
    scw.city_id,
    sl.city_name_en,
    scw.current_weather_at,
    scw.created_at,
    scw.updated_at,
    scw.weather_name,
    scw.temperature_celsius
from {{ ref('stg_current_weather') }} as scw
inner join {{ ref('stg_locations') }} as sl
    on scw.city_id = sl.city_id
{% if is_incremental() %}
where scw.updated_at > (select max(updated_at) from {{ this }})
{% endif %}
