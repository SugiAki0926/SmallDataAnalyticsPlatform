select
    scw.current_weather_id,
    scw.city_id,
    sl.city_name_en,
    scw.current_weather_at,
    scw.weather_name,
    scw.temperature_celsius,
    scw.minimum_temperature_celsius,
    scw.maximum_temperature_celsius,
    scw.humidity_percentage,
    scw.wind_speed
from
    {{ ref('stg_current_weather') }} as scw
inner join
    {{ ref('stg_locations') }} as sl
on scw.city_id = sl.city_id
