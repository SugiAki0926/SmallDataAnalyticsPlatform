with current_weather_hourly as (
    select
        current_weather_hour,
        city_id,
        city_name_en,
        weather_name,
        temperature_celsius,
        minimum_temperature_celsius,
        maximum_temperature_celsius,
        humidity_percentage,
        wind_speed
    from (
        select
            date_trunc('hour', current_weather_at) as current_weather_hour,
            city_id,
            city_name_en,
            weather_name,
            temperature_celsius,
            minimum_temperature_celsius,
            maximum_temperature_celsius,
            humidity_percentage,
            wind_speed,
            row_number() over (
                partition by
                    city_id,
                    date_trunc('hour', current_weather_at)
                order by current_weather_at desc
            ) as rn
        from
            {{ ref('int_current_weather') }}
    ) as ranked
    where rn = 1
), air_pollution_hourly as (
    select
        air_pollution_hour,
        city_id,
        carbon_monoxide,
        nitrogen_monoxide,
        nitrogen_dioxide,
        ozone,
        sulphur_dioxide,
        fine_particulate_matter,
        coarse_particulate_matter,
        ammonia
    from (
        select
            date_trunc('hour', air_pollution_at) as air_pollution_hour,
            city_id,
            carbon_monoxide,
            nitrogen_monoxide,
            nitrogen_dioxide,
            ozone,
            sulphur_dioxide,
            fine_particulate_matter,
            coarse_particulate_matter,
            ammonia,
            row_number() over (
                partition by
                    city_id,
                    date_trunc('hour', air_pollution_at)
                order by air_pollution_at desc
            ) as rn
        from
            {{ ref('int_air_pollution') }}
    ) as ranked
    where rn = 1
)
select
    current_weather_hour,
    cwh.city_id,
    city_name_en,
    weather_name,
    temperature_celsius,
    minimum_temperature_celsius,
    maximum_temperature_celsius,
    humidity_percentage,
    wind_speed,
    fine_particulate_matter,
    coarse_particulate_matter
from
    current_weather_hourly as cwh
left join
    air_pollution_hourly as awh
on
    cwh.current_weather_hour = awh.air_pollution_hour
    and cwh.city_id = awh.city_id
order by
    cwh.current_weather_hour ASC
