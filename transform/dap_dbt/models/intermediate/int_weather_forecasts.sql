select
    swf.weather_forecast_id,
    swf.city_id,
    sl.city_name_en,
    swf.forecast_at,
    swf.weather_name,
    swf.weather_description,
    swf.temperature_celsius,
    swf.feels_like_temperature_celsius,
    swf.minimum_temperature_celsius,
    swf.maximum_temperature_celsius,
    swf.humidity_percentage,
    swf.wind_speed,
    swf.wind_direction,
    swf.precipitation_probability,
    swf.part_of_day,
    swf.cloud_coverage_percentage
from
    {{ ref('stg_weather_forecasts') }} as swf
inner join
    {{ ref('stg_locations') }} as sl
on swf.city_id = sl.city_id
